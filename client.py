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
    
    #while True:
    operation = input()
    s.sendto(operation.encode(), (server_ip, server_port))
    
    data, addr = s.recvfrom(1024)
    # debugg -> print(str(data), addr)
    print(bytes.decode(data))

    s.close()


if __name__ == "__main__":
    main()