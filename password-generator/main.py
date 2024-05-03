import numpy as np

def generate_passphrase(length: int, seed=42) -> str:
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

    rng_generator = np.random.default_rng(seed)
    words = load_words()
    MAX_INDEX = len(words) - 1
    random_indexes = rng_generator.integers(0, MAX_INDEX, length)

    passphrase = "-".join([words[i] for i in random_indexes])
    return passphrase


def generate_password(length: int, seed: str) -> str:
    raise NotImplementedError


def generate_seed(seed: int) -> int:
    raise NotImplementedError


def load_words() -> list[str]:
    with open("wordlist.txt", "r") as f:
        return f.read().splitlines()


def main() -> None:
    length = input("Enter passphrase length (at least 4): ")
    try:
        passphrase_length = int(length)
    except ValueError:
        print("Invalid input, please enter an integer. Default length of 4 selected.")
        passphrase_length = 4
    seed = input("Enter seed for random number generator (optional): ")
    
    passphrase = generate_passphrase(passphrase_length)
    print(passphrase)


if __name__ == "__main__":
    main()
