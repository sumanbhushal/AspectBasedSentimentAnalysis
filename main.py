import config, product_aspects_extraction
import nltk
from nltk import sent_tokenize, word_tokenize


def read_file():
    """
    Read file with review contents
    :return: content of file
    """
    file = open(config.Datasets_path + "Canon PowerShot SD500.txt", "r").read()
    return file


def sentence_tokenize_of_review(file):
    """
    :param file:
    :return: file after sentence tokenize
    """
    return sent_tokenize(file)


def word_tokenize_review(sentence_list):
    """
    :param sentence_list:
    :return: list of word tokenize
    """
    # word_tokenize_list=[]
    # for word in sentence_list:
    #     word_tokenize_list.append(word_tokenize(word))
    # return word_tokenize_list
    return word_tokenize(sentence_list)


#POS tagging
def pos_tagging(consumer_review):
    """

    :param consumer_review: word tokenize consumer review
    :return: List of word with POS tagging
    """
    pos_tagged = nltk.pos_tag(consumer_review)
    return pos_tagged


fileContent = read_file()
reviewSentenceList = sentence_tokenize_of_review(fileContent)

tokenizeReviewWordList = word_tokenize_review(fileContent)
pos_tagged_list=pos_tagging(tokenizeReviewWordList)
noun_list= product_aspects_extraction.noun_chunking(pos_tagged_list)
print(noun_list)
print(len(noun_list))
aspect_list_after_stopwords = product_aspects_extraction.filter_stopword(noun_list)
print(len(aspect_list_after_stopwords))
#print(noun_list)