from bitvectordemo import *
from BitVector import *

# Pad or trim a key to 16 bytes
def pad_or_trim(key):
    if len(key) == 16:
        return key
    if len(key) > 16:
        return key[:16]
    if len(key) < 16:
        key = str.ljust(key, 16)
        return key

# pad a text to a multiple of 16 bytes
def pad_text(text):
    if len(text) % 16 != 0:
        text = str.ljust(text, len(text) + (16 - (len(text) % 16)), ' ')
    texts = [text[i:i+16] for i in range(0, len(text), 16)]
    return texts

# get the 1D hex matrix from a string
def get_hex_matrix(text):
    matrix = []
    for i in range(4):
        for j in range(4):
            matrix.append(BitVector(textstring=text[i * 4 + j]).get_hex_string_from_bitvector())

        # hex_matrix = list_2d(matrix,self.length,self.width)

    return matrix

# get ascii value from hex string
def get_ascii_from_hex(hex_string):
    ascii_string = ''.join([chr(int(''.join(c), 16)) for c in zip(hex_string[0::2],hex_string[1::2])])
    return ascii_string

# make a 2D list from a list
def list_2d(list1, rows, columns):
    result = []
    start = 0
    end = columns
    for i in range(rows):
        result.append(list1[start:end])
        start += columns
        end += columns
    return result

# left-rotate a matrix by a given number of offset
def circular_rotate_left(word,offset):
    temp = word.copy()
    l = len(word)
    for i in range(l):
        temp[i] = word[(i+offset)%l]
    return temp

# right-rotate a matrix by a given number of offset
def circular_rotate_right(word,offset):
    temp = word.copy()
    l = len(word)
    for i in range(l):
        temp[(i+offset)%l] = word[i]
    return temp

# xor add a round constant to a matrix
def add_round_constant(word,i):

    word[0] = hex(int(word[0], 16) ^ int(round_cons[i], 16))[2:]
    return word

# hex xor of two words
def hex_xor_word(w1,w2):
    result = []
    for i in range(len(w1)):
        result.append(hex(int(w1[i], 16) ^ int(w2[i], 16))[2:])
    return result

# hex xor of two 2D matrices
def xor_2d(mat1,mat2):
    result = []
    for i in range(len(mat1)):
        result.append(hex_xor_word(mat1[i],mat2[i]))
    return result

# get transpose of a matrix
def get_transposed_matrix(matrix,height, width):
    mat_2d = list_2d(matrix, height, width)
    for i in range(height):
        for j in range(width):
            mat_2d[j][i] = matrix[i * width + j]

    return mat_2d

# get 1D list from 2D matrix
def get_text_from_matrix(matrix):
    result = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            result.append(matrix[j][i])
    return result

# get string from a list
def get_string_from_list(list):
    text = ""
    for i in range(len(list)):
        if len(list[i]) == 1:
            text += '0'
        text += list[i]
    return text

# print a 2D matrix
def print_matrix(matrix):
    for row in matrix:
        for element in row:
            print(element, end=" ")
        print()

# convert a hex list to bitvector one
def hex_to_bitvector(matrix):
    result = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[0])):
            row.append(BitVector(hexstring=matrix[i][j]))
        result.append(row)
    return result

# convert a bitvector list to hex list
def bitvector_to_hex(matrix):
    result = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[0])):
            row.append(matrix[i][j].get_bitvector_in_hex())
        result.append(row)
    return result

# perform galois matrix multiplication in a finite field
def matrix_mul(mat1,mat2):
    result = []
    for i in range(len(mat1)):
        row = []
        for j in range(len(mat2[0])):
            sum = mat1[i][0].gf_multiply_modular(mat2[0][j], AES_modulus, 8)
            sum ^= mat1[i][1].gf_multiply_modular(mat2[1][j], AES_modulus, 8)
            sum ^= mat1[i][2].gf_multiply_modular(mat2[2][j], AES_modulus, 8)
            sum ^= mat1[i][3].gf_multiply_modular(mat2[3][j], AES_modulus, 8)
            row.append(sum)
        result.append(row)
    return bitvector_to_hex(result)