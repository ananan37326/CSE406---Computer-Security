import os
import time, socket, sys, json
from S1705053_AES import *
from S1705053_RSA import *


# Get the plaintext and aes key from a file
def get_text_info(file):
    with open(file, 'r') as f:
        lines = f.readlines()

        plaintext = lines[0].strip()
        aes_key = lines[1].strip()

        return plaintext, aes_key


# store the private RSA key in a file
def store_key(folder,key):
    with open(folder+"/key.txt", 'w') as f:
        f.write(str(key[0]))
        f.write("\n")
        f.write(str(key[1]))


# get the deciphered text from a file
def get_DPT(folder):
    with open(folder + "/dpt.txt", "r") as f:
        deciphered_plaintext = f.read()
        return deciphered_plaintext


# Poll the directory and find the dpt.txt file
def poll_directory(folder):
    try:
        print("Polling directory for files...")
        while True:
            # code to find the latest file
            files = os.listdir(folder)
            if "dpt.txt" in files:
                print("dpt.txt found")
                return get_DPT(folder)
                break

            time.sleep(5)
    except KeyboardInterrupt:
        print("Quitting the program.")
    except:
        print("Unexpected error: ", sys.exc_info()[0])
        raise


# apply the algorithms and return the ciphertext and the encrypted key along with the RSA keys
def prepare_text_data(plaintext,aes_key):
    aes = AES(aes_key)
    rsa = RSA()
    keys = rsa.generateKeys()
    public_key = keys['public']
    private_key = keys['private']
    aes.key_expansion()
    _, ciphertext = aes.encrypt(plaintext)
    encrypted_key = rsa.encrypt(aes_key,public_key[0],public_key[1])

    return ciphertext, encrypted_key, public_key, private_key


# make json object of the data
def make_json_object(ciphertext, encrypted_key, public_key):
    json_object = {
        "CT": ciphertext,
        "EK": encrypted_key,
        "PUK": public_key
    }
    return json.dumps(json_object)


# set up the TCP connection
def set_up_connection():
    sock = socket.socket()
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    port = 1234
    sock.bind((host, port))
    print("Sender : Alice is listening on %s:%s" % (ip, port))

    sock.listen(1)
    print("Awaiting connection...")
    conn, addr = sock.accept()
    print("Sender : Alice has connected to %s:%s" % (addr[0], addr[1]))
    return conn




# hardcoded data
plaintext = "CanTheyDoTheirFest"
aes_key = "BUET CSE17 Batch"

# SET THE FOLDER AND FILE PATH
file_path = "../data.txt"
folder_path = "../DONOTOPEN"

# INITIAL FILE SETUP
files = os.listdir(folder_path)
if "key.txt" in files:
    os.remove(folder_path+"/key.txt")


# START HERE
print("Sender : Alice")
time.sleep(1)

# TEXT or FILE
choice = input("Press 1 for text and 2 for file: ")

if choice == "1":
    # GET THE PLAINTEXT AND AES KEY FROM THE FILE
    plaintext, aes_key = get_text_info(file_path)
else :
    path,aes_key = get_text_info(file_path)
    plaintext = read_file(path)
    filename, file_extension = os.path.splitext(path)



# SET UP THE CONNECTION
conn = set_up_connection()

# PREPARE THE DATA
ciphertext, encrypted_key, public_key, private_key = prepare_text_data(plaintext,aes_key)



# MAKE THE JSON OBJECT
json_object = make_json_object(ciphertext, encrypted_key, public_key)

# STORE THE PRIVATE KEY
store_key(folder_path,private_key)

# SEND THE CHOICE TO THE RECEIVER
conn.send(choice.encode())

# SEND THE JSON DATA
conn.send(json_object.encode())


# GET RESPONSE FROM THE RECEIVER
data = conn.recv(1024)
received_data = data.decode()
if received_data == "OK":
    print("Acknowledgement received. Closing the connection.")

conn.close()

# POLL THE DIRECTORY
if choice == "1":
    dpt = poll_directory(folder_path)
    print("Original plaintext: ", plaintext)
    print("Received deciphered text: ", dpt)
    if dpt == plaintext:
        print("The plaintext has been successfully decrypted.")
    else:
        print("The plaintext could not be decrypted.")


