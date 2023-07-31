import base64
import datetime
import json
import os
import random
import requests
import secrets
import string
import time
import webbrowser
import msal.oauth2cli.oidc as oidc

from cryptography.fernet import Fernet

import server


class MissingClientError(Exception):
    print("Error - set CLIENT environment variable")

# Exception to throw when a token is invalid
class InvalidTokenError(Exception):
    print("Error - Invalid token")


CLIENT = os.environ.get("CLIENT")
if CLIENT == None:
    raise MissingClientError


def invalid_time(t1: int, t2: int) -> bool:
    # Make sure the current time is between two given UNIX timestamps
    # Used to ensure the token hasn't expired
    t = time.time()
    return t < t1 or t > t2

def verify(decoded: dict, nonce: str = None) -> bool:
    # Verifies the contents of a token based on the advice given here:
    # https://learn.microsoft.com/en-us/azure/active-directory/develop/claims-validation
    try:
        if decoded['aud'] != CLIENT:
            return False
        if "https://login.microsoftonline.com" not in decoded['iss']:
            return False
        if invalid_time(decoded['nbf'], decoded['exp']):
            return False
        if nonce and decoded['nonce'] != nonce:
            return False
        if decoded['ver'] != "2.0":
            return False

        return True
    except KeyError:
        # Means that either the token doesn't follow Microsoft's layout
        # (and hence probably wasn't issued by Microsoft)
        # Or the token is missing required fields
        # Either way, the token shouldn't be considered valid
        return False

def issue_token() -> dict:
    # Stuff for the URL
    # For more info visit:
    # https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-protocols-oidc
    state = generate_state()
    nonce = secrets.token_urlsafe()

    # Prompt user to login to validate their identity
    # &prompt=login will force the user to reauthenticate themself, even if they
    # were logged in previously
    x = requests.get(f'''https://login.microsoftonline.com/common/oauth2/v2.0/authorize?
    client_id={CLIENT}
    &response_type=id_token
    &redirect_uri=http%3A%2F%2Flocalhost%3A8000%2F
    &response_mode=form_post
    &scope=openid+profile
    &state={state}
    &nonce={nonce}
    &prompt=login''')
    webbrowser.open_new(x.url)

    # Logging in will prompt Microsoft to send the ID token to 127.0.0.1:8000, so
    # we need to open that port and capture the incoming token
    # Don't need any of the headers so just ignore them
    data = server.token()
    body = data[data.index("id_token"):].split('&')

    # Write results into a dictionary for easy access
    contents = {}
    for el in body:
        key, val = el.split('=')
        contents[key] = val

    # Use Microsoft's OIDC library to decode the retrieved token and verify it
    token = oidc.decode_id_token(contents['id_token'])
    valid = verify(token, nonce=nonce)
    print(valid)
    if valid:
        # Store the token on the device so we don't have to keep contacting
        # Microsoft
        with open('token.json', 'w+') as f:
            json.dump(token, f, indent=2)
        print(f"Received token for {token['name']}, issued {datetime.datetime.fromtimestamp(token['iat'])} expires {datetime.datetime.fromtimestamp(token['exp'])}")
        return token
    
    # In case we recieve an invalid token
    return None

def code_verifier() -> bytes:
    code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
    return base64.urlsafe_b64encode(code_verifier.encode('utf-8'))

def generate_state() -> bytes:
    # Generates state to be used in the initial request URL
    cv = code_verifier()
    key = Fernet.generate_key()
    fernet = Fernet(key)

    return fernet.encrypt(cv)