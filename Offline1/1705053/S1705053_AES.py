from S1705053_bitvectordemo import *
from BitVector import *
from S1705053_Helper import *

# A class to implement AES encryption and decryption
class AES:
    def __init__(self, key):
        self.key = key
        self.length = 4
        self.width = 4
        self.rounds = 11
        self.round_keys = []
        # self.round_keys = self.key_expansion()

    # substitute bytes in the state matrix from SBOX
    def sub_bytes(self, matrix):
        s_matrix = []
        for i in range(len(matrix)):
            s_matrix.append(hex(Sbox[int(matrix[i], 16)])[2:])
        return s_matrix

    # substitute bytes in the state matrix from inverse SBOX
    def inv_sub_bytes(self, matrix):
        inv_s_matrix = []
        for i in range(len(matrix)):
            inv_s_matrix.append(hex(InvSbox[int(matrix[i], 16)])[2:])
        return inv_s_matrix

    # substitute bytes in the state matrix from SBOX 2D
    def sub_bytes_2d(self, matrix):
        s_matrix = []
        for i in range(len(matrix)):
            s_matrix.append(self.sub_bytes(matrix[i]))
        return s_matrix

    # substitute bytes in the state matrix from inverse SBOX 2D
    def inv_sub_bytes_2d(self, matrix):
        inv_s_matrix = []
        for i in range(len(matrix)):
            inv_s_matrix.append(self.inv_sub_bytes(matrix[i]))
        return inv_s_matrix

    # shift rows in the state matrix
    def shift_rows(self, matrix):
        matrix[1] = circular_rotate_left(matrix[1], 1)
        matrix[2] = circular_rotate_left(matrix[2], 2)
        matrix[3] = circular_rotate_left(matrix[3], 3)

        return matrix

    # inverse shift rows in the state matrix
    def inv_shift_rows(self, matrix):
        matrix[1] = circular_rotate_right(matrix[1], 1)
        matrix[2] = circular_rotate_right(matrix[2], 2)
        matrix[3] = circular_rotate_right(matrix[3], 3)

        return matrix

    # inverse mix columns in the state matrix
    def inv_mix_columns(self, matrix):
        return matrix_mul(InvMixer, hex_to_bitvector(matrix))

    # mix columns in the state matrix
    def mix_columns(self, matrix):
        return matrix_mul(Mixer, hex_to_bitvector(matrix))

    # add round key to the state matrix
    def add_round_key(self, mat1, mat2):
        return xor_2d(mat1, mat2)

    # get g(word)
    def get_g(self, word, i):
        temp = word.copy()
        g_word = circular_rotate_left(temp, 1)
        g_word = self.sub_bytes(g_word)
        g_word = add_round_constant(g_word, i - 1)

        return g_word

   # get all the round keys
    def get_round_keys(self, key_matrix):
        round_keys = [key_matrix]

        for i in range(1, self.rounds):
            w0 = round_keys[i - 1][0:4]
            w1 = round_keys[i - 1][4:8]
            w2 = round_keys[i - 1][8:12]
            w3 = round_keys[i - 1][12:16]

            gw3 = self.get_g(w3, i)

            new_w0 = hex_xor_word(w0, gw3)
            new_w1 = hex_xor_word(w1, new_w0)
            new_w2 = hex_xor_word(w2, new_w1)
            new_w3 = hex_xor_word(w3, new_w2)

            round_keys.append(new_w0 + new_w1 + new_w2 + new_w3)

        return round_keys

    # key scheduling
    def key_expansion(self):
        key = pad_or_trim(self.key)
        key_matrix = get_hex_matrix(key)
        self.round_keys = self.get_round_keys(key_matrix)
        return self.round_keys

    # AES encryption
    def encrypt(self, plaintext):
        # print(self.round_keys)

        #plaintext = plaintext.rstrip()
        plaintext_blocks = pad_text(plaintext)
        # print("Plaintext blocks: ", plaintext_blocks)

        full_ciphertext = ""
        full_asciitext = ""

        for block in plaintext_blocks:

            plaintext_matrix = get_hex_matrix(block)

            state_matrix = get_transposed_matrix(plaintext_matrix, self.length, self.width)
            round_matrix = get_transposed_matrix(self.round_keys[0], self.length, self.width)

            state_matrix = self.add_round_key(state_matrix, round_matrix)

            for i in range(1, self.rounds - 1):
                state_matrix = self.sub_bytes_2d(state_matrix)
                state_matrix = self.shift_rows(state_matrix)
                state_matrix = self.mix_columns(state_matrix)
                round_matrix = get_transposed_matrix(self.round_keys[i], self.length, self.width)
                state_matrix = self.add_round_key(state_matrix, round_matrix)

            state_matrix = self.sub_bytes_2d(state_matrix)
            state_matrix = self.shift_rows(state_matrix)
            round_matrix = get_transposed_matrix(self.round_keys[self.rounds - 1], self.length, self.width)
            state_matrix = self.add_round_key(state_matrix, round_matrix)

            ciphertext = get_text_from_matrix(state_matrix)
            ciphertext = get_string_from_list(ciphertext)
            asciitext = get_ascii_from_hex(ciphertext)
            # print("Ascii text: ", asciitext)

            full_ciphertext += ciphertext
            full_asciitext += asciitext

        # print("Ciphertext: ", full_ciphertext)
        # print("ASCII text: ", full_asciitext)
        return full_ciphertext, full_asciitext

    # AES decryption
    def decrypt(self, ciphertext):

        ciphertext_blocks = pad_text(ciphertext)
        # print("Ciphertext blocks: ", ciphertext_blocks)
        full_plaintext = ""
        full_asciitext = ""

        for block in ciphertext_blocks:

            ciphertext_matrix = get_hex_matrix(block)

            state_matrix = get_transposed_matrix(ciphertext_matrix, self.length, self.width)
            round_matrix = get_transposed_matrix(self.round_keys[self.rounds - 1], self.length, self.width)

            state_matrix = self.add_round_key(state_matrix, round_matrix)

            for i in range(self.rounds - 1, 1, -1):
                state_matrix = self.inv_shift_rows(state_matrix)
                state_matrix = self.inv_sub_bytes_2d(state_matrix)
                round_matrix = get_transposed_matrix(self.round_keys[i - 1], self.length, self.width)
                state_matrix = self.add_round_key(state_matrix, round_matrix)
                state_matrix = self.inv_mix_columns(state_matrix)

            state_matrix = self.inv_shift_rows(state_matrix)
            state_matrix = self.inv_sub_bytes_2d(state_matrix)
            round_matrix = get_transposed_matrix(self.round_keys[0], self.length, self.width)
            state_matrix = self.add_round_key(state_matrix, round_matrix)

            plaintext = get_text_from_matrix(state_matrix)
            plaintext = get_string_from_list(plaintext)
            asciitext = get_ascii_from_hex(plaintext)

            full_plaintext += plaintext
            full_asciitext += asciitext

        full_asciitext = full_asciitext.rstrip()

        return full_plaintext, full_asciitext
