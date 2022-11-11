import socket
import sys

def validate_args(args):
    return True

def main():

    if not(validate_args(sys.argv)):
        exit()

    my_port = int(sys.argv[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', my_port))

    while True:
        data, addr = s.recvfrom(1024)
        print(str(data), addr)
        s.sendto(data.upper(), addr)


if __name__ == "__main__":
    main()