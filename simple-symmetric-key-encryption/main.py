def encrypt(key: str, msg: str) -> str:
    # Simple symmetric key encryption using XOR of key and msg
    raise NotImplementedError

def decrypt(key: str, token: str) -> str:
    # Simple symmetric key decryption using XOR of key and token
    raise NotImplementedError

def main():
    key = input("Enter key (longer is better): ")
    msg = input("Enter message: ")
    token = encrypt(key, msg)
    print(f"Encrypted token: {token}")
    print(f"Decrypted message: {decrypt(key, token)}")

if __name__ == "__main__":
    main()