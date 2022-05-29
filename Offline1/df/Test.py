from S1705053_RSA import *
from BitVector import *
from S1705053_AES import *

# print("Miller-Rabin Primality Test")
# mr = MillerRabin()
# print(mr.generate_prime_duo(bits=8))
#
# bv1 = BitVector(intVal=45097)
# bv2 = BitVector(intVal=2571216841)
# bv3 = bv1.multiplicative_inverse(bv2)
# print(bv3.intValue())
#
# rsa = RSA(keysize=256)
# print(rsa.generateKeys())
# s = "CanTheyDoTheirFest?"
# print(s)
# print(rsa.encrypt(s))
# print(rsa.decrypt(rsa.encrypt(s)))

st = "BUET CSE17 Batch"
plaintext = "CanTheyDoTheirFest"
# aes = AES(key=st)
# cipher,ascii_cipher = aes.encrypt(plaintext)
# plain, ascii_plain = aes.decrypt(ascii_cipher)

from S1705053_Sender import prepare_data
ciphertext, encrypted_key, public_key, private_key = prepare_data(plaintext, st)
rsa = RSA()
print(private_key)
key = rsa.decrypt(encrypted_key, private_key[0], private_key[1])
aes = AES(key=key)
plain, ascii_plain = aes.decrypt(ciphertext)
print(ascii_plain)




