from S1705053_Helper import *
from S1705053_bitvectordemo import *
from S1705053_AES import *
from S1705053_RSA import *

# read a file and return the bytedata
def read_file(file):
    with open(file, 'rb') as f:
        data = f.read()
        return BitVector(rawbytes = data).get_text_from_bitvector()

data = read_file('../a.png')

#convert the bytedata to bitvector


aes = AES(key='0123456789abcdef0123456789abcdef')

aes.key_expansion()
cipher_hex, cipher_ascii = aes.encrypt(bv_data)

plain_hex, plain_ascii = aes.decrypt(cipher_ascii)

plain_ascii = plain_ascii.rstrip()

bv_plain = BitVector(textstring = plain_ascii)
print(bv_plain)

with open('../b.png', 'wb') as f:
    bv_plain.write_to_file(f)


print(len(bv_data))
print(bv_data)