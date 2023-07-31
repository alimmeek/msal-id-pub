import server
from utils import *

# TODO: Connection resets sometimes

def main():
    token = {}
    # Check whether we have a valid token
    # If we don't have a token, or it has expired, then issue a new token
    try:
        with open('token.json') as f:
            token = json.load(f)
        if invalid_time(token['nbf'], token['exp']):
            print("Old token expired - contacting Microsoft...")
            raise ExpiredTokenError
        else:
            print(f"Found token for {token['name']} expires on {datetime.datetime.fromtimestamp(token['exp'])}")
    except (FileNotFoundError, ExpiredTokenError):
        token = issue_token()    
    
    # Once we have a token, we need to trade with the other person
    # Should also keep track of whether our token has successfully been sent
    other_token = None
    has_sent = False
    while not has_sent or other_token == None:
        # If we've sent our token, we should only listen
        # If we've received the other token, we should only try to send
        # Otherwise, choose randomly
        to_send_or_not_to_send = False if has_sent else True if other_token != None else bool(random.choice((0,1)))
        temp, has_sent = server.client(str(token), to_send_or_not_to_send, has_sent)
        
        # If we've received a token, convert it to a dictionary
        if temp != None:
            other_token = json.loads(temp)
    
    # Verify received token
    if verify(other_token):
        print(f"Received valid token for {other_token['name']}")
        print(json.dumps(other_token, indent=2))


main()