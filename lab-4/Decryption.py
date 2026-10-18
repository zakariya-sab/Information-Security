# AES S-box (public standard table). For decryption, invert this mapping.
SBOX = [int(x, 16) for x in """63 7c 77 7b f2 6b 6f c5 30 01 67 2b fe d7 ab 76
ca 82 c9 7d fa 59 47 f0 ad d4 a2 af 9c a4 72 c0
b7 fd 93 26 36 3f f7 cc 34 a5 e5 f1 71 d8 31 15
04 c7 23 c3 18 96 05 9a 07 12 80 e2 eb 27 b2 75
09 83 2c 1a 1b 6e 5a a0 52 3b d6 b3 29 e3 2f 84
53 d1 00 ed 20 fc b1 5b 6a cb be 39 4a 4c 58 cf
d0 ef aa fb 43 4d 33 85 45 f9 02 7f 50 3c 9f a8
51 a3 40 8f 92 9d 38 f5 bc b6 da 21 10 ff f3 d2
cd 0c 13 ec 5f 97 44 17 c4 a7 7e 3d 64 5d 19 73
60 81 4f dc 22 2a 90 88 46 ee b8 14 de 5e 0b db
e0 32 3a 0a 49 06 24 5c c2 d3 ac 62 91 95 e4 79
e7 c8 37 6d 8d d5 4e a9 6c 56 f4 ea 65 7a ae 08
ba 78 25 2e 1c a6 b4 c6 e8 dd 74 1f 4b bd 8b 8a
70 3e b5 66 48 03 f6 0e 61 35 57 b9 86 c1 1d 9e
e1 f8 98 11 69 d9 8e 94 9b 1e 87 e9 ce 55 28 df
8c a1 89 0d bf e6 42 68 41 99 2d 0f b0 54 bb 16
""".split()]
INV_SBOX = [0] * 256
for index, value in enumerate(SBOX):
    INV_SBOX[value] = index

# First byte of each Rcon word, for the 10 AES-128 expansions.
RCON = [0x01, 0x02, 0x04, 0x08, 0x10,0x20, 0x40, 0x80, 0x1B, 0x36]
def expand_key(key):
    """PROVIDED: expand a 16-byte AES key into 11 round keys.
    Every 4-byte word is a column. w[0]..w[3] are the original key.
    At positions divisible by four: RotWord, SubWord, Rcon, then XOR.
    At all positions: XOR with the word four positions earlier.
    Output: round_keys[round][row][column] for rounds 0..10.
    """
    if len(key) != 16:
        raise ValueError("AES-128 requires exactly 16 key bytes")
    words = [list(key[4*i : 4*i+4]) for i in range(4)]
    for i in range(4, 44):
        temp = words[i-1].copy()
        if i % 4 == 0:
            temp = temp[1:] + temp[:1] # RotWord
            temp = [SBOX[b] for b in temp] # SubWord
            temp[0] ^= RCON[i//4-1] # Rcon
        words.append([words[i-4][j] ^ temp[j] for j in range(4)])
    round_keys = []
    for rnd in range(11):
        cols = words[4*rnd : 4*rnd+4]
        round_keys.append([[cols[c][r] for c in range(4)]for r in range(4)])
    return round_keys
def bytes_to_state(block):
    return [[block[j + i*4] for i in range(4)] for j in range(4)]
def state_to_bytes(state):
    result = []
    for i in range(4):
        for j in range(4):
            result.append(state[j][i])
    return bytes(result)

def xtime(value):
    """PROVIDED: multiply by 02 in GF(2^8), reducing with 0x1B."""
    return ((value << 1) & 0xFF) ^ (0x1B if value & 0x80 else 0)
# ===== IMPLEMENT THE INVERSE AES TRANSFORMATIONS =====
def add_round_key(state, round_key):
    """TODO 1: XOR every state byte with the matching round-key byte.
    Both arguments are 4x4 matrices, indexed as [row][column].
    Modify state in place.
    """
    for i in range(4):
        for j in range(4):
            state[i][j] = state[i][j] ^ round_key[i][j]
    return state
def right_Shift(row,pos):
    original = row.copy()
    for i in range(4):
        row[i] = original[(i-pos)%4]
    return row
def inv_shift_rows(state):
    """TODO 2: circularly shift row r RIGHT by r positions.
    Row 0: 0, row 1: 1, row 2: 2, row 3: 3 positions.
    """
    for i in range(4):
        state[i] = right_Shift(state[i],i)
    return state 
# -------------------------------------
# def left_Shift(row , pos):
#     original = row.copy()
#     for i in range(4):
#        row[i] = original[(i+pos) % 4]
#     return row
# def shift_rows(state):
#     for i in range(4):
#         state[i] = left_Shift(state[i],i)
#     return state
# -------------------------------------
def inv_sub_bytes(state):
    """TODO 3: substitute each byte using the provided INV_SBOX."""
    for i in range(4):
        for j in range(4):
            state[i][j] = INV_SBOX[state[i][j]]
    return state
def gf_mul(a, b):
    """TODO 4: multiply two bytes in GF(2^8).
    HINT: when b’s low bit is 1, XOR a into the result;
    update  a with xtime(a); shift b one bit right; repeat.
    """ 
    result = 0
    A =a 
    while(b != 0):
        if(b & 1 ) ==1:
            result = result ^ A
        A = xtime(A)
        b = b>>1
    return result
def inv_mix_columns(state):
    """TODO 5: transform every column using the inverse AES matrix:
    0E 0B 0D 09
    09 0E 0B 0D
    0D 09 0E 0B
    0B 0D 09 0E
    Multiply with gf_mul, combine using XOR. Modify state in place.
    """
    inverseAesM = [[0x0E ,0x0B, 0x0D, 0x09],[0x09,0x0E,0x0B,0x0D],[0x0D,0x09,0x0E,0x0B],[0x0B,0x0D,0x09,0x0E]]
    a = b = c = d = 0
    for i in range(4):
        a = state[0][i]
        b = state[1][i]
        c = state[2][i]
        d = state[3][i]
        for j in range(4):
            state[j][i] = (
                gf_mul(a, inverseAesM[j][0])
                ^ gf_mul(b, inverseAesM[j][1])
                ^ gf_mul(c, inverseAesM[j][2])
                ^ gf_mul(d, inverseAesM[j][3])
            )    
    return state 
def decrypt_block(ciphertext, round_keys):
    """TODO 6: AES-128 inverse cipher for exactly one 16-byte block.
    Suggested sequence:
    1. Build the 4x4 state from ciphertext.
    2. AddRoundKey using round key 10.
    3. For rounds 9 down to 1:
    InvShiftRows, InvSubBytes, AddRoundKey, InvMixColumns.
    4. InvShiftRows, InvSubBytes, AddRoundKey using round key 0.
    5. Convert the final state to bytes and return it.
    """
    state= bytes_to_state(ciphertext)
    state = add_round_key(state,round_keys[-1])
    for i in range(9):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state= add_round_key(state,round_keys[9-i])
        state = inv_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state= add_round_key(state,round_keys[0])
    return state_to_bytes(state)

# ===== PROVIDED TEST INPUT: =====
KEY = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
CIPHERTEXT = bytes.fromhex("d21bb1d61866796323d61a23c635fb45")
if __name__ == "__main__":
    keys = expand_key(KEY)
    assert len(keys) == 11
    plaintext = decrypt_block(CIPHERTEXT, keys)
    print("Plaintext (hex):", plaintext.hex())
    print("Secret message: ", plaintext.decode("ascii"))

