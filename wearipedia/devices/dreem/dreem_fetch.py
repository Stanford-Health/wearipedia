import json
import os
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm

EEG_LOCAL_DIR = "/tmp/wearipedia-cache/dreem/headband_2"

os.makedirs(EEG_LOCAL_DIR, exist_ok=True)


def get_aux_records(auth_dict):
    url = "https://api.rythm.co/v1/dreem/algorythm/restricted_list/9f38863b-8180-4dd4-81cf-9395800ae0cc/record/?limit=100&offset=0"

    headers = {"Authorization": "Bearer " + auth_dict["token"]}

    out = requests.get(url, headers=headers)

    out_dict = json.loads(out.text)

    return out_dict


def get_user2id_mapping(auth_dict, user_ids):
    url = "https://api.rythm.co/v1/dreem/dreemer/dreemer/details/"
    headers = {
        "Authorization": "Bearer " + auth_dict["token"],
        "Content-Type": "application/json",
    }

    payload = {"id": [user_id for user_id in user_ids]}

    out = requests.post(
        url,
        headers=headers,
        data='{"id":["ce73192e-874c-4576-a2e3-27b0dc0ebcee","1222a474-bc02-44ab-b4c5-d66dc34620b7","e1ec95b0-b71b-4499-b73c-cf9b1e3576c2"]}',
    ).text

    return {x["pseudo"]: x["dreemer"] for x in json.loads(out)}


def fetch_users(auth_dict):
    # we care about aux_records because:
    # (1) it contains the user_ids
    # (2) it contains a mapping between references and record id's
    aux_records = get_aux_records(auth_dict)

    # (1) here
    user_ids = {result["user"] for result in aux_records["results"]}

    map = get_user2id_mapping(auth_dict, user_ids)

    return map


############
# records! #
############


def get_table_records(auth_dict, record_ids):
    # this is distinct from aux_records

    # we get the *actual* info that is displayed on the table
    # in the web portal
    url = "https://api.rythm.co/v1/dreem/record/report/details/"

    headers = {
        "Authorization": "Bearer " + auth_dict["token"],
        "Content-Type": "application/json",
    }

    payload = {"id": record_ids}

    out_dict = json.loads(
        requests.post(url, headers=headers, data=json.dumps(payload)).text
    )

    return out_dict


def records_to_df(table_records, aux_records):
    columns = {
        "record_id": "Record ID",
        "record_start_iso": "Start (ISO)",
        "record_stop_iso": "Stop (ISO)",
        "timezone": "Timezone",
        "record_duration": "Duration (seconds)",
        "proportion_good_quality_eeg1": "Channel quality 1",
        "proportion_good_quality_eeg2": "Channel quality 2",
        "proportion_good_quality_eeg4": "Channel quality 4",
        "proportion_off_head": "Proportion off head",
        "proportion_scorable": "Proportion scorable",
    }

    list_of_dicts = []

    for record in table_records:

        d = {
            columns[key]: endpoint
            for key, endpoint in record["endpoints"].items()
            if key in columns.keys()
        }

        d["Record ID"] = record["record"]

        list_of_dicts.append(d)

    records_df = pd.DataFrame(list_of_dicts, columns=columns.values())

    # (2) here
    id2ref_map = {
        aux_record["id"]: aux_record["reference"] for aux_record in aux_records
    }

    records_df.insert(
        0, "Ref", records_df["Record ID"].apply(lambda id: id2ref_map[id])
    )

    return records_df


def fetch_records(auth_dict, username=None):

    aux_records = get_aux_records(auth_dict)

    uname_filter = username

    map_ = fetch_users(auth_dict)

    # optionally filter by username
    if username is None:
        filtered_aux_records = [record for record in aux_records["results"]]
    else:
        uid = [uid for uname, uid in map_.items() if uname == uname_filter][0]
        filtered_aux_records = [
            record for record in aux_records["results"] if record["user"] == uid
        ]

    record_ids = [record["id"] for record in filtered_aux_records]

    table_records = get_table_records(auth_dict, record_ids)

    records_df = records_to_df(table_records, filtered_aux_records)

    records_df = records_df.sort_values("Ref", ascending=False, ignore_index=True)

    return records_df


##################################
# get stuff from a single record #
##################################


def ref2id(auth_dict, record_ref):
    records_df = fetch_records(auth_dict)
    id = records_df[records_df["Ref"] == record_ref]["Record ID"].iloc[0]

    return id


def get_download_info(auth_dict, record_ref):
    # get the record id

    id = ref2id(auth_dict, record_ref)

    url = (
        f"https://api.rythm.co/v1/dreem/algorythm/record/{id}/h5/?filename={record_ref}"
    )

    headers = {"Authorization": "Bearer " + auth_dict["token"]}

    out_dict = json.loads(requests.get(url, headers=headers).text)

    return out_dict


def fetch_hypnogram(auth_dict, record_ref):
    record_id = ref2id(auth_dict, record_ref)
    url = f"https://api.rythm.co/v1/dreem/record/record/{record_id}/latest_hypnogram_as_txt/"

    headers = {"Authorization": "Bearer " + auth_dict["token"]}

    hypnogram_text = requests.get(url, headers=headers).text

    from io import StringIO

    # get index of header
    idx_start = [
        i for i, l in enumerate(hypnogram_text.split("\n")) if "Sleep Stage" in l
    ][0]

    hypnogram = pd.read_csv(
        StringIO("\n".join(hypnogram_text.split("\n")[idx_start:])), sep="\t"
    )

    return hypnogram


def fetch_eeg_file(auth_dict, record_ref):
    record_id = ref2id(auth_dict, record_ref)
    download_info = get_download_info(auth_dict, record_ref)

    assert download_info["status_display"] == "Available"

    download_url = download_info["data_url"]
    download_path = Path(EEG_LOCAL_DIR) / (str(record_ref) + ".h5")

    # Streaming, so we can iterate over the response.
    response = requests.get(download_url, stream=True)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
    with open(download_path, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")

    return download_path
