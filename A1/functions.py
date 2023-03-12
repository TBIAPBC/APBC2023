# -*- coding: utf-8 -*-
def clean_word(word):
    # this removes unnecessary things from the words and changes the 'umlaute'
    word = word.strip(',.!?][\"\n\'-;: \r')
    word.replace('ä', 'ae')
    word.replace('ö', 'oe')
    word.replace('ü', 'ue')
    word.replace('ß', 'ss')
    return word


def get_words(row):
    row = row.replace('-', ' ')
    words = row.split(' ')
    return words


def count_word(current_word, word_set, word_count):
    # this counts the word and updates the dictionary
    if current_word in word_set:
        word_count[current_word] += 1
    else:
        word_count[current_word] = 1
    word_set.add(current_word)
    return word_set, word_count


def word_counter(text, ignore_case=False, print_list=False):
    # here the text will be processed and some special cases are filtered out
    special_cases = {'don\'t': ['do', 'not'], 'I\'m': ['I', 'am'], 'demon\'s': ['demon'], 'cushion\'s': ['cushion'],
                     'bosom\'s': ['bosom'], 'night\'s': ['night'], 'Night\'s': ['Night'], 'o\'er': ['over']}
    word_set = set({})
    word_counts = {}

    # here I go through the text row by row
    for row in text:
        words = get_words(row)
        for word in words:
            word = clean_word(word)

            # CASE IGNORE
            if ignore_case:
                word = word.lower()

            # check for special cases
            if word in list(special_cases.keys()):
                cur_words = special_cases[word]
                for cur_w in cur_words:
                    count_word(cur_w, word_set, word_counts)
            else:
                count_word(word, word_set, word_counts)

    # dictionaries are sorted
    word_counts = dict(sorted(word_counts.items(), reverse=False, key=lambda item: item[0]))
    word_counts = dict(sorted(word_counts.items(), reverse=True, key=lambda item: item[1]))

    # PRINT LIST?
    if print_list:
        for key in word_counts.keys():
            print(key, word_counts[key])

    print(f'{len(word_counts)}/{sum(word_counts.values())}')
    return word_counts
