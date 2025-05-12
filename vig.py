def generate_key(msg, key):
    key = list(key)
    if len(msg) == len(key):
        return key
    else:
        for i in range(len(msg) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def encrypt_vigenere(msg, key, alphabet):
    encrypted_text = []
    key = generate_key(msg, key)
    for i in range(len(msg)):
        m_index = alphabet.index(msg[i])
        k_index = alphabet.index(key[i])
        encrypted_char = alphabet[(m_index + k_index) % len(alphabet)]
        encrypted_text.append(encrypted_char)
    return "".join(encrypted_text)

def decrypt_vigenere(msg, key, alphabet):
    decrypted_text = []
    key = generate_key(msg, key)
    for i in range(len(msg)):
        c_index = alphabet.index(msg[i])
        k_index = alphabet.index(key[i])
        decrypted_char = alphabet[(c_index - k_index) % len(alphabet)]
        decrypted_text.append(decrypted_char)
    return "".join(decrypted_text)


def switch_chars(text,char1,char2):
    text = list(text)
    for i in range(len(text)):
        if text[i] == char1:
            text[i] = char2
        elif text[i] == char2:
            text[i] = char1
    return "".join(text)


# Example usage
text_to_encrypt = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
#text_to_encrypt = switch_chars(initialText, "K", "E")

key = "VCWWZ"
alphabet = "KRYPTOSABCDEFGHIJLMNQUVWXZ"

encrypted_text = encrypt_vigenere(text_to_encrypt, key, alphabet)
print(f"Encrypted Text: {encrypted_text}")

decrypted_text = decrypt_vigenere(text_to_encrypt, key, alphabet)
print(f"Decrypted Text: {decrypted_text}")

print(decrypted_text[4])
print(decrypted_text[19])
print(decrypted_text[3])
print(decrypted_text[3])
print(decrypted_text[0])

if decrypted_text[63] == "B":
    print("Correct!")
else:
    print("Incorrect!")
