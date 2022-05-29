import json
import time, socket, sys, os
from S1705053_AES import *
from S1705053_RSA import *


# establish connection
def connect_to_sender():
    sock = socket.socket()
    s_host = socket.gethostname()
    ip = socket.gethostbyname(s_host)
    host = ip
    port = 1234
    print("Trying to connect to ", host, ":", port)
    time.sleep(1)
    sock.connect((host, port))
    print("Connected to ", host, ":", port)
    return sock


# get the private key from the key.txt file
def get_private_key(folder):
    with open(folder + "/key.txt", "r") as f:
        private_key = f.readlines()
        d_val = int(private_key[0].strip())
        n_val = int(private_key[1].strip())
    return d_val, n_val


# poll the directory and find the key.txt file
def poll_directory(folder):
    try:
        print("Polling directory for files...")
        while True:
            # code to find the latest file
            files = os.listdir(folder)
            if "key.txt" in files:
                print("key.txt found")
                return get_private_key(folder)
                break

            time.sleep(5)
    except KeyboardInterrupt:
        print("Quitting the program.")
    except:
        print("Unexpected error: ", sys.exc_info()[0])
        raise


# write the deciphered message to the file
def write_to_file(file_name, data):
    with open(file_name, "w") as f:
        f.write(data)


# FOLDER AND FILEPATH
private_folder = "../DONOTOPEN"
dpt_filepath = "../DONOTOPEN/dpt.txt"

# INITIAL CLEANING
if "dpt.txt" in os.listdir(private_folder):
    os.remove(dpt_filepath)

# START HERE
print("Receiver : Bob")
time.sleep(1)

# CONNECT TO SENDER
sock = connect_to_sender()

# RECEIVE THE CHOICE
choice = sock.recv(1024).decode()

# RECEIVE THE INITIAL MESSAGE
# data_received = ""
# while True:
#     data = sock.recv(1024)
#     if not data:
#         break
#     data_received += data.decode()

data = sock.recv(1024).decode()

# PARSE THE INITIAL MESSAGE
json_data = json.loads(data)
ciphertext = json_data["CT"]
encrypted_key = json_data["EK"]
public_key = json_data["PUK"]

# POLL THE FOLDER FOR PRIVATE KEY
d_val, n_val = poll_directory(private_folder)
print("Private key : ", d_val, " ", n_val)

# DECRYPT THE ENCRYPTED KEY WITH RSA
rsa = RSA()
decrypted_key = rsa.decrypt(encrypted_key, d_val, n_val)

# DECRYPT THE CIPHERTEXT WITH AES
aes = AES(key=decrypted_key)
aes.key_expansion()
_,plaintext = aes.decrypt(ciphertext)

if choice == "2":
    # WRITE THE BYTES TO FILE
    plaintext = plaintext.strip()
    bv_plain = BitVector(textstring=plaintext)
    outpath = "../deciphered-file"
    write_file(outpath,bv_plain)


# WRITE THE PLAINTEXT TO A FILE
write_to_file("../DONOTOPEN/dpt.txt", plaintext)
print("dpt.txt updated.")

# SEND THE ACKNOWLEDGEMENT TO THE SENDER
message = input("SEND OK > ")
sock.send(message.encode())
print("Acknowledgement sent. Closing the connection.")

# CLOSING THE CONNECTION
sock.close()


