import socket
import sys

def validate_args(args):
    return True


def main():
    
    if not(validate_args(sys.argv)):
        exit()
    
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        operation = input()
        s.sendto(operation.encode(), ('127.0.0.1', server_port))
        data, addr = s.recvfrom(1024)
        print(str(data), addr)

    s.close()


if __name__ == "__main__":
    main()