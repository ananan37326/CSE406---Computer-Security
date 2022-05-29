from S1705053_AES import *
from S1705053_RSA import *
import time, os, sys
from S1705053_Helper import *

# PERFORM TIME TEST
def time_test(func, *args):
    start = time.perf_counter()
    returned_val = func(*args)
    end = time.perf_counter()
    return end - start, returned_val

# FUNCTION TO STORE TIME TEST RESULTS
def write_to_file(file,data):
    with open(file, 'a', encoding="utf-8") as f:
        f.write(data)



# PERFORM AES ENCRYPTION TIME TEST
def aes_time_test(plaintext,key):
    aes = AES(key)

    # PLAINTEXT
    plaintexts = pad_text(plaintext)

    plaintext = ""
    for i in plaintexts:
        plaintext += i

    plaintext_hex = get_hex_matrix(plaintext)
    plaintext_hex = get_string_from_list(plaintext_hex)

    # KEY
    key_hex = pad_or_trim(key)
    key_hex = get_hex_list(key_hex)
    key_hex = get_string_from_list(key_hex)

    # KEY EXPANSION
    key_expansion_time,_ = time_test(aes.key_expansion)

    # ENCRYPTION
    encryption_time, ciphertuple = time_test(aes.encrypt, plaintext)
    cipher_hex = ciphertuple[0]
    cipher_ascii = ciphertuple[1]

    # DECRYPTION
    decryption_time, deciphertuple = time_test(aes.decrypt, cipher_ascii)
    decipher_hex = deciphertuple[0]
    decipher_ascii = deciphertuple[1]

    # WRITE TO FILE
    file_str = "Plain Text:\n"
    file_str += plaintext + "  [ In ASCII ]" + "\n"
    file_str += plaintext_hex + "  [ In HEX ]" + "\n\n"

    file_str += "Key:\n"
    file_str += key + "  [ In ASCII ]" + "\n"
    file_str += key_hex + "  [ In HEX ]" + "\n\n"

    file_str += "Cipher Text:\n"
    file_str += cipher_hex + "  [ In HEX ]" + "\n"
    file_str += cipher_ascii + "  [ In ASCII ]" + "\n\n"

    file_str += "Deciphered Text:\n"
    file_str += decipher_hex + "  [ In HEX ]" + "\n"
    file_str += decipher_ascii + "  [ In ASCII ]" + "\n\n"

    file_str += "Execution Time:\n"
    file_str += "Key Scheduling: " + str(key_expansion_time) + " seconds" + "\n"
    file_str += "Encryption Time: " + str(encryption_time) + " seconds" + "\n"
    file_str += "Decryption Time: " + str(decryption_time) + " seconds" + "\n\n"

    write_to_file("../AES_Time_Test.txt",str(file_str))

    print("AES")
    print("Plain Text: " + plaintext)
    print("Deciphered Text: " + decipher_ascii)
    if plaintext == decipher_ascii:
        print("MATCH FOUND!")
    else:
        print("MISMATCH FOUND!")


# PERFORM AES TIME TEST FOR FILE
def aes_file_time_test(file,key):
    aes = AES(key)

    # PLAINTEXT
    plaintext_hex = get_hex_matrix(file)
    plaintext_hex = get_string_from_list(plaintext_hex)

    # KEY
    key_hex = pad_or_trim(key)
    key_hex = get_hex_matrix(key_hex)
    key_hex = get_string_from_list(key_hex)

    # KEY EXPANSION
    key_expansion_time, _ = time_test(aes.key_expansion)

    # ENCRYPTION
    encryption_time, ciphertuple = time_test(aes.encrypt, file)
    cipher_hex = ciphertuple[0]
    cipher_ascii = ciphertuple[1]

    # DECRYPTION
    decryption_time, deciphertuple = time_test(aes.decrypt, cipher_ascii)
    decipher_hex = deciphertuple[0]
    decipher_ascii = deciphertuple[1]

    # WRITE TO FILE
    file_str = "Plain Text:\n"
    file_str += file + "  [ In ASCII ]" + "\n"
    file_str += plaintext_hex + "  [ In HEX ]" + "\n\n"

    file_str += "Key:\n"
    file_str += key + "  [ In ASCII ]" + "\n"
    file_str += key_hex + "  [ In HEX ]" + "\n\n"

    file_str += "Cipher Text:\n"
    file_str += cipher_hex + "  [ In HEX ]" + "\n"
    file_str += cipher_ascii + "  [ In ASCII ]" + "\n\n"

    file_str += "Deciphered Text:\n"
    file_str += decipher_hex + "  [ In HEX ]" + "\n"
    file_str += decipher_ascii + "  [ In ASCII ]" + "\n\n"

    file_str += "Execution Time:\n"
    file_str += "Key Scheduling: " + str(key_expansion_time) + " seconds" + "\n"
    file_str += "Encryption Time: " + str(encryption_time) + " seconds" + "\n"
    file_str += "Decryption Time: " + str(decryption_time) + " seconds" + "\n\n"

    write_to_file("../AES_FILE_Time_Test.txt", str(file_str))

    plain_ascii = decipher_ascii.rstrip()

    bv_plain = BitVector(textstring=plain_ascii)


    print("AES")
    print("Plain Text: " + file)
    print("Deciphered Text: " + decipher_ascii)
    if file == decipher_ascii:
        print("MATCH FOUND!")
    else:
        print("MISMATCH FOUND!")

    return bv_plain

# PERFORM RSA ENCRYPTION TIME TEST
def rsa_time_test(plaintext,keysize):
    rsa = RSA(keysize)

    # KEY GENERATION
    key_generation_time, keys = time_test(rsa.generateKeys)
    public_key = keys['public']
    private_key = keys['private']
    e_val = public_key[0]
    n_val = public_key[1]
    d_val = private_key[0]

    # ENCRYPTION
    encryption_time, ciphertext = time_test(rsa.encrypt, plaintext, e_val, n_val)

    # DECRYPTION
    decryption_time, decipheredtext = time_test(rsa.decrypt, ciphertext, d_val, n_val)

    # WRITE TO FILE
    file_str = str(keysize) + "," + str(key_generation_time) + "," + str(encryption_time) + "," + str(decryption_time) + "\n"
    write_to_file("../RSA_Time_Test.csv",str(file_str))

    print("RSA - K : " + str(keysize))
    print("Plain Text: " + plaintext)
    print("Deciphered Text: " + decipheredtext)
    if plaintext == decipheredtext:
        print("MATCH FOUND!")
    else:
        print("MISMATCH FOUND!")


# Text or FILE
choice = input("Enter 1 for text or 2 for file: ")
#choice = "1"


# TEXT AND KEY
#text = "ThisIsAPlainText" # hardcoded text
#key = "encryptionkey" # hardcoded key



# INITIAL FILE CLEANING
if os.path.exists("../AES_Time_Test.txt"):
    os.remove("../AES_Time_Test.txt")
if os.path.exists("../RSA_Time_Test.csv"):
    os.remove("../RSA_Time_Test.csv")



if choice == "1":
    # TEST AES
    text = input("Enter the text: ")
    key = input("Enter the key ( FOR AES ONLY ): ")
    #print(text)
    aes_time_test(text,key)
    # TEST RSA
    # text = "CanTheyDoTheirFest"
    rsa_keys = [16, 32, 64, 128, 256]
    file_str = "K,Key-Generation,Encryption,Decryption\n"
    if "RSA_Time_Test.csv" in os.listdir("../."):
        os.remove("../RSA_Time_Test.csv")
    write_to_file("../RSA_Time_Test.csv", str(file_str))
    for key in rsa_keys:
        rsa_time_test(text, key)
else:
    file_path = input("Enter the file path: ")
    key = input("Enter the key ( FOR AES ONLY ): ")
    filename, file_extension = os.path.splitext(file_path)
    file_data = read_file(file_path)

    deciphered_bv = aes_file_time_test(file_data, key)
    write_file("../deciphered"+str(file_extension), deciphered_bv)




