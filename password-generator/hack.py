# Program to hack into my system (not completed)
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken


with open("master_pw", "rb") as f:
    master_pw = f.read()

with open("salt", "rb") as f:
    salt = f.read()

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000
)

# Decrypt master password
key = base64.urlsafe_b64encode(kdf.derive(master_pw))
f= Fernet(key)
master_pw = f.decrypt(master_pw)
print("Master password:", master_pw)