import nltk
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet


def extract_opinion(pos_tagged_sentence_list):
    adjective_list = []
    chunkRegExpress = r"""Opinion: {<JJ.*>+}"""
    chunkParsar = nltk.RegexpParser(chunkRegExpress)
    for pos_tagged_content in pos_tagged_sentence_list:
        chunked = chunkParsar.parse(pos_tagged_content)
        # chunked.draw()
        # print(chunked)
        for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'Opinion'):
            adjective_list.append(" ".join(word for word, pos in subtree.leaves()).lower())
    print(len(adjective_list),adjective_list)


def opinion_from_tagged_sents(pos_tagged_sentences):
    opinion_list=[]
    for pos_taged_sents in pos_tagged_sentences:
        for word, pos in pos_taged_sents:
            if pos =='JJ' or pos =='JJR' or pos == 'JJS':
                opinion_list.append(word)
    print(len(opinion_list),opinion_list)

# WordNet to get the syns set and use SentiWordNet to find the orientation of the word
def word_orientation(inputWord):
    syns = wordnet.synsets(inputWord)
    if (len(syns) != 0):
        word = syns[0].name()
        word_orientation = sentiwordnet.senti_synset(word)
        #print(word_orientation)
        #print(word_orientation.pos_score())
    #print(syns[0])

word_orientation('good')
