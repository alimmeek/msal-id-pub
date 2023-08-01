# OIDC using Microsoft Authentication Library (MSAL)

## Overview
Implements the OIDC authentication flow to issue ID tokens which verify each instance of the program. Makes use of the Python `msal` library and the **Microsoft Identity Platform** in order to verify the identities of users.

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
  
    python main.py

to start an instance of the program. Your default web browser should launch, and you will need to log in with a Microsoft account (personal or work/school). Once complete, the browser will be redirected to `localhost:8000`. It's possible that you may see a "Connection reset" page, ignore it and close the web browser.</p>

If you have successfully completed the authentication flow, you should now see this message in the terminal:

    Received token for <NAME>, issued <DATE> expires <DATE>

Open another terminal window and run the program again (you'll have to log in again, you can choose either the same account as before, or a different one). Once the authentication flow has finished, close the web browser.
The terminals will now show that they have received another token:

    Received token for <NAME>
    {
        ...
    }
