import socket
import sys


def validate_args(args):
    if not(sys.argv[2].isnumeric()):
        return False
    if int(sys.argv[2]) in range(1, 65535):
        return True
    else:
        return False


def main():
    
    if not(validate_args(sys.argv)):
        exit()
    
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        operation = input()
        s.sendto(operation.encode(), (server_ip, server_port))
        
        data, addr = s.recvfrom(1024)
        print(bytes.decode(data))
        # debugg -> print(str(data), addr)
        

    s.close()


if __name__ == "__main__":
    main()