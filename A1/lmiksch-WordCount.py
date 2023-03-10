import argparse
import re 

#input parameters
parser = argparse.ArgumentParser()
parser.add_argument("input", help="file name")
parser.add_argument("-l", "--list", action = "store_true", help="Returns a list of the words based on their occurences")
parser.add_argument("-I", "--ignore", action="store_true", help="ignore case when searching for items")
args = parser.parse_args()


input = args.input
list_arg = args.list
ignore_arg = args.ignore


#reading file into a list 
with open(input, "r") as f:
    word_list = []
    word_list.append(f.read().replace("\n"," "))
    

#corects words that end with n't and seperates them into prefix and 'not'

for i in range(len(word_list)):
    if re.match(r"\b\w+n't\b", word_list[i]):
        word_list[i:i+1] = [word_list[i][:-3], "not"]

#using regex to remove non alphabetical characters but keeps '
regex = re.compile("[^a-zA-Züäöß]")

for i,line in enumerate(word_list):

    word_list[i] = regex.sub(" ",line).strip()

#puts every word as an entry 
word_list = word_list[0].split()




#converting uppercase to lower case if -I is True
if ignore_arg == True:
    for i,line in enumerate(word_list):
        word_list[i] = word_list[i].lower()

#generating default output
if not list_arg:
    print(len(set(word_list)),"/",len(word_list))

#generating output if -l is given
if list_arg:
    word_dict = {}
    #puts each word into dict and if it's allready in there it increases the count by 1
    for word in word_list:
        if word not in word_dict.keys():
            word_dict[word] = 1
        else:
            word_dict[word] += 1 
    #sorts the dictionary based on the counts descending if two words have the same count they get order alphabetically
    word_dict = dict(sorted(word_dict.items(), key = lambda x:(-x[1],x[0])))

    
    for x in word_dict.keys():
        print(x,word_dict[x])



