import json
import sys

from utils import *


# Warning: Connection resets sometimes, not sure what's going on there
# It still issues you an ID token though

def main(path):
    # Retreive a token
    token = issue_token()

    if token == None:
        raise InvalidTokenError
    else:
        with open(path, 'w+') as f:
            json.dump(token, f, indent=2)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise SyntaxError("Missing file path")
    elif len(sys.argv) > 2:
        raise SyntaxError("Too many arguements")
    else:
        main(sys.argv[1])