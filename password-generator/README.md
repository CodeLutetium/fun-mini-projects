# Password-Generator

Password-Generator is a mini Python project by me to generate and store passwords and passphrases. Passphrases are more secure and memorable than passwords, and this sparked me an idea to create a simple passphrase generator, which quickly evolved to this project as I added more features.

Please feel free to play around with my code and look for vulnerabilities in my code. 

Generated passwords can be saved in a file (passwords.csv). This functionality is implemented with [Fernet](https://cryptography.io/en/latest/fernet/) and uses symmetric key encryption to store the passwords. **NEVER** store passwords in plaintext!

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

## Usage
Ensure that you have a list of words that the passphrase generator can choose from. The list of words should be saved as `wordlist.txt` in the same directory. To generate `wordlist.txt`, you can also run `load_wordlist.py`.

As of the most recent commit, only the passphrase generator function has been implemented. The password generator function will be implemented in the future.


## License

[MIT](https://choosealicense.com/licenses/mit/)