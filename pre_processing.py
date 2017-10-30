import re
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer


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

    # Removing title [t]
    rg_exp_title = re.compile('(\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    review_filtered_title = re.sub(rg_exp_title, '', review_filtered_single_words_aspects)
    #print(re.findall(rg_exp_title, review_filtered_single_words_aspects), len(re.findall(rg_exp_title, review_filtered_single_words_aspects)))

    return review_filtered_title


def review_cleanup_symbols(sentences):
    # Removing [#,{, }] symbols
    reg_exp_main = re.compile('[^A-Za-z0-9^\n^\.^\"^\' ]+', re.IGNORECASE | re.DOTALL)
    # review_filtered_main = re.findall(reg_exp_main, sentences)
    review_filtered_main = re.sub(reg_exp_main, '', sentences)
    print(review_filtered_main)

    # Removing [#,{, }] symbols
    reg_exp_multi_symbol = re.compile('[#\\{\\}]', re.IGNORECASE | re.DOTALL)
    review_filtered_multi_symbol = re.sub(reg_exp_multi_symbol, '', sentences)

    # Removing =) symbols
    reg_exp_symbol1 = re.compile('(=\\))', re.IGNORECASE | re.DOTALL)
    review_filtered_symbol1 = re.sub(reg_exp_symbol1, '', review_filtered_multi_symbol)

    # Removing ... symbols
    reg_exp_symbol2 = re.compile('(\\.)(\\.)(\\.)', re.IGNORECASE | re.DOTALL)
    review_filtered_symbol2 = re.sub(reg_exp_symbol2, '', review_filtered_symbol1)

    # Removing ,,, symbols
    reg_exp_symbol3 = re.compile('(,)(,)(,)', re.IGNORECASE | re.DOTALL)
    review_filtered_symbol3 = re.sub(reg_exp_symbol3, '', review_filtered_symbol2)

    # Removing ,, symbols
    reg_exp_symbol4 = re.compile('(,)(,)', re.IGNORECASE | re.DOTALL)
    final_filtered_review = re.sub(reg_exp_symbol4, '', review_filtered_symbol3)


    # Removing , symbols at the starting of line
    # reg_exp_symbol3 = re.compile('[^,]', re.IGNORECASE | re.DOTALL)
    # reg_exp_symbol3 = re.compile('(,)((?:[a-z][a-z]+))', re.IGNORECASE | re.DOTALL)
    # review = re.findall(reg_exp_symbol3, final_filtered_review)
     #print(review)

    return final_filtered_review


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
    ids_tokenize_value = []
    for sent_id, review_id, sentences in sentence_list:
        sent_id = sent_id
        review_id = review_id
        word_tokenize_sent = word_tokenize(sentences)
        combine_value = (review_id, sent_id, word_tokenize_sent)
        ids_tokenize_value.append(combine_value)
    return ids_tokenize_value


# Filter Stopwords - (English)
def filter_stopwords(product_aspect_list):
    """
    :param product_aspect_list:
    :return: product aspect list after filtering stopwords
    """
    stop_words = set(stopwords.words('english'))
    stop_words.update('(', ')')
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
    product_aspect_dictionary = {}
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


def get_synonyms_set(noun_list):
    product_aspects_dictionary = {}
    noun_list_replacing_space = []
    for noun, count in noun_list:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        noun_list_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', noun)
        new_noun_count_pair = (noun_list_replacing_space_with_underscore, count)
        noun_list_replacing_space.append(new_noun_count_pair)
    # print(len(noun_list_replacing_space), noun_list_replacing_space)
    for noun, count in noun_list:
        synonyms = []
        for syn in wordnet.synsets(noun):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        #print(synonyms)
        if synonyms:
            for nn, cc in noun_list_replacing_space:
                if nn in synonyms:
                    noun_count_pair = (nn, cc)
                    replace_value = (noun, cc)
                    noun_list_replacing_space[noun_list_replacing_space.index(noun_count_pair)] = replace_value

    # print(len(noun_list), noun_list)
    for noun, count in noun_list_replacing_space:
        if noun in product_aspects_dictionary:
            product_aspects_dictionary[noun] = (product_aspects_dictionary[noun]) + count
        else:
            product_aspects_dictionary[noun] = count

    product_aspect = sorted(product_aspects_dictionary.items(), key=lambda x: x[1], reverse=True)
    # print(len(product_aspect),product_aspect)
    return product_aspect
