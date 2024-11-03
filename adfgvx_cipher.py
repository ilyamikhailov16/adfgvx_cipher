from typing import List, Dict


def create_adfgvx_square(square_2d: list) -> dict:
    square_dict = {}
    for i in range(1, 7):
        for j in range(1, 7):
            square_dict[square_2d[i][j]] = square_2d[0][i - 1] + square_2d[j][0]

    return square_dict


def adfgvx_encrypt(plaintext: str, key: str, square: Dict[str, str]) -> str:
    if not key.isalpha():
        raise ValueError
    
    square = {key.lower(): value for key, value in square.items()}
    
    plaintext = plaintext.lower()
    for letter in plaintext:
        if letter not in square:
            plaintext = plaintext.replace(letter, "")


    # first step
    plaintext_split = list(plaintext)
    for i, letter in enumerate(plaintext_split):
        plaintext_split[i] = square[letter]

    

    plaintext = list("".join(plaintext_split))
    key_table = []
    residue = len(plaintext) % len(key)

    for i in range(len(plaintext) // len(key) + (residue // 2)):
        key_table.append(list(plaintext[: len(key)]))
        del plaintext[: len(key)]
        
    # second step
    index_key_dict = []

    for i, letter in enumerate(key):
        index_key_dict.append([letter, i])

    permutation_key = sorted(key)
    index_permutation_key = []

    for i, letter in enumerate(permutation_key):
        for j, pair in enumerate(index_key_dict):
            if letter in pair:
                index_permutation_key.append([i, pair[1]])
                index_key_dict.pop(j)
                break

    permutation_table = []
    for row in key_table:
        if len(row) == len(key):
            permutation_row = row.copy()
            for idx in index_permutation_key:
                permutation_row[idx[0]] = row[idx[1]]

            permutation_table.append(permutation_row)
        else:
            permutation_row = row
            permutation_table.append(permutation_row)

    ciphertext = ""

    for row in permutation_table:
        ciphertext += "".join(row).lower()

    return ciphertext.upper()
def adfgvx_decrypt(ciphertext: str, key: str, square: Dict[str, str]) -> str:
    if not key.isalpha():
        raise ValueError
    ciphertext = list(ciphertext)
    # first step
    permutation_table = []
    residue = len(ciphertext) % len(key)
    for _ in range(len(ciphertext) // len(key) + (residue // 2)):
        permutation_table.append(list(ciphertext[: len(key)]))
        del ciphertext[: len(key)]
    
    # second step
    index_key_dict = []
    for i, letter in enumerate(key):
        index_key_dict.append([letter, i])

    permutation_key = sorted(key)
    index_permutation_key = []

    for i, letter in enumerate(permutation_key):
        for j, pair in enumerate(index_key_dict):
            if letter in pair:
                index_permutation_key.append([i, pair[1]])
                index_key_dict.pop(j)
                break

    key_table = []
    for permutation_row in permutation_table:
        if len(permutation_row) == len(key):
            row = permutation_row.copy()
            for idx in index_permutation_key:
                row[idx[1]] = permutation_row[idx[0]].upper()
            key_table.append(row)
        else:
            row = [el.upper() for el in permutation_row]
            key_table.append(row)

    for i, row in enumerate(key_table):
        key_table[i] = "".join(row)

    key_string = "".join(key_table)

    plaintext_list = []

    for i in range(0, len(key_string), 2):
        plaintext_list.append(key_string[i : i + 2])

    square = {value: key for key, value in square.items()}
    plaintext = ""
    for letter in plaintext_list:
        plaintext += square[letter]

    return plaintext.upper()

plaintext = "Hello, World! 123"
key = 'SECRET'
square_2d =  [
        ["A", "D", "F", "G", "V", "X"],
    ["A", "n", "h", "q", "g", "m", "e"],
    ["D", "a", "y", "s", "o", "f", "d"],
    ["F", "v", "p", "i", "r", "u", "t"],
    ["G", "b", "l", "c", "w", "k", "z"],
    ["V", "j", "X", "3", "4", "5", "6"],
    ["X", "0", "1", "2", "7", "8", "9"],
]

square = create_adfgvx_square(square_2d)
encrypted = adfgvx_encrypt(plaintext, key, square)
print(encrypted)
decrypted = adfgvx_decrypt(encrypted, key, square)
print(decrypted)