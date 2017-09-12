from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.corpus import stopwords


# Sentence Tokenization
def sentence_tokenize_of_review(file):
    """
    :param file:
    :return: file after sentence tokenize
    """
    return sent_tokenize(file)


# Word Tokenization
def word_tokenize_review(sentence_list):
    """
    :param sentence_list:
    :return: list of word tokenize
    """
    return word_tokenize(sentence_list)


# POS tagging
def pos_tagging(consumer_review):
    """

    :param consumer_review: word tokenize consumer review
    :return: List of word with POS tagging
    """
    pos_tagged = pos_tag(consumer_review)
    return pos_tagged


# Filter Stopwords - (English)
def filter_stopwords(product_aspect_list):
    """
    :param product_aspect_list:
    :return: product aspect list after filtering stopwords
    """

    stop_words = set(stopwords.words('english'))
    aspect_list_without_stopwords = []
    for words in product_aspect_list:
        if words[0] not in stop_words:
            aspect_list_without_stopwords.append(words)
    return aspect_list_without_stopwords
