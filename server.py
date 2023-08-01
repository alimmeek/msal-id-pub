import socket


SELF = "127.0.0.1"
TOKEN_PORT = 8000
CLIENT_PORT = 7878


def token() -> str:
    data = ""
    # Create a socket and bind to the given IP address and port number
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SELF,TOKEN_PORT))

        # Await for response, and accept the connection when ready
        s.listen()
        conn, _ = s.accept()
        message_len = -1
        expected = 0
        with conn:

            # Read message into buffer while data is being sent
            while message_len < expected:
                temp = conn.recv(1024).decode("utf-8")

                # Split the HTTP headers into a dictionary
                # Remove the 1st line since it is just the status code
                if "Content-Length" in temp:
                    no_newlines = temp.split('\r\n')[1:]
                    temp_dict = {}
                    for line in no_newlines:
                        try:
                            key, val = line.split(': ')
                            temp_dict[key] = val
                        except:
                            pass
                    
                    # HTTP specifies content length in headers so we can use this
                    # To determine how much data will be sent
                    expected = int(temp_dict['Content-Length'])
                
                # id_token is the beginning of the body
                # add 1 to account for message_len = -1 (only do this once)
                if "id_token" in temp:
                    message_len += len(temp[temp.index('id_token'):]) + 1
                else:
                    message_len += len(temp)

                # append the received data to the rest of the fetched data
                data += temp
            
            # Respond with HTTP OK and request to close the connection
            conn.send(b'HTTP/1.1 200 OK\r\n')
    return data

def client(my_token: str, send: bool, has_sent: bool) -> (str, bool):
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if send:
            # If we are attempting to send, try to connect to the destination 
            # port
            # If successful, send our token and change has_sent to True so 
            # we don't attempt to send the token again
            # If the connection is refused, it means the destination hadn't 
            # opened the port, so just return and try again later
            try:
                s.connect((SELF, CLIENT_PORT))
                s.send(my_token.encode())
                s.send(b'\r\n')
                has_sent = True
            except ConnectionRefusedError:
                return (None, has_sent)
        else:
            # Otherwise, we should listen for an incoming token
            # Avoids potential deadlock in the case of both clients waiting for
            # the other to send their token by using timeouts
            # If no connection is detected within 1 second, a TimeoutError is
            # raised, causing None to be returned
            # OSError can occur if the client are on the same device, and one
            # attempts to listen while the other is already listening
            try:
                s.bind((SELF, CLIENT_PORT))
                s.settimeout(1)
                s.listen()
                conn, _ = s.accept()
            except (OSError, TimeoutError):
                return (None, has_sent)
            
            # If a connection was successfully set up, read the incoming token
            # Break once the end of the message (indicated by \r\n) is received
            token = ""
            with conn:
                while True:
                    temp = conn.recv(1024).decode()
                    token += temp
                    if '\r\n' in temp:
                        break
            
            # Return the received token, removing the \r\n and replacing the 
            # single quotes with "" (allows us to use json to convert it to
            # a dict)
            return (token.replace("\r\n", "").replace("'", '"'), has_sent)
    return (None, has_sent)