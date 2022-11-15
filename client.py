import socket
import sys

MIN_PORT = 0
MAX_PORT = 65536

def validate_args(args):

    if not(len(args) == 2):
        print("Ilegal number of argument")
        return False

    port_num = 0
    
    try:
        port_num =  int(port_num)
    except:
        print("Port number must be a number")
        return False

    if port_num <= MIN_PORT or port_num >= MAX_PORT:
        print("Invalid port number")
        return False
    
    return True


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