import nltk
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet

def generate_ngrams(input_text, n):
    ngram_list = []
    input = input_text.split(' ')
    for i in range(len(input) - n+1):
        ngram_list.append(input[i:i+n])
    #print(ngram_list)
    return ngram_list

generate_ngrams("this is test test test text.", 3)

#wordnet to get the syns set and use sentiwordnet to find the orientation of the word
def word_orientation(inputWord):
    syns = wordnet.synsets(inputWord)
    if (len(syns) != 0):
        word = syns[0].name()
        word_orientation = sentiwordnet.senti_synset(word)
        print(word_orientation)
        print(word_orientation.pos_score())
    print(syns[0])

word_orientation('good')
