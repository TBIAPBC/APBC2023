import re
import argparse
from collections import Counter

parser = argparse.ArgumentParser(description='A1 - Word Counting')
parser.add_argument('input', type=str, help='the input file')
parser.add_argument('-I', action='store_true', help='ignore upper/lower case')
parser.add_argument('-l', action='store_true', help='print list')
args = parser.parse_args()

pattern = "\w+"

if __name__ == "__main__":
    with open(args.input, "r") as f:
        content = f.read()

    if args.I:
        content = content.lower()

    all_words = re.findall(pattern, content)
    diff_words = set(all_words)

    if args.l:
        count = Counter(all_words)
        count = sorted(count.items(), key=lambda item: (-item[1], item[0]))
        for word in count:
            print(f"{word[0]}\t{word[1]}")
    else:
        print(len(diff_words), "/", len(all_words))

