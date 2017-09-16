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


def calculate_relative_frequency_tags(pos_tagged_review_list):
    """
    Calculation to estimate the relative frequency of different tags following a certain tag
    :param pos_tagged_review_list:
    :return:
    """
    tags_relative_frequency = []
    pos_tags =['NN', 'JJ', 'VB' 'DT', '.']
    # review_to_dict=dict(pos_tagged_review_list)
    word_length = ''
    print(pos_tagged_review_list)
    for tags in pos_tags:
        for word in pos_tagged_review_list:
            if word[1] in tags:
                print("Current Tag: ",tags,"Prev Tag: ",pos_tagged_review_list[pos_tagged_review_list.index(word)-1][1])

    #
    # for word in review_to_dict:
    #     for key, value in word.items():
    #         for i in range(1, len(word)):
    #             print(value[i], value[i - 1])


        # if word[1] == 'NN':
        #     print(zip((word[1:], word)))
        #     tags_relative_frequency.append(word[0])
    print(tags_relative_frequency)



def main():
    review_list = read_file()
    sentence_list = pre_processing.sentence_tokenize_of_review(review_list)
    review_filter_labeled_data = pre_processing.review_cleanup_labeled_data(review_list)
    review_cleanup = pre_processing.review_cleanup_symbols(review_filter_labeled_data)
    print(review_cleanup)
    # word_tokenize_review_list = pre_processing.word_tokenize_review(sentence_list)
    # print(len(word_tokenize_review_list),word_tokenize_review_list)
    # pos_tagged_review_list = pre_processing.pos_tagging(word_tokenize_review_list)
    # noun_list = product_aspects_extraction.noun_chunking(pos_tagged_review_list)
    # noun_list_without_stopwords = product_aspects_extraction.filter_stopword(noun_list)
    # print(noun_list_without_stopwords)


if __name__ == '__main__':
    main()