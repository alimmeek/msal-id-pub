import socket


SELF = "127.0.0.1"
TOKEN_PORT = 8000


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
