# OIDC using Microsoft Authentication Library (MSAL)

## Overview
An implementation of the OIDC authentication flow to issue ID tokens which verify each instance of the program. Makes use of the Python `msal` library and the **Microsoft Identity Platform** in order to verify the identities of users.

#### `main.py`
Drives the program: responsible for issuing, validating and swapping tokens with another program instance

#### `server.py`
Contains the methods which listen for a response from Microsoft's redirection after the user has successfully logged in, as well as handling the token swap between two clients

#### `utils.py`
Contains various methods used throughout the other files, including the method that starts the authentication process with Microsoft and a method to verify any received tokens


## Setup & Running

### Requirements
Python 3.8+, as well as the following libraries:
- `msal`
- `cryptography`

All other libraries used are part of Python's standard library.

You'll also need to [register the application](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-protocols-oidc/) in your **Azure Active Directory** and obtain the **client ID**.
Once you have this, export it as an environment variable:

    export CLIENT="<Your ID goes here>"

### Running the Program
Download the code, and navigate to the location of the code in your terminal

Run the command:
  
    python main.py <FILEPATH>

to start an instance of the program, where FILEPATH is the where you want the token to be stored (including the file name). Note that Microsoft uses **JSON Web Tokens**, so the file should be a `.json` file. 

Your default web browser should launch, and you will need to log in with a Microsoft account (personal or work/school). Once complete, the browser will be redirected to `localhost:8000`. It's possible that you may see a "Connection reset" page, ignore it and close the web browser. If you have successfully completed the authentication flow, you should now see this message in the terminal:

    Received token for <NAME>, issued <DATE> expires <DATE>

Navigate to the file path you specified when running the program, and open the new `.json` file, the contents should look like:

    {
        "<field name>": "<value>"
        ...
    }

[Click here](https://learn.microsoft.com/en-us/azure/active-directory/develop/id-token-claims-reference?source=recommendations) to find out what each field corresponds to.
