import socket
import sys

"""
    Validate the port's number
"""
def validate_args():
    if not(sys.argv[2].isnumeric()):
        return False
    if int(sys.argv[2]) in range(1, 65536):
        return True
    else:
        return False


def main():

    # In case the port's number is invalid
    if not(validate_args()):
        exit()
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:

        # Get operation from the user
        operation = input()

        # Send the request to the server
        s.sendto(operation.encode(), (server_ip, server_port))

        # Receive the response from the server
        data, addr = s.recvfrom(1024)

        # In case the user send 4 - close the socket and the program
        if operation.isdigit() and (int(operation) == 4) and bytes.decode(data) == '':
            s.close()
            exit()
        elif bytes.decode(data) == '':
            continue
        print(bytes.decode(data))


if __name__ == "__main__":
    main()