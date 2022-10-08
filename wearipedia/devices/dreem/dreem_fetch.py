# @title Get available users
import json
import pprint

import pandas as pd
import requests
from tqdm import tqdm


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


def fetch_records(auth_dict, user):

    pass


##################################
# get stuff from a single record #
##################################


def get_download_info(record_ref, records_df):
    # get the record id
    id = records_df[records_df["Ref"] == record_ref]["Record ID"].iloc[0]

    url = (
        f"https://api.rythm.co/v1/dreem/algorythm/record/{id}/h5/?filename={record_ref}"
    )

    headers = {"Authorization": "Bearer " + auth_dict["token"]}

    out_dict = json.loads(requests.get(url, headers=headers).text)

    return out_dict


def fetch_hypnogram(auth_dict, records, record_id):
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

    hypnogram_df = get_hypnogram(record_id)

    return hypnogram_df


def fetch_eeg_file(auth_dict, records, record_ref):
    download_info = get_download_info(record_id, record_ref)

    assert download_info["status_display"] == "Available"

    download_url = download_info["data_url"]
    download_path = str(record_ref) + ".h5"

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
