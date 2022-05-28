from RSA import *
from BitVector import *
from AES import *

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
aes = AES(key=st)
cipher,ascii_cipher = aes.encrypt(plaintext)
plain, ascii_plain = aes.decrypt(ascii_cipher)



