from MillerRabin import *
from OLD.RSA import *
from BitVector import *

print("Miller-Rabin Primality Test")
mr = MillerRabin()
print(mr.generate_prime_duo(bits=8))

bv1 = BitVector(intVal=45097)
bv2 = BitVector(intVal=2571216841)
bv3 = bv1.multiplicative_inverse(bv2)
print(bv3.intValue())

rsa = RSA(keysize=16)
print(rsa.generateKeys())
s = "Hello World"
print(s)
print(rsa.encrypt(s))
print(rsa.decrypt(rsa.encrypt(s)))

