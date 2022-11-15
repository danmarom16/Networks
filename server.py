import socket
import sys
ERROR_MSG = "Illegal request"


def debug_prints(s, data, addr):
    print(str(data), addr)
    s.sendto(data.upper(), addr)


def validate_args(args):
    if not(sys.argv[1].isnumeric()):
        return False
    if int(sys.argv[1]) in range(1, 65536):
        return True
    else:
        return False


def validate_request(request):
    splitted_request = bytes.decode(request).split(' ', 1)         # takes client request and breaks it down do matching
    if not(splitted_request[0].isdigit()):
        return False
    if len(splitted_request) == 2:
        if not(int(splitted_request[0]) in range(1, 4)):
            return False
        else:
            return True
    elif len(splitted_request) == 1:
        if not (int(splitted_request[0]) in range(4, 6)):
            return False
        else:
            return True
    else:
        return False


def check_if_registered(name):
    if name is None:
        return False
    else:
        return True

"""
    Generate list of current members and sends it immediately
    to the client.
"""
def inform_new_client(logged_users, sock, client_address):                             # Creates lists of current members
    if len(logged_users) != 0:                       
        sock.sendto(', '.join(logged_users).encode(), (client_address[0], client_address[1]))
    else:
        sock.sendto(b'', (client_address[0], client_address[1]))
    

"""
    Returns client name by his socket address
"""
def find_by_adress(client_address, clients_details):
    client_name = [key for key in clients_details.keys() if (clients_details[key] == client_address)]

    # in case the client is not registered
    if not client_name:
        return None
    return client_name[0]


"""
    Changes client name from the current name to a new one
"""
def change_name(waiting_updates, details ,current_name, new_name, logged_users):

    # Assign the address of old client name to his new name as a new pair in the dict, and then delete the old one
    details[new_name] = details[current_name]
    del details[current_name]

    # Same as above 
    waiting_updates[new_name] = waiting_updates[current_name]
    del waiting_updates[current_name]

    old_name_idx = logged_users.index(current_name)
    logged_users[old_name_idx] = new_name


"""
    Adds an update message to each of the current clients 
    waiting_update_list of messages.
    DOES NOT sends it to the client immediately.
"""
def update_members(operation_num, operation_info, waiting_updates, client_name):

    if operation_num == 1:                                                          # in this case operation_info = name
        message = operation_info + " has joined"
    elif operation_num == 2:                                                        # in this case operation_info = Message
        message = client_name + ": " +  operation_info
    elif operation_num == 3:                                                        # in this case operation_info = New Name
        message = operation_info + " changed his name to " + client_name
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
def handle_client_request(request, address, details,
                          waiting_updates, sock, logged_users):

    splitted_request = bytes.decode(request).split(' ', 1)    # takes client request and breaks it down do matching                                                     
    operation_info = ""                                 # parameters for readability

    if len(splitted_request) == 2:
        operation_num = int(splitted_request[0])
        operation_info = splitted_request[1]
    else:
        operation_num = int(splitted_request[0])

    if operation_num == 1:                                # in this case operation_info = name
        if operation_info in logged_users:
            sock.sendto(b'Illegal request', (address[0], address[1]))
        else:
            inform_new_client(logged_users, sock, address)
            logged_users.insert(0, operation_info)              # inseart to the beggining of the list
            details[operation_info] = address                   # save client info the current members list:
            waiting_updates[operation_info] = list()            # Create a new record for future messages:
            update_members(operation_num, operation_info, waiting_updates, operation_info)

    elif operation_num == 2:                                # in this case operation_info = Message
        name = find_by_adress(address, details)
        if not check_if_registered(name):
            sock.sendto(b'Illegal request', (address[0], address[1]))
        else:
            update_members(operation_num, operation_info, waiting_updates, name)
            sock.sendto(b'', (address[0], address[1]))

    elif operation_num == 3:                                # in this case operation_info = New Name
        current_name = find_by_adress(address, details)
        if not check_if_registered(current_name):
            sock.sendto(b'Illegal request', (address[0], address[1]))
        else:
            change_name(waiting_updates, details, current_name, operation_info, logged_users)
            print(logged_users)
            update_members(operation_num, current_name, waiting_updates, operation_info)
            sock.sendto(b'', (address[0], address[1]))
    
    elif operation_num == 4:                                # in this case we dont have operation info
        to_remove_name = find_by_adress(address, details)
        if not check_if_registered(to_remove_name):
            sock.sendto(b'Illegal request', (address[0], address[1]))
        else:
            del details[to_remove_name]
            del waiting_updates[to_remove_name]
            logged_users.remove(to_remove_name)

            update_members(operation_num, operation_info, waiting_updates, to_remove_name)
            sock.sendto(b'', (address[0], address[1]))

    elif operation_num == 5:                                # in this case we dont have operation info
        name = find_by_adress(address, details)
        if not check_if_registered(name):
            sock.sendto(b'Illegal request', (address[0], address[1]))
        else:
            sock.sendto('\n'.join(waiting_updates[name]).encode(), (address[0], address[1]))
            waiting_updates[name] = list()                  # initialize his list to an empty one


def main():

    details = dict()                                # contains mapping {name -> (client_ip, client_port)}
    waiting_updates = dict()                        # contains mapping {name -> [waiting_updates]}
    logged_users = []

    if not(validate_args(sys.argv)):
        exit()

    my_port = int(sys.argv[1])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', my_port))

    while True:
        request, address = s.recvfrom(1024)
        if not(validate_request(request)):
            s.sendto(b'Illegal request', (address[0], address[1]))
        else:
            handle_client_request(request, address, details,
                                  waiting_updates, s, logged_users)


if __name__ == "__main__":
    main()