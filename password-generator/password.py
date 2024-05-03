"""
Playground to experiement with the master password function before implementing it in main
"""
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken
import getpass
import scrypt


def create_master_pw() -> None:
    # Create salt and save it
    salt = os.urandom(32)
    with open("salt", "wb") as f:
        f.write(salt)

    # Get master password from user
    isValidPassword = False
    while isValidPassword != True:
        master_password = getpass.getpass(
            "Enter master password. The master password will be used to encrypt and decrypt your stored passwords. \nMaster password (at least 8 characters): ")

        # @TODO Add function to check if master password is sufficiently strong
        if len(master_password) < 8:
            print("Master password should be at least 8 characters.")
        else:
            print("Master password successfully created")
            isValidPassword = True
            master_password = str.encode(master_password)

    # Hash salted master password and store
    hashed_pw = scrypt.hash(master_password, salt)
    with open("master_pw", "wb") as f:
        f.write(hashed_pw)
        print("Master password successfully stored.")


def verify_master_pw() -> bool:
    # Load salt
    try:
        with open("salt", "rb") as f:
            salt = f.read()
    except FileNotFoundError:
        print("Salt not found.")
        return False

    # Get master password from user
    master_password = getpass.getpass("Enter master password: ")

    # Retrieve stored hashed master password
    try:
        with open("master_pw", "rb") as f:
            stored_hashed_pw = f.read()
    except FileNotFoundError:
        print("Master password not found.")
        return False

    return stored_hashed_pw == scrypt.hash(str.encode(master_password), salt)


def test():
    password = b"password"
    with open("salt", "rb") as f:
        salt = f.read()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))

    f = Fernet(key)
    token = f.encrypt(b"message")
    
    password2 = b"password123"
    kdf2 = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000
    )
    key2 = base64.urlsafe_b64encode(kdf2.derive(password2))

    f = Fernet(key2)
    try:
        print(f.decrypt(token))
    except InvalidSignature:
        print("Incorrect password")
    except InvalidToken:
        print("Incorrect token")
    except:
        print("Something went wrong")


# create_master_pw()
print(verify_master_pw())
# test()
