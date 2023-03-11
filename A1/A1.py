text = open('WordCount-test1.in')

ends = [',', '.', '!', '?', ']', '[']
starts = [',', '.', '!', '?', ']', '[']

all_words = set({})
dict_words = {}

for row in text:
    words = row.split(' ')
    for word in words:
        word = word.rstrip()
        if word[-1] in ends:
            print(word[:-1])
            x = word[:-1]
            if x in all_words:
                dict_words[x] += 1
            else:
                dict_words[x] = 1
            all_words.add(x)
        elif word[0] in starts:
            print(word[1:])
            x = word[1:]
            if x in all_words:
                dict_words[x] += 1
            else:
                dict_words[x] = 1
            all_words.add(x)
        else:
            print(word)
            if word in all_words:
                dict_words[word] += 1
            else:
                dict_words[word] = 1
            all_words.add(word)

for key in dict_words.keys():
    print(key, dict_words[key])
print(f'{len(dict_words)}/{sum(dict_words.values())}')


