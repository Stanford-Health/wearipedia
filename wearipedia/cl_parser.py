import argparse
import json

import wearipedia


# The rudimentary command line interface for wearipedia
def parseCLI():
    desc = """Wearipedia is a tool for accessing and extracting data from 
    various wearable devices, such as devices from FitBit and Oura. This tool
    should be used by individuals monitoring their health, clinical researchers, 
    health coaches, and biotech companies for development of new products. This is
    not intended to be a data collection tool for marketing/advertisers. 

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

    # Formats start/end parameter to pass along data collection
    def formatStartEnd(argDict: dict):
        params = {}
        start = argDict.get("params.start", "")
        if start:
            params["start"] = start
        end = argDict.get("params.end", "")
        if end:
            params["end"] = end
        return params

    # Get the data based on what type of data is requested and if it is synthetic/real
    def getData(argDict: dict, deviceObj, file=None):
        # for replacing the default params inside the specific device child classes
        paramDict = {}
        if "params.start" in argDict and "params.end" in argDict:
            paramDict = formatStartEnd(argDict)
        data = deviceObj.get_data(argDict["type"], paramDict)
        if file:
            try:
                file.write(data)
            except:
                print(
                    "File failed to write synthetic output. Printing to console instead."
                )
                print(data)
            finally:
                file.close()

    # Depending on the output flag, switch the outputs to either a file or STDOUT, returns validity of file
    def checkOutput(file: str):
        return file.lower().endswith((".json", ".txt"))

    # Check device type and instantiate an object based on it
    # If credentials are added, try them for a specific device instance, returns device instance
    def createDeviceObject(argDict: dict, synthetic: bool):

        # currently only supports Whoop4 and Garmin Fenix 7s devices
        device = wearipedia.get_device(argDict["extract"])

        if not device:
            raise Exception("Not a valid device. Please try again.")

        # check if credentials are present
        if not synthetic:
            with open(argDict["auth_creds"]) as json_file:
                creds = json.load(json_file)
                try:
                    device.authenticate(creds["email"], creds["password"])
                except:
                    print(
                        "Invalid credentials. Switching to synthetic data generation."
                    )

        # check if output file exists and is valid
        if "output_path" in argDict:
            outputFile = argDict["output_path"]
            if checkOutput(outputFile):
                try:
                    f = open(outputFile, "w+")
                    getData(argDict, device, f)
                except:
                    print("Output file failed to open.")
            else:  # otherwise we just print output to STDOUT
                getData(argDict, device)

    # Switch case implementation for Python version compatibility
    def switch(case: dict):
        # go through each possible use case currently laid out
        argKeys = sorted(case.keys())
        # wearipedia --extract whoop/whoop_4 --type metrics --auth_creds path/to/creds.json
        if all(key in argKeys for key in ("auth_creds", "extract", "type")):
            createDeviceObject(case, False)
        # wearipedia --extract whoop/whoop_4 --type metrics --synthetic
        elif all(key in argKeys for key in ("extract", "synthetic", "type")):
            createDeviceObject(case, True)
        else:
            raise Exception(
                "The following arguments ", case, " are not valid use cases currently."
            )

    # run the command line args into wearipedia tool
    switch(args)
