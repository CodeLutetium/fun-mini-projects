"""
Helper program to generate the txt file of eligible words (4 letters or longer) from online txt file

Source used: Florida State University 300,260 English words (https://people.sc.fsu.edu/~jburkardt/datasets/words/wordlist.txt)
"""
from urllib.request import urlopen

def main() -> None:
    url = "https://people.sc.fsu.edu/~jburkardt/datasets/words/wordlist.txt"
    with open("wordlist.txt", "w") as f:
        for line in urlopen(url):
            word = line.decode("utf-8").strip()
            if len(word) >= 4:
                f.write(word + "\n")

if __name__ == "__main__":
    main()