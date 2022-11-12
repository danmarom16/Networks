import socket
import sys
ERROR_MSG = "Ilegal request"


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
    Generate list of current members and sends it immediately
    to the client.
"""
def inform_new_client(client_details, sock, client_address):

   
    current_clients = list(client_details.keys())                               # Creates lists of current members

    
    if len(current_clients) != 0:                       

        print(current_clients)

        
        sock.sendto(', '.join(current_clients).encode(), client_address)        # sends the client list to the new client
    

"""
    Returns client name by his socket address
"""
def find_by_adress(client_address, clients_details):
    client_name = [key for key in clients_details.keys() if (clients_details[key] == client_address)]
    print(client_name)
    return client_name


"""
    Changes client name from the current name to a new one
"""
def change_name(waiting_updates, details ,current_name, new_name):

    # Assign the address of old client name to his new name as a new pair in the dict, and then delete the old one
    details[new_name] = details[current_name]
    del details[current_name]

    # Same as above 
    waiting_updates[new_name] = waiting_updates[current_name]
    del waiting_updates[current_name]


"""
    Adds an update message to each of the current clients 
    waiting_update_list of messages.
    DOES NOT sends it to the client immediately.
"""
def update_members(operation_num, operation_info, waiting_updates, client_name):

    if operation_num == 1:                                                          # in this case operation_info = name
        message = operation_info + " has joined"
    elif operation_num == 2:                                                        # in this case operation_info = Message
        message = client_name +  operation_info
    elif operation_num == 3:                                                        # in this case operation_info = New Name
        message = client_name + " changed his name to " + operation_info
    elif operation_num == 4:                                                        # in this case operation_info = ""
        message = client_name + " has left the group"
    else:
        message = ERROR_MSG

    for client in waiting_updates:                                                  # iterate through all clients and add the
        if client != client_name and message != ERROR_MSG:
            waiting_updates[client].append(message)                                 # message to their waiting updates






"""
    Handles the client request based on the operation number.
"""
def handle_client_request(request, address, details, waiting_updates, sock):

    splitted_request = bytes.decode(request).split()    # takes client request and breaks it down do matching                                                     
    operation_info = ""                                 # parameters for readability

    if len(splitted_request) == 2:
        operation_num = int(splitted_request[0])
        operation_info = splitted_request[1]
    else:
        operation_num = int(splitted_request[0])


    if operation_num == 1 :                                 # in this case operation_info = name
        details[operation_info] = address                   # save client info the current members list:
        waiting_updates[operation_info] = list()            # Create a new record for future messages:
        inform_new_client(details, sock, address)
        update_members(operation_num, operation_info, waiting_updates, operation_info)

    elif operation_num == 2:                                # in this case operation_info = Message
        name = find_by_adress(address)
        update_members(operation_num, operation_info, waiting_updates, name)

    elif operation_num == 3:                                # in this case operation_info = New Name
        current_name = find_by_adress(address)
        change_name(waiting_updates, details ,current_name, operation_info)
        update_members(operation_num, operation_info, waiting_updates, current_name)
    
    elif operation_num == 4:                                # in this case we dont have operation info
        to_remove_name = find_by_adress(address)
        del details[to_remove_name]
        del waiting_updates
        update_members(operation_num, operation_info, waiting_updates, to_remove_name)

    elif operation_num == 5:                                # in this case we dont have operation info
        name = find_by_adress(address)
        sock.sendto('\n'.join(waiting_updates[name]).encode, address)



def main():

    details = dict()                                # contains mapping {name -> (client_ip, client_port)}
    waiting_updates = dict()                        # contains mapping {(name, ip, port) -> [waiting_updates] }
    
    if not(validate_args(sys.argv)):
        exit()

    my_port = int(sys.argv[1])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', my_port))

    while True:
        request, address = s.recvfrom(1024)
        if not(validate_request(request)):
            print("Ilegal request")
            continue
        else:
            handle_client_request(request, address,details, waiting_updates, s)


if __name__ == "__main__":
    main()