import socket
import threading 
import tkinter as tk
from tkinter import scrolledtext, messagebox
import customtkinter


HOST = '172.20.10.9'
PORT = 1234


DARK_BLUE = "#0A0E3F"
MEDIUM_BLUE = "#0D47A1"
LIGHT_BLUE = "#1565C0"
WHITE = "white"
FONT = ("Arial", 16)
BUTTON_FONT = ("Arial", 14)
SMALL_FONT = ("Arial", 12)
BLACK = "black"

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

    #creating a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
        # connecting to server
  
    try:
        client.connect((HOST, PORT))
        add_message(f"Client successfully connected to server {HOST}")
    except:
        message_box.showerror("Unable to connect to server", f"unable to connect to server {HOST} {PORT}")
    
        
    username = username_textbox.get()
    if username != ' ':
        client.sendall(username.encode())
    else: 
        message_box.showerror('Invalid Username', 'Username can not be empty')
  
        
    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
    
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)
    
def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
    else:
        message_box.showerror('Invalid Message', 'Message can not be empty')
    
    
    
    
    
root = customtkinter.CTk()
root.geometry("600x600")
root.title("Chat App")
root.resizable(False, False)


root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

topFrame = customtkinter.CTkFrame(root, width=600, height= 100)
topFrame.grid(row = 0, column = 0, sticky = tk.NSEW)



middleFrame = customtkinter.CTkFrame(root, width=600, height= 400)
middleFrame.grid(row = 1, column = 0, sticky = tk.NSEW)


bottomFrame = customtkinter.CTkFrame(root, width= 600, height= 100)
bottomFrame.grid(row=2, column=0, sticky = tk.NSEW)

username_label = customtkinter.CTkLabel(topFrame, text="Username: ", font=FONT)
username_label.pack(side=tk.LEFT, padx=10, pady=10)

username_textbox = customtkinter.CTkEntry(topFrame, font=FONT, width=200)
username_textbox.pack(side=tk.LEFT, padx=10, pady=10)

username_button = customtkinter.CTkButton(topFrame, text="Enter", font=BUTTON_FONT, command=connect)
username_button.pack(side=tk.LEFT, padx=10, pady=10)

message_textbox = customtkinter.CTkEntry(bottomFrame, font=FONT, width=400)
message_textbox.pack(side=tk.LEFT, padx=10, pady=10)

message_button = customtkinter.CTkButton(bottomFrame, text="Send", font=BUTTON_FONT, command=send_message)
message_button.pack(side=tk.LEFT, padx=20, pady=10)

message_box = scrolledtext.ScrolledText(middleFrame, width=85, height=35, font=SMALL_FONT)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages_from_server(client):
    
    while 1: 
        
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split('~')[0]
            content = message.split('~')[1]
            
            add_message(f'{username}: {content}')
        else:
            message_box.showerror('Message recieved was empty','Message recieved was empty')
            
# def send_message_to_server(client):
    
#     while 1:
#         message = input('Message: ')
#         if message != '':
#             client.sendall(message.encode())
#         else:
#             print('Message can not be empty')
#             exit(0)
            
            
# function to communicate to server

# def communicate_to_server(client):
    
#     username = input("Enter username: ")
#     if username != ' ':
#         client.sendall(username.encode())
#     else: 
#         print('Username can not be empty')
#         exit(0)
        
#     threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
    
#     send_message_to_server(client)

def main():
    
    root.mainloop()

    # # connecting to server
  
    # try:
    #     client.connect((HOST, PORT))
    #     print("Client successfully connected to server")
    # except:
    #     print(f"unable to connect to server {HOST} {PORT}")
    
    # communicate_to_server(client)
    
if __name__ == '__main__':
    main()