def encrypt(key: str, msg: str) -> str:
    """
    Simple symmetric key encryption using XOR of key and msg

    Args:
        key (str): key to be used for encryption
        msg (str): message to be encrypted

    Returns:
        str: encrypted ciphertext
    """
    ciphertext = []
    for i in range(len(msg)):
        ciphertext.append(chr(ord(msg[i]) ^ ord(key[i % len(key)])))
    return "".join(ciphertext)
    

def decrypt(key: str, ciphertext: str) -> str:
    """
    Simple symmetric key decryption using XOR of key and ciphertext
    """
    return encrypt(key, ciphertext)


def main():
    key = input(
        "Enter key. For best security, key should at least be as long as the message (see one time pad): ")
    msg = input("Enter message: ")
    ciphertext = encrypt(key, msg.strip())
    print(f"Encrypted ciphertext: {ciphertext}")
    print(f"Decrypted message: {decrypt(key, ciphertext)}")


if __name__ == "__main__":
    main()
