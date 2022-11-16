import socket
import sys
ERROR_MSG = "Illegal request"


"""
    Validate the port's number
"""
def validate_args():
    if not(sys.argv[1].isnumeric()):
        return False
    if int(sys.argv[1]) in range(1, 65536):
        return True
    else:
        return False


"""
    Validate the request of the client
"""
def validate_request(request):

    # Parse the request of the client
    splitted_request = bytes.decode(request).split(' ', 1)
    if not(splitted_request[0].isdigit()):
        return False
    if len(splitted_request) == 2:
        if not(int(splitted_request[0]) in range(1, 4)):
            return False
        else:
            return True
    elif len(splitted_request) == 1:
        if not(int(splitted_request[0]) in range(4, 6)):
            return False
        else:
            return True
    else:
        return False


"""
    Check if the current client is already registered to the group
"""
def check_if_registered(name, logged_users):
    if name in logged_users:
        return True
    else:
        return False


"""
    Generate list of current members and sends it immediately
    to the new client.
"""
def inform_new_client(logged_users, sock, client_address):
    if len(logged_users) != 0:                       
        sock.sendto(', '.join(logged_users).encode(), (client_address[0], client_address[1]))
    else:
        sock.sendto(b'', (client_address[0], client_address[1]))
    

"""
    Return client name by his socket address
"""
def find_by_adress(client_address, clients_details):
    client_name = [key for key in clients_details.keys() if (clients_details[key] == client_address)]

    # In case the client is not registered
    if len(client_name) == 0:
        return None
    return client_name[0]


"""
    Change client name from the current name to the new one
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

    if operation_num == 1:

        # in this case operation_info = name
        message = operation_info + " has joined"
    elif operation_num == 2:

        # in this case operation_info = Message
        message = client_name + ": " +  operation_info
    elif operation_num == 3:

        # in this case operation_info = New Name
        message = operation_info + " changed his name to " + client_name
    elif operation_num == 4:

        # in this case operation_info = ""
        message = client_name + " has left the group"
    else:
        message = ERROR_MSG

    for client in waiting_updates:

        # iterate through all clients and add the message to their waiting updates
        if client != client_name and message != ERROR_MSG:
            waiting_updates[client].append(message)


"""
    Push the messages that are waiting for the current client 
"""
def push_messages(waiting_updates, name, address, sock):
    messages = waiting_updates[name]
    if len(messages) != 0:
        sock.sendto('\n'.join(waiting_updates[name]).encode(), (address[0], address[1]))

        # initialize his list to an empty one
        waiting_updates[name] = list()
    else:
        sock.sendto(b'', (address[0], address[1]))
        

"""
    Delete the client from the local DB of the group
"""
def delete_user(details, waiting_updates, to_remove_name, logged_users):
    del details[to_remove_name]
    del waiting_updates[to_remove_name]
    logged_users.remove(to_remove_name)


"""
    Add the new client to the local DB of the group
"""
def save_client(operation_info, address, waiting_updates, details, logged_users):

    # inseart to the beggining of the list
    logged_users.insert(0, operation_info)

    # save client info the current members list:
    details[operation_info] = address

    # Create a new record for future messages:
    waiting_updates[operation_info] = list()


"""
    Handles the client request based on the operation number.
"""
def handle_client_request(request, address, details,
                          waiting_updates, sock, logged_users):

    # Parse the request of the client
    splitted_request = bytes.decode(request).split(' ', 1)
    operation_info = ""

    if len(splitted_request) == 2:
        operation_num = int(splitted_request[0])
        operation_info = splitted_request[1]
    else:
        operation_num = int(splitted_request[0])

    if operation_num == 1:

        # in this case operation_info = name
        if operation_info in logged_users:
            sock.sendto(b'Illegal request', (address[0], address[1]))
        else:
            inform_new_client(logged_users, sock, address)
            save_client(operation_info, address, waiting_updates, details, logged_users)
            update_members(operation_num, operation_info, waiting_updates, operation_info)

    elif operation_num == 2:

        # in this case operation_info = Message
        name = find_by_adress(address, details)
        if not check_if_registered(name, logged_users):
            sock.sendto(b'Illegal request', (address[0], address[1]))
        else:
            update_members(operation_num, operation_info, waiting_updates, name)
            push_messages(waiting_updates, name, address, sock)

    elif operation_num == 3:

        # in this case operation_info = New Name
        current_name = find_by_adress(address, details)
        if not check_if_registered(current_name, logged_users):
            sock.sendto(b'Illegal request', (address[0], address[1]))
        else:
            change_name(waiting_updates, details, current_name, operation_info, logged_users)
            update_members(operation_num, current_name, waiting_updates, operation_info)
            push_messages(waiting_updates, operation_info, address, sock)
    
    elif operation_num == 4:

        # in this case we dont have operation info
        to_remove_name = find_by_adress(address, details)
        if not check_if_registered(to_remove_name, logged_users):
            sock.sendto(b'Illegal request', (address[0], address[1]))
        else:
            delete_user(details, waiting_updates, to_remove_name, logged_users)
            update_members(operation_num, operation_info, waiting_updates, to_remove_name)
            sock.sendto(b'', (address[0], address[1]))

    elif operation_num == 5:

        # in this case we dont have operation info
        name = find_by_adress(address, details)
        if not check_if_registered(name, logged_users):
            sock.sendto(b'Illegal request', (address[0], address[1]))
        else:
            push_messages(waiting_updates, name, address, sock)


def main():

    # contains mapping {name -> (client_ip, client_port)}
    details = dict()

    # contains mapping {name -> [waiting_updates]}
    waiting_updates = dict()

    # contains a list of the registered members of the group
    logged_users = []

    # In case the port's number is invalid
    if not(validate_args()):
        exit()
    my_port = int(sys.argv[1])

    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to a port
    s.bind(('', my_port))

    # The server gets requests from the clients
    while True:
        request, address = s.recvfrom(1024)

        # Check if the request of the client is valid
        if not(validate_request(request)):
            s.sendto(b'Illegal request', (address[0], address[1]))
        else:
            handle_client_request(request, address, details,
                                  waiting_updates, s, logged_users)


if __name__ == "__main__":
    main()