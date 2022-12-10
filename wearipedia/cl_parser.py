import argparse
import json

import wearipedia


# The rudimentary command line interface for wearipedia
def parse_CLI():
    desc = """Wearipedia is a tool for accessing and extracting data from 
    various wearable devices, such as devices from FitBit and Oura. This tool
    should be used by individuals monitoring their health, clinical researchers, 
    health coaches, and biotech companies for development of new products. 

    Currently for simple data extraction, one must specify the '--extract' flag with the specific device brand
    and model, the '--type' flag with the specific data type such as metrics, and the '--auth_creds' flag with
    your credentials to access device data (otherwise synthetic data will be provided). 
    
    For more information about the current development and more detailed descriptions about the tool,
    please visit the Github README page at https://github.com/Stanford-Health/wearipedia or visit our 
    documentation website at https://wearipedia.readthedocs.io/.

    Example for real data extraction: 
    wearipedia --extract whoop/whoop_4 --type metrics --auth_creds path/to/creds.json

    Example for synthetic data extraction: 
    wearipedia --extract whoop/whoop_4 --type metrics --synthetic

    """
    # Create parser for CL
    parser = argparse.ArgumentParser(prog="wearipedia", description=desc)

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
        "-ps",
        "--params.start",
        type=str,
        help="specify the start date of data collection as such: -ps YYYY-MM-DD;",
    )
    parser.add_argument(
        "-pe",
        "--params.end",
        type=str,
        help="specify the end date of data collection as such: -pe YYYY-MM-DD;",
    )
    parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        help="the output file for the data to stored into (only .txt and.json files): -o /FILENAME;",
    )

    # Convert parsed CL into dictionary
    args = vars(parser.parse_args())

    # run the command line args into wearipedia tool
    switch(args)


# Populates parameter dict to pass along data collection
def get_params_dict(arg_dict: dict):
    params = {}
    for key in arg_dict:
        if key.startswith("params."):
            params[key[7:]] = arg_dict[key]
    return params


# Depending on the output flag, switch the outputs to either a file or STDOUT, returns validity of file
def has_valid_extension(file: str):
    try:
        return file.lower().endswith((".json", ".txt"))
    except:
        print("Not a valid output file (must end in .json or .txt).")
        return False


# Check device type and instantiate an object based on it
# If credentials are added, try them for a specific device instance, returns device instance
def create_device_object(arg_dict: dict, synthetic: bool):

    # currently only supports Whoop4 and Garmin Fenix 7s devices
    device = wearipedia.get_device(arg_dict["extract"])

    # check if credentials are present
    if not synthetic:
        try:
            with open(arg_dict.get("auth_creds", "")) as json_file:
                creds = json.load(json_file)
                device.authenticate(creds["email"], creds["password"])
        except Exception as e:
            print(e, "\nInvalid credentials. Switching to synthetic data generation.")

    # for replacing the default params inside the specific device child classes
    params = get_params_dict(arg_dict)
    data = device.get_data(arg_dict["type"], params=params)

    # check if output file exists and is valid
    print_to_console = True
    if arg_dict["output_path"]:
        output_file = arg_dict["output_path"]
        if has_valid_extension(output_file):
            try:
                # Get the data based on what type of data is requested and if it is synthetic/real
                with open(output_file, "w+") as f:
                    f.write(data)
                    print_to_console = False
            except:
                print("Output file failed to open. Printing results on screen.")
    if print_to_console:  # otherwise we just print output to STDOUT
        print(data)


# Switch case implementation for Python version compatibility
def switch(case: dict):
    # go through each possible use case currently laid out
    arg_keys = sorted(case.keys())
    # wearipedia --extract whoop/whoop_4 --type metrics --auth_creds path/to/creds.json
    if case["auth_creds"] and case["extract"] and case["type"]:
        create_device_object(case, False)
    # wearipedia --extract whoop/whoop_4 --type metrics --synthetic
    elif case["extract"] and case["synthetic"] and case["type"]:
        create_device_object(case, True)
    else:
        raise Exception(
            "The following arguments ", case, " are not valid use cases currently."
        )
