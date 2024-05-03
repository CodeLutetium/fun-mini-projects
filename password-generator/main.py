import random
import pyperclip

# Import relevant modules
from pwgen import generate_passphrase, generate_password
from login_handler import LoginHandler


def generate_passphrase_main() -> None:
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
        "Do you want to save your password to a text file? (y/[n]): ")
    if response.lower() == "y":
        store_password(passphrase)
    else:
        print("Password not saved")


def generate_password_main() -> None:
    raise NotImplementedError


def view_passwords() -> None:
    if login_handler.is_logged_in == False:
        login_handler.login()

    with open("passwords.csv", "r") as f:
        passwords = f.readlines()
        for password in passwords:
            website, encrypted_passphrase = password.split(", ")
            passphrase = login_handler.f.decrypt(encrypted_passphrase)
            print(f"Website: {website}, Password: {passphrase.decode()}")


def store_password(passphrase: str) -> None:
    if login_handler.is_logged_in == False:
        login_handler.login()

    # Encrypt passphrase
    passphrase = login_handler.f.encrypt(str.encode(passphrase))
    passphrase = passphrase.decode()

    # Save encrypted passphrase to passwords.csv
    website = input("Enter website: ")
    with open("passwords.csv", "a") as f:
        f.write(f"{website}, {passphrase}\n")

    print("Passphrase saved to passwords.csv")


login_handler = LoginHandler()


def main() -> None:
    print((login_handler.master_password))
    while True:
        print("==============================")
        print("{:-^30}".format("Password manager"))
        print("==============================")
        print(f"""
Select an option:
(1) Generate passphrase
(2) Generate password
(3) View stored passwords {"(login required)" if login_handler.is_logged_in is False else ""}
Press any other key to exit
              
Login status: {"Logged in" if login_handler.is_logged_in else "Not logged in"}
""")
        if login_handler.has_master_password == False:
            print("Press (4) or (L) to create a master password.")
        elif login_handler.is_logged_in == False:
            print("Press (4) or (L) to login.")

        print("==============================")

        response = input()
        if response == "1":
            generate_passphrase_main()
        elif response == "2":
            generate_password_main()
        elif response == "3":
            view_passwords()
        elif response == "4" or response.lower() == "l" and login_handler.is_logged_in == False:
            login_handler.login()
        else:
            print("Exiting program")
            break


if __name__ == "__main__":
    main()
