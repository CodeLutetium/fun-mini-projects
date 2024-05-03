import numpy as np
import random
import pyperclip
import getpass

# For cryptography
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import scrypt


def generate_passphrase(length: int, seed=None) -> str:
    """Generates a passphrase of the given length using the given seed.

    Args:
        length (int): The number of words in the passphrase.
        seed (int): The seed for the random number generator.

    Returns:   
        str: A passphrase of the given length.
    """
    # Check if length is valid
    if length < 4:
        print("Passphrase length should be at least 4. Default length of 4 selected.")
        length = 4

    if length > 20:
        print("Passphrase is too long. Limit of 20 selected")
        length = 20

    rng_generator = np.random.default_rng(seed)
    words = load_words()
    MAX_INDEX = len(words) - 1
    random_indexes = rng_generator.integers(0, MAX_INDEX, length)

    passphrase = "-".join([words[i] for i in random_indexes])
    return passphrase


def generate_password(length: int, seed: str) -> str:
    raise NotImplementedError


def load_words() -> list[str]:
    with open("wordlist.txt", "r") as f:
        return f.read().splitlines()


def check_pw_file() -> None:
    """
    Check if passwords.csv exists, if not create it."""
    try:
        with open("passwords.csv", "r") as f:
            pass
    except FileNotFoundError:
        # Disclaimer
        input("Disclaimer: This program was written for fun, please do not use it to generate/ store password for sensitive accounts. NEVER store passwords in plain text! Press enter to continue.")

        create_master_pw()

        # Create passwords.csv
        with open("passwords.csv", "w") as f:
            pass


def store_password(passphrase: str) -> None:
    # Check for existence of passwords.csv
    check_pw_file()

    # Retrieve salt
    try:
        with open("salt", "rb") as f:
            salt = f.read()
    except FileNotFoundError:
        print("Salt not found.")
        return
    
    # Create kdf object
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000
    )

    # Verify master password
    master_password = getpass.getpass("Enter master password: ")
    if not verify_master_pw(master_password, salt):
        print("Master password is incorrect.")
        return
    
    # Encrypt passphrase
    key = base64.urlsafe_b64encode(kdf.derive(str.encode(master_password)))
    f = Fernet(key)
    passphrase = f.encrypt(str.encode(passphrase))

    # Save encrypted passphrase to passwords.csv
    website = input("Enter website: ")
    with open("passwords.csv", "a") as f:
        f.write(f"{website}, {passphrase}\n")

    print("Passphrase saved to passwords.csv")


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


def verify_master_pw(master_password: str, salt: bytes) -> bool:
    # Retrieve stored hashed master password
    try:
        with open("master_pw", "rb") as f:
            stored_hashed_pw = f.read()
            stored_hashed_pw = base64.urlsafe_b64encode(stored_hashed_pw)
    except FileNotFoundError:
        print("Master password not found.")
        return False

    # Hash user input and compare to stored hash
    return stored_hashed_pw == scrypt.hash(str.encode(master_password), salt)


def main() -> None:
    length = input("Enter passphrase length (at least 4): ")
    try:
        passphrase_length = int(length)
    except ValueError:
        print("Invalid input, please enter an integer. Default length of 4 selected.")
        passphrase_length = 4
    seed = input("Enter seed for random number generator (optional): ")

    seed = random.seed(seed)

    passphrase = generate_passphrase(passphrase_length, seed)
    print("Your passphrase is: ")
    print(passphrase)

    pyperclip.copy(passphrase)
    print("Passphrase automatically copied to clipboard.")

    response = input(
        "Do you want to save your password to a text file? (y/n): ")
    if response.lower() == "y":
        store_password(passphrase)
    else:
        print("Password not saved")


if __name__ == "__main__":
    main()
