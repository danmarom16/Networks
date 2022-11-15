import socket
import sys

def validate_args(args):
    if not(sys.argv[2].isnumeric()):
        return False
    if int(sys.argv[2]) in range(1, 65536):
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
        if operation.isdigit() and (int(operation) == 4):
            s.close()
            exit()
        elif bytes.decode(data) == '':
            continue
        print(bytes.decode(data))

if __name__ == "__main__":
    main()