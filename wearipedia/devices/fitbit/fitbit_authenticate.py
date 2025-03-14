import base64
import hashlib
import os

import requests

__all__ = ["fitbit_token"]


def fitbit_application():
    """gives us access token given the auth_creds + going through the process, it's interactive
    Returns the client id and client secret"""

    params = {
        "Description": "Any thing here should suffice",
        "Application Website URL": "Place any url here, even google.com",
        "Organization": "type the name of the organization",
        "Organization Website URL": " type organization webiste",
        "Terms of Service URL": "Any Url should suffice",
        "Privacy Policy URL": "Any Url should suffice",
        "OAuth 2.0 Application Type": "choose the appropriate type",
    }

    print(
        "fill the following parameters in this url then input the resulting client id and secret: ",
        "https://dev.fitbit.com/apps/new",
        "\n",
    )
    for key, value in params.items():
        print(key, ":", value)

    client_id = input("Enter the client id: ")
    client_secret = input("Enter the client secret: ")

    return client_id, client_secret


def fitbit_token(client_id, client_secret):
    """generates an access token"""

    code_verifier = (
        base64.urlsafe_b64encode(os.urandom(43)).decode("utf-8")
        if "code_verifier" not in locals()
        else code_verifier
    )
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .decode("utf-8")
        .replace("=", "")
    )

    variables = dict()

    # user specified
    variables["client_id"] = client_id
    variables["client_secret"] = client_secret
    variables["expires_in"] = "31536000"  # expiry of token in seconds

    # constants or one-time generated
    variables["code_verifier"] = code_verifier
    variables["code_challenge"] = code_challenge
    variables["code_challenge_method"] = "S256"
    variables["response_type"] = "token"  # code
    variables["scope"] = (
        "weight%20location%20settings%20profile%20nutrition%20"
        + "activity%20sleep%20heartrate%20social%20"
        + "respiratory_rate%20oxygen_saturation"
    )
    variables["prompt"] = "none"
    variables["grant_type"] = "authorization_code"
    variables["authorization"] = base64.urlsafe_b64encode(
        bytes(variables["client_id"] + ":" + variables["client_secret"], "utf-8")
    ).decode("utf-8")

    # combine all parameters into the url string
    url = "https://www.fitbit.com/oauth2/authorize"  # authorization endpoint
    for key in [
        "client_id",
        "code_challenge",
        "code_challenge_method",
        "scope",
        "response_type",
        "expires_in",
    ]:
        if url == "https://www.fitbit.com/oauth2/authorize":
            url += "?" + key + "=" + variables[key]
        else:
            url += "&" + key + "=" + variables[key]

    print(
        "Click the URL above to access the Authorization page. Check Allow All and click the Allow button in red then input the resulting url",
        url,
    )

    authurl = input("Enter the resulting url: ")

    lst_of_token = []
    append = False
    for i in authurl:
        if i == "=":
            append = True
            continue
        elif i == "&":
            break
        if append == True:
            lst_of_token.append(i)

    access_token = "".join(lst_of_token)

    return access_token
