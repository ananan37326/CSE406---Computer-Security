# a class to implement RSA encryption and decryption
#

from BitVector import *

from S1705053_MillerRabin import *


# A class to implement RSA encryption and decryption
class RSA:
    def __init__(self, keysize = 32):
        self.keysize = keysize
        self.mr = MillerRabin()
        self.public_key = 0
        self.private_key = 0
        self.n = 0
        self.phi = 0

    # check if two numbers are coprime
    def is_coprime(self, a, b):
        bv_a = BitVector(intVal = a)
        bv_b = BitVector(intVal = b)
        bv_gcd = bv_a.gcd(bv_b)
        if bv_gcd.int_val() == 1:
            return True
        else:
            return False

    # generate a random prime number of keysize/2 bits
    def generate_e(self,phi):
        #e = 45097
        e = self.mr.generate_prime(self.keysize//2)
        while not self.is_coprime(e, phi):
            e = self.mr.generate_prime(self.keysize//2)
        return e

    # get the multiplicative inverse of a number Extended Euclidean Algorithm
    def get_multiplicative_inverse(self,e,phi):
        d, new_d, r, new_r = 0, 1, phi, e

        while new_r != 0:
            q = r // new_r
            d, new_d = new_d, d - q * new_d
            r, new_r = new_r, r - q * new_r

        if r > 1:
            return None
        if d < 0:
            d += phi
        return d

    # Generate a public and private key pair
    def generateKeys(self):
        p, q = self.mr.generate_prime_duo(self.keysize // 2)
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        #self.phi = 2571216841
        self.public_key = self.generate_e(self.phi)
        self.private_key = self.get_multiplicative_inverse(self.public_key, self.phi)

        #self.public_key = 45097
        #self.private_key = 2123962321

        #return (n, e, d)
        pub_tuple = (self.public_key, self.n)
        pri_tuple = (self.private_key, self.n)
        keys = {
            "public": pub_tuple,
            "private": pri_tuple
        }
        return keys


    # RSA encryption
    def encrypt(self, plaintext,public_key,n):
        ciphertext = []
        for i in plaintext:
            ciphertext.append(pow(ord(i), public_key, n))

        return ciphertext

    # RSA decryption
    def decrypt(self,ciphertext,private_key,n):
        p = ""
        for i in range(len(ciphertext)):
            res = pow(ciphertext[i], private_key, n)
            p += chr(res)


        return p




