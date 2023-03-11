import os
import argparse as ap
import re

# python3 sedorfer-WordCount.py -h for help on how to use this tool


def count_occurrences(words: list[str]) -> dict[str, int]:
    word_dict = dict()
    for w in words:
        word_dict[w] = word_dict[w] + 1 if w in word_dict else 1        # increase count by one or create entry
    return word_dict


def word_count(file: str, ignore: bool, lst: bool):
    if not os.path.isfile(file):
        raise FileNotFoundError(f"{file} does not exist")
    with open(file, "r") as f:
        text = f.read()
        if ignore:
            text = text.lower()
        words = re.findall(r"\w+", text)        # finds all words while ignoring punctuations and special symbols
        word_dict = count_occurrences(words)
        if not lst:
            print(f"{len(word_dict)} / {len(words)}")
        else:
            sorted_words = sorted(word_dict.items(), key=lambda item: (-item[1], item[0]))      # sorts words by frequency and then alphabetically
            for (word, frequency) in sorted_words:
                print(f"{word}\t{frequency}")


if __name__ == "__main__":
    parser = ap.ArgumentParser(description="Word Count for a text file. Output: Number of different words/total number")
    parser.add_argument("file", help="path to file")
    parser.add_argument("-I", action="store_true", help="case insensitive")     # adds flags to the tool
    parser.add_argument("-l", action="store_true", help="list words and their frequency")
    args = parser.parse_args()      # parses the arguments and options from the command line
    word_count(file=args.file, ignore=args.I, lst=args.l)




