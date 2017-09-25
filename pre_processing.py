from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import re


# Sentence Tokenization
def sentence_tokenize_of_review(file):
    """
    :param file:
    :return: file after sentence tokenize
    """
    return sent_tokenize(file)


def review_cleanup_labeled_data(sentences):
    """
    Cleaning up the review (removing explicitly mentioned product aspect and their sentiment score
    :param sentences:
    :return: cleaned manually labeled data
    """
    # Removing explict product aspect formed with three words and a hyperlink and sentiment score
    rg_exp_for_3plus = re.compile('(\\w+)(-)((?:[a-z][a-z]+))(\\s+)(\\w+)(\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    review_filtered = re.sub(rg_exp_for_3plus, '', sentences)

    # Removing explicit product aspect formed with two words and a hyperlink and sentiment score
    rg_exp_for_2plus = re.compile('(\\w+)(-)((?:[a-z][a-z]+))(\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    review_filtered_hyperlink = re.sub(rg_exp_for_2plus, '', review_filtered)

    # Removing explict product aspect with alphanumeric characters and sentiment score
    rg_exp_alphanumeric = re.compile('((?:[a-z][a-z]*[0-9]+[a-z0-9]*))(\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    # review = re.findall(rg_exp_alphanumeric, sentence_list)
    review_filtered_alphanumeric = re.sub(rg_exp_alphanumeric, '', review_filtered_hyperlink)

    # Removing explict product aspect with two words separated with space and sentiment score
    rg_exp_two_words_aspects = re.compile('(\\w+)(\\s+)(\\w+)(\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    review_filtered_two_words_aspects = re.sub(rg_exp_two_words_aspects, '', review_filtered_alphanumeric)

    # Removing explict product aspect with single words and sentiment score
    rg_exp_single_words_aspects = re.compile('(\\w+)(\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    review_filtered_single_words_aspects = re.sub(rg_exp_single_words_aspects, '', review_filtered_two_words_aspects)

    return review_filtered_single_words_aspects


def review_cleanup_symbols(sentences):
    # Removing [#,{, }] symbols
    reg_exp_multi_symbol = re.compile('[#\\{\\}]', re.IGNORECASE | re.DOTALL)
    review_filtered_multi_symbol = re.sub(reg_exp_multi_symbol, '', sentences)

    # Removing =) symbols
    reg_exp_symbol1 = re.compile('(=\\))', re.IGNORECASE | re.DOTALL)
    review_filtered_symbol1 = re.sub(reg_exp_symbol1, '', review_filtered_multi_symbol)

    # Removing ... symbols
    reg_exp_symbol2 = re.compile('(\\.)(\\.)(\\.)', re.IGNORECASE | re.DOTALL)
    final_filtered_review = re.sub(reg_exp_symbol2, '', review_filtered_symbol1)

    # Removing , symbols at the starting of line
    # reg_exp_symbol3 = re.compile('[^,]', re.IGNORECASE | re.DOTALL)
    # reg_exp_symbol3 = re.compile('(,)((?:[a-z][a-z]+))', re.IGNORECASE | re.DOTALL)
    # review = re.findall(reg_exp_symbol3, final_filtered_review)
     #print(review)

    return final_filtered_review

# Word Tokenization
def word_tokenize_review(sentence_list):
    """
    :param sentence_list:
    :return: list of word tokenize
    """
    return [word_tokenize(sentences) for sentences in sentence_list]


# POS tagging
def pos_tagging(tokeninzed_sentence_list):
    """

    :param tokeninzed_sentence_list: word tokenize consumer review
    :return: List of word with POS tagging
    """
    pos_tagged = [pos_tag(sentences) for sentences in tokeninzed_sentence_list]
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


def lemmatization(product_aspect_list):
    """
    Normalizing words as many variations of words carry same meaning
    :param product_aspect_list:
    :return: combination of product aspect that has the same meaning
    """
    product_aspect_dictionary={}
    lemmatizer = WordNetLemmatizer()
    for lemma in product_aspect_list:
        # count=lemma[1]
        lemma_word = lemmatizer.lemmatize(lemma[0])
        if lemma_word in product_aspect_dictionary:
            for key, value in product_aspect_dictionary.items():
                product_aspect_dictionary[key] = value + lemma[1]
        else:
            product_aspect_dictionary[lemma_word] = lemma[1]

    product_aspect = sorted(product_aspect_dictionary.items(), key=lambda x: x[1], reverse=True)
    return product_aspect


def get_synonym_sets(noun_list):

    product_aspects_dictionary = {}
    for noun, count in noun_list:
        synonyms = []
        in_list = []
        not_in_list=[]
        for syn in wordnet.synsets(noun):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        print(synonyms)
        for nn in noun_list:
            for ss in synonyms:
                print(ss)
                if nn in synonyms:
                    in_list.append(nn)
                else:
                    not_in_list.append(nn)
    print(in_list)
    print(not_in_list)


    #comparing words
    first_word = wordnet.synset('image.n.01')

    second_word = wordnet.synset('picture.n.01')
    print(first_word.wup_similarity(second_word))
    #print(synonyms)

    hyponyms_list = []
    for syn in wordnet.synsets("phone"):
        hyponyms_list.append(list(syn.closure(lambda h: h.hyponyms())))
    #print(hyponyms_list)