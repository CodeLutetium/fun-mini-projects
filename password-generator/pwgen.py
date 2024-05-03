"""
Functions to generate passwords and passphrases
"""
import numpy as np
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
    """
    Loads a list of words from a file.

    Args:
        None

    Returns:
        list[str]: A list of words.
    """
    try:
        with open("wordlist.txt", "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print("Wordlist not found. Generate word list and save as wordlist.txt in the same directory.")
        raise FileNotFoundError
