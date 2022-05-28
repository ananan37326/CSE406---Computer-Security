import random


# A class to generate large prime numbers using the Miller-Rabin Primality Test

class MillerRabin:
    def __init__(self):
        self.p = 0
        self.q = 0

    # Generate a random prime number of size n bits
    def generate_number(self, bits):
        num = random.getrandbits(bits)

        num |= (1 << bits - 1) | 1

        return num

    # Primality test using the Miller-Rabin Primality Test
    def is_prime(self, number, iterations=20):
        if number == 2 or number == 3:
            return True

        if number <= 1 or number % 2 == 0:
            return False

        r, s = 0, number - 1
        while s % 2 == 0:
            r += 1
            s //= 2
        for _ in range(iterations):
            a = random.randrange(2, number - 1)
            x = pow(a, s, number)
            if x == 1 or x == number - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, number)
                if x == number - 1:
                    break
            else:
                return False
        return True

    # Generate a large prime number of size n bits
    def generate_prime(self, bits):
        p = 4
        while not self.is_prime(p, 20):
            p = self.generate_number(bits)
        return p

    # Generate two large prime numbers of size n bits
    def generate_prime_duo(self, bits):
        p = self.generate_prime(bits)
        q = self.generate_prime(bits)
        while p == q:
            q = self.generate_prime(bits)

        return p, q
