import database, pre_processing, evaluation_matrix
from nltk.util import ngrams

def generate_unigram(tokenized_sentence_list):
    stopword_list = pre_processing.filter_stopwords(tokenized_sentence_list)
    database.trucate_table('unigram')
    unigrams = []
    for review_id, sent_id, sent in stopword_list:
        unigrams = list(ngrams(sent, 1))
        database.insert_unigrams_into_db(review_id, sent_id, unigrams)


def evaluation_matrix_with_unigram():
    unigram_list=database.fetch_unigrams()
    precision = evaluation_matrix.precision(unigram_list)
    recall = evaluation_matrix.recall(unigram_list)
    f_measure = evaluation_matrix.f_measure(precision, recall)


def generate_bigram(tokenized_sentence_list):
    stopword_list = pre_processing.filter_stopwords(tokenized_sentence_list)
    database.trucate_table('bigrams')
    bigrams = []
    for review_id, sent_id, sent in stopword_list:
        bigrams = list(ngrams(sent, 2))
        database.insert_bigrams_into_db(review_id, sent_id, bigrams)


def evaluation_matrix_with_bigrams():
    bigram_list=database.fetch_bigrams()
    bg_list = []
    for count, bg in bigram_list:
        word = eval(bg)
        combine_word = ' '.join(word)
        word_with_count = (count, combine_word)
        bg_list.append(word_with_count)
    print(bg_list)

    precision = evaluation_matrix.precision(bg_list)
    recall = evaluation_matrix.recall(bg_list)
    f_measure = evaluation_matrix.f_measure(precision, recall)

def generate_tigram(tokenized_sentence_list):
    database.trucate_table('trigrams')
    trigrams = []
    for review_id, sent_id, sent in tokenized_sentence_list:
        trigrams = list(ngrams(sent, 3))
        database.insert_trigrams_into_db(review_id, sent_id, trigrams)


def generate_quadgram(tokenized_sentence_list):
    database.trucate_table('quadgrams')
    quadgrams = []
    for review_id, sent_id, sent in tokenized_sentence_list:
        quadgrams = list(ngrams(sent, 4))
        database.insert_quadgrams_into_db(review_id, sent_id, quadgrams)


def generate_pentagram(tokenized_sentence_list):
    database.trucate_table('pentagrams')
    pentagrams = []
    for review_id, sent_id, sent in tokenized_sentence_list:
        pentagrams = list(ngrams(sent, 5))
        database.insert_pentagrams_into_db(review_id, sent_id, pentagrams)