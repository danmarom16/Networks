import socket
import sys

def debug_prints(s, data, addr):
    print(str(data), addr)
    s.sendto(data.upper(), addr)

def validate_args(args):
    return True

def validate_request(request):
    pass


def save_client_info(info, client_details):
    pass

def update_existing_members(operation_num, operation_info):
    pass

def inform_new_client(client_details):
    pass


def handle_client_request(request, client_address, 
                            clients_details, clients_waiting_updates):

    # takes client requst and breaks it down do matching parameters for readability
    splitted_request = request.split()
    if len(splitted_request) == 2:
        operation_num = int(splitted_request[0])
        operation_info = splitted_request[1]
    else:
        operation_num = int(splitted_request[0])

    if(operation_num == 1):
        save_client_info(operation_info, client_address)
        # update existing members that current client is added to the group
        update_existing_members(operation_num, operation_info)
        # update the new client who is already a member of the group
        inform_new_client(clients_details)









def main():

    # contains mapping {name -> (client_ip, client_port)}
    clients_details = dict()   

    # contains mapping {(name, ip, port) -> [waiting_updates] }
    clients_waiting_updates = dict()

    if not(validate_args(sys.argv)):
        exit()

    my_port = int(sys.argv[1])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', my_port))

    while True:
        client_request, client_address = s.recvfrom(1024)
        if not(validate_request(client_request)):
            print("Ileagal request")
            continue
        else:
            handle_client_request(client_request, client_address,
            clients_details, clients_waiting_updates)





if __name__ == "__main__":
    main()