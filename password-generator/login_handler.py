"""
Login handler class to handler user login
"""
import getpass
import os
import scrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


class LoginHandler():
    def __init__(self):
        self.salt = self.retrieve_salt()
        self.master_password = None
        self.is_logged_in = False
        self.has_master_password = self.check_master_pw()

        self.f = None

    def retrieve_salt(self) -> bytes:
        """
        Retrieve salt from the directory. If the salt is not found, generate a new salt and save it in the directory.

        Args:
            None

        Returns:
            bytes: Salt
        """
        try:
            with open("salt", "rb") as f:
                salt = f.read()
        except FileNotFoundError:
            # Generate salt
            salt = os.urandom(32)
            with open("salt", "wb") as f:
                f.write(salt)
        return salt

    def check_master_pw(self) -> bool:
        """
        Checks if master password exists in directory. Retrieves it if exists.

        Args:
            None

        Returns:
            bool: True if master password exists, False otherwise
        """
        try:
            with open("master_pw", "rb") as f:
                self.master_password = f.read()
                return True
        except FileNotFoundError:
            return False

    def login(self) -> None:
        """
        Verify the master password with the stored master password. Once verified, logs the user in

        Args:
            None

        Returns:
            None
        """
        if self.has_master_password == False:
            self.create_master_pw()
            return

        master_password = getpass.getpass("Enter master password: ")

        # Hash user input and compare to stored hash
        if self.master_password == scrypt.hash(str.encode(master_password), self.salt):
            print("Login success!")
            self.is_logged_in = True
            self.init_fernet()
        else:
            print("Login failed: wrong password.")
            self.is_logged_in = False
            return

    def create_master_pw(self) -> None:
        """
        Create a master password and store the hash in the directory

        Args:
            None

        Returns:
            None
        """
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
        hashed_pw = scrypt.hash(master_password, self.salt)
        with open("master_pw", "wb") as f:
            f.write(hashed_pw)
            print("Master password successfully stored.")

        with open("passwords.csv", "w") as f:
            print("passwords.csv created.")

        self.has_master_password = True
        self.master_password = master_password
        self.is_logged_in = True
        self.init_fernet()

    def init_fernet(self) -> None:
        """
        Initialize the Fernet object with the master password

        Args:
            None

        Returns:
            None
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=480000
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_password))
        self.f = Fernet(key)
