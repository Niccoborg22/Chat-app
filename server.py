import tkinter as tk
import socket
import threading 

# define constants
LISTENER_LIMIT = 5 # number of clients that can connect to server
active_clients = [] # list to store active clients


# function to listen for messages from clients
def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_message = username + "~" + message
            send_messages_to_all(final_message)
        else:
            print(f"Message from {username} empty")

# function to send messages to all connected clients
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)        

# function to send message to client        
def send_message_to_client(client, message):
    client.sendall(message.encode('utf-8'))

# Function to handle client connection
def client_handler(client):
    # server will listen for client message that contain username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            break
        else:
            print("Username is empty")
    threading.Thread(target=listen_for_messages, args=(client, username)).start()

# Main function for server
def main(server_ip, port):
    #AF_INET: states we will use IPv4 ip address
    #SOCK_STREAM: states we will be using tcp packets for data transfer
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # creating a try catch block
    try:
        # provide the server with an address in the form of host IP and port 
        server.bind((server_ip, port))
        print(f"Running server on {server_ip} {port}")
    except:
        print(f"""Unable to bind to host {server_ip} and port {port} """)
    # Setting the server limit
    server.listen(LISTENER_LIMIT)
    # keeps server listening to client connection with while loop
    while 1:
        client, address = server.accept()
        print(f"Successfully Connected to Client {address[0]} {address[1]}")
        threading.Thread(target=client_handler, args=(client, )).start()

# function to retrieve user inputs and start server
def start_server():
    server_ip = server_ip_entry.get()
    port = int(port_entry.get())
    threading.Thread(target=main, args=(server_ip, port)).start()


# create tkinter GUI
root = tk.Tk()
root.geometry("400x200")
root.title("Server Configuration")

# create widgets for server IP address and port number input
server_ip_label = tk.Label(root, text="Server IP Address:")
server_ip_entry = tk.Entry(root, width=30)
port_label = tk.Label(root, text="Port Number:")
port_entry = tk.Entry(root, width=10)

# create submit button
submit_button = tk.Button(root, text="Start Server", command=start_server)


# layout widgets using grid
server_ip_label.grid(row=0, column=0, padx=10, pady=10)
server_ip_entry.grid(row=0, column=1, padx=10, pady=10)
port_label.grid(row=1, column=0, padx=10, pady=10)
port_entry.grid(row=1, column=1, padx=10, pady=10)
submit_button.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()