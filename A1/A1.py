text = open('WordCount-test1.in')


def clean_word(string):
    end = [',', '.', '!', '?', ']', '[']
    start = [',', '.', '!', '?', ']', '[']
    if string[-1] in end:
        return string[:-1]
    elif string[0] in start:
        return string[1:]
    else:
        return string


def count_word(string, all_word, word_s):
    if string in all_word:
        word_s[string] += 1
    else:
        word_s[string] = 1
    all_word.add(string)
    return all_word, word_s


special_case = {'don\'t': ['do', 'not'], 'I\'m': ['I', 'am']}

word_set = set({})
word_counts = {}

for row in text:
    words = row.split(' ')
    for word in words:
        word = clean_word(word.rstrip())
        if word in list(special_case.keys()):
            cur_words = special_case[word]
            for cur_w in cur_words:
                count_word(cur_w, word_set, word_counts)
        else:
            count_word(word, word_set, word_counts)


for key in word_counts.keys():
    print(key, word_counts[key])
print(f'{len(word_counts)}/{sum(word_counts.values())}')
