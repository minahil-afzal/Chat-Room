import threading
import socket
from tkinter import *
from tkinter import scrolledtext, messagebox

# Set up the client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

nickname = None
chat_text = None

# Function to prompt for a nickname through a popup
def ask_nickname():
    def submit_nickname():
        global nickname
        nickname = nickname_entry.get()
        if nickname:
            nickname_window.destroy()  # Close the nickname window
            root.title(f"Chat Room - {nickname}")
            root.geometry("500x500")
            chat_window()  # Open the chat window after the nickname is set

            # Start a thread to receive messages
            receive_thread = threading.Thread(target=receive_message, daemon=True)
            receive_thread.start()
        else:
            messagebox.showwarning("Nickname Required", "Please enter a valid nickname.")

    # Create the nickname window
    nickname_window = Toplevel(root)
    nickname_window.title("Enter Nickname")
    nickname_window.geometry("300x150")
    nickname_window.configure(bg="#F9F9F9")

    nickname_label = Label(nickname_window, text="Choose a nickname:", font=("Arial", 12), bg="#F9F9F9", fg="#333333")
    nickname_label.pack(pady=10)

    nickname_entry = Entry(nickname_window, font=("Arial", 12), bg="#E8F0FE", fg="#333333", insertbackground="#333333")
    nickname_entry.pack(pady=5)

    submit_button = Button(nickname_window, text="Submit", font=("Arial", 12), bg="#B3D4FC", fg="#333333", command=submit_nickname)
    submit_button.pack(pady=10)

# Function to create the chat window
def chat_window():
    global chat_text, input_field
    # Chat text area with light blue background and dark text
    chat_text = scrolledtext.ScrolledText(root, font=("Arial", 12), bg="#F0F8FF", fg="#333333", wrap=WORD, state=DISABLED)
    chat_text.pack(pady=10, padx=10, fill=BOTH, expand=True)

    # Input frame with a light blue background
    input_frame = Frame(root, bg="#E6F7FF")
    input_frame.pack(fill=X, pady=5)

    # Input field with light gray background and dark text
    input_field = Entry(input_frame, font=("Arial", 14), bg="#F5F5F5", fg="#333333", insertbackground="#333333")
    input_field.pack(side=LEFT, padx=10, pady=5, fill=X, expand=True)

    # Send button with light blue color
    send_button = Button(input_frame, text="Send", font=("Arial", 12), bg="#A7C7E7", fg="#333333", command=send_message)
    send_button.pack(side=RIGHT, padx=10, pady=5)

    # Footer with acknowledgment
    footer_label = Label(root, text="TCP Chat Room - Developed by You", bg="#E6F7FF", fg="#333333", font=("Arial", 10))
    footer_label.pack(pady=10)

# Function to receive messages from the server
def receive_message():
    chat_text.config(state=NORMAL)
    chat_text.insert(END, "Connected to the server!\n")
    chat_text.config(state=DISABLED)

    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(f"Received message: {message}")

            if message == 'NAME':
                client.send(nickname.encode('ascii'))
            else:
                root.after(0, update_chat_text, message)

        except Exception as e:
            print(f"Error in receiving message: {e}")
            messagebox.showerror("Error", "An error occurred! Connection lost.")
            client.close()
            break

# Function to update the chat text area
def update_chat_text(message):
    chat_text.config(state=NORMAL)
    chat_text.insert(END, f"{message}\n")
    chat_text.config(state=DISABLED)
    chat_text.see(END)

# Function to send a message to the server
def send_message():
    message = f"{nickname}: {input_field.get()}"
    if input_field.get().strip():  # Ensure the input is not empty
        client.send(message.encode('ascii'))
        input_field.delete(0, END)

# Tkinter root window setup
root = Tk()
root.title("Chat Room")
root.geometry("300x150")
root.resizable(False, False)
root.configure(bg="#FFFFFF")  # White background for main window

ask_nickname()  # Start with nickname prompt

root.mainloop()
