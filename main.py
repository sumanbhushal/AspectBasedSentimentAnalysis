import config, product_aspects_extraction, pre_processing
import nltk
from nltk import sent_tokenize, word_tokenize


def read_file():
    """
    Read file with review contents
    :return: content of file
    """
    file = open(config.Datasets_path + "Canon PowerShot SD500.txt", "r").read()
    return file


def main():
    review_list = read_file()
    word_tokenize_review_list = pre_processing.word_tokenize_review(review_list)
    pos_tagged_review_list = pre_processing.pos_tagging(word_tokenize_review_list)
    noun_list = product_aspects_extraction.noun_chunking(pos_tagged_review_list)
    noun_list_without_stopwords = product_aspects_extraction.filter_stopword(noun_list)
    print(noun_list_without_stopwords)

if __name__ == '__main__':
    main()