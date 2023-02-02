import argparse
import json

import wearipedia


# The rudimentary command line interface for wearipedia
def parse_CLI():
    desc = """
    Wearipedia is a tool for accessing and extracting data from 
    various wearable devices, such as devices from FitBit and Oura. This tool
    can be used by individuals monitoring their health, clinical researchers, 
    health coaches, and biotech companies for development of new products. 

    Currently for simple data extraction, one must specify the '--extract' flag with the specific device brand
    and model, the '--type' flag with the specific data type such as metrics, and the '--auth_creds' flag with
    your credentials to access device data (otherwise synthetic data will be provided). 
    
    For more information about the current development and more detailed descriptions about the tool,
    please visit the Github README page at https://github.com/Stanford-Health/wearipedia or visit our 
    documentation website at https://wearipedia.readthedocs.io/.

    Example for real data extraction:
    wearipedia --extract garmin/fenix_7s --type steps --auth_creds path/to/creds.json

    Example for synthetic data extraction: 
    wearipedia --extract garmin/fenix_7s --type steps --synthetic

    """
    # Create parser for CL
    parser = argparse.ArgumentParser(
        prog="wearipedia",
        description=desc,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Group synthetic data and real data authorizer as mutually exclusive
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-ac",
        "--auth_creds",
        type=str,
        help="the textfile of authetication credentials for a specific device: -ac /FILENAME;",
    )
    group.add_argument(
        "-s",
        "--synthetic",
        action="store_true",
        help="generate synthetic data instead of real data (not compatible w/ --auth_creds);",
    )

    # The rest of the flags
    parser.add_argument(
        "-e",
        "--extract",
        type=str,
        required=True,
        help="the filepath to the notebook for the device and its model: -e /FILEPATH;",
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        required=True,
        help="the type of data to extracted: -t metric;",
    )
    parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        help="the output file for the data to stored into (only .txt and.json files): -o /FILENAME;",
    )

    # Convert parsed CL into dictionary
    args, remaining = parser.parse_known_args()

    args = vars(args)

    # run the command line args into wearipedia tool
    switch(args, remaining)


# Populates parameter dict to pass along data collection
def get_params_dict(remaining_args: list):
    param_dict = {
        ".".join(k.split(".")[1:]): v
        for k, v in zip(remaining_args[::2], remaining_args[1::2])
    }

    return param_dict


# Check device type and instantiate an object based on it
# If credentials are added, try them for a specific device instance, returns device instance
def create_device_object(arg_dict: dict, remaining_args: list, synthetic: bool):

    # currently only supports Whoop4 and Garmin Fenix 7s devices
    device = wearipedia.get_device(arg_dict["extract"])

    # check if credentials are present
    if not synthetic:
        try:
            with open(arg_dict.get("auth_creds", "")) as json_file:
                creds = json.load(json_file)
                # temporary: will take in kwargs once authenticate() refactor is in
                device.authenticate(creds)
        except Exception as e:
            raise Exception(
                f"{e}\nInvalid credentials. Switching to synthetic data generation."
            )

    # for replacing the default params inside the specific device child classes
    new_params = get_params_dict(remaining_args)

    # temporary: after get_data() refactor, should be streamlined
    params = device._default_params()

    for k, v in new_params.items():
        params[k] = v

    raw_data = device.get_data(arg_dict["type"], params=params)

    # check if output file exists and is valid
    output_file = arg_dict["output_path"]

    if not output_file:
        print(raw_data)

    if output_file.lower().endswith(".json"):
        json.dump(raw_data, open(output_file, "w"))
    elif output_file.lower().endswith(".txt"):
        with open(output_file, "w") as f:
            f.write(str(raw_data))
    else:
        raise Exception("Invalid file extension.")


# Switch case implementation for Python version compatibility
def switch(case: dict, remaining: list):
    # go through each possible use case currently laid out
    arg_keys = sorted(case.keys())
    # wearipedia --extract whoop/whoop_4 --type metrics --auth_creds path/to/creds.json
    if case["auth_creds"] and case["extract"] and case["type"]:
        create_device_object(case, remaining, False)
    # wearipedia --extract whoop/whoop_4 --type metrics --synthetic
    elif case["extract"] and case["synthetic"] and case["type"]:
        create_device_object(case, remaining, True)
    else:
        raise Exception(
            "The following arguments ", case, " are not valid use cases currently."
        )


if __name__ == "__main__":
    parse_CLI()
