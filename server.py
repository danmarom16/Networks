import socket
import sys



def debug_prints(s, data, addr):
    print(str(data), addr)
    s.sendto(data.upper(), addr)



# TODO: validate arguments through all edge cases
def validate_args(args):
    return True



# TODO: validate request through all edge cases
def validate_request(request):
    return True



"""
    Adds an update message to each of the current clients 
    waiting_update_list of messages.
    DOES NOT sends it to the client immediately.
"""
def update_existing_members(operation_num, operation_info, clients_waiting_updates):
    if operation_num == 1:
        message = operation_info + " has joined"

    # iterate through all clients and add the message to their waiting updates  
    for client in clients_waiting_updates:
        clients_waiting_updates[client].append(message)



"""
    Generate list of current members and sends it immediately
    to the client.
"""
def inform_new_client(client_details, sock, client_address):

    # Creates lists of current members
    current_clients = list(client_details.keys())

    # if its not empty:
    if len(current_clients) != 0:

        print(current_clients)

        # sends the client list to the new client
        sock.sendto(', '.join(current_clients).encode(), client_address)
    


def handle_client_request(request, client_address, 
                            clients_details, clients_waiting_updates, sock):

    # clients_details: {name -> (client_ip, client_port)}
    # clients_waiting_updates: {name -> {name: [empty waiting updates list]}}

    # takes client request and breaks it down do matching parameters for readability
    splitted_request = bytes.decode(request).split()
    operation_info = ""

    if len(splitted_request) == 2:
        operation_num = int(splitted_request[0])
        operation_info = splitted_request[1]
    else:
        operation_num = int(splitted_request[0])

    # in this case operation operation_info = name
    if(operation_num == 1):
        
        # update the new client who is already a member of the group
        inform_new_client(clients_details, sock, client_address)

        # save client info the current members list:
        clients_details[operation_info] = client_address
        # Create a new record for future messages:
        clients_waiting_updates[operation_info] = list()

        # update existing members that current client is added to the group
        update_existing_members(operation_num, operation_info, clients_waiting_updates)





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
            print("Ilegal request")
            continue
        else:
            handle_client_request(client_request, client_address,
            clients_details, clients_waiting_updates, s)





if __name__ == "__main__":
    main()