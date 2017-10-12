import config, product_aspects_extraction, pre_processing, opinion_extraction, msc
import nltk


def read_file():
    """
    Read file with review contents
    :return: content of file
    """
    file = open(config.Datasets_path + "Hitachi router.txt", "r").read()
    return file


def write_to_file(filename, output_content):
    with open(config.Output_file_path + filename, 'a') as output:
        for text in output_content:
            output.write(text)


def calculate_relative_frequency_tags(pos_tagged_review_list):
    """
    Calculation to estimate the relative frequency of different tags following a certain tag
    :param pos_tagged_review_list:
    :return:
    """
    tags_relative_frequency = []
    tags_relative_frequency_dictionary = {}
    pos_tags = ['NN', 'JJ', 'VB', 'DT', '.', 'VBP']
    print(pos_tagged_review_list)
    for tags in pos_tags:
        for word_pos in pos_tagged_review_list:
            for word, pos in word_pos:
                if pos in pos_tags:
                    word_pos_position = (word, pos)
                    prev_pos_current_pos = ( word_pos[word_pos.index(word_pos_position) - 1][1], pos)
                    tags_relative_frequency.append(prev_pos_current_pos)

    for current_prev_tag in tags_relative_frequency:
        if (tags_relative_frequency_dictionary.keys()!= current_prev_tag):
            tags_relative_frequency_dictionary[current_prev_tag] = tags_relative_frequency.count(current_prev_tag)

        combine_tag_frequency = sorted(tags_relative_frequency_dictionary.items(), key=lambda x: x[1], reverse=True)
    print(len(combine_tag_frequency), combine_tag_frequency)


def main():
    review_list = read_file()
    # pre_processing.extract_each_review(review_list)
    review_filter_labeled_data = pre_processing.review_cleanup_labeled_data(review_list)
    cleanup_review = pre_processing.review_cleanup_symbols(review_filter_labeled_data)
    sentence_list = pre_processing.sentence_tokenize_of_review(cleanup_review)
    # write_to_file('review.txt', sentence_list)
    word_tokenize_review_list = pre_processing.word_tokenize_review(sentence_list)
    pos_tagged_review_list = pre_processing.pos_tagging(word_tokenize_review_list)
    noun_list = product_aspects_extraction.noun_chunking(pos_tagged_review_list)
    noun_list_without_stopwords = pre_processing.filter_stopwords(noun_list)
    lemmatized = pre_processing.lemmatization(noun_list_without_stopwords)
    product_list = pre_processing.get_synonyms_set(lemmatized)

    # op_list = opinion_extraction.extract_opinion(pos_tagged_review_list)
    # opinion_list = opinion_extraction.opinion_from_tagged_sents(pos_tagged_review_list)

    # precision = evaluation_matrix.precision(len(lemmatized), 179)
    print(len(noun_list_without_stopwords),noun_list_without_stopwords)
    # pre_processing.get_synonym_sets()
    # print(len(noun_list_without_stopwords),noun_list_without_stopwords)
    # calculate_relative_frequency_tags(pos_tagged_review_list)

    aspect_notin_noun_list=[]
    aspect_in_noun_list = []
    manual_labeled_product_aspect = msc.extract_manual_labeled_aspect(review_list)
    print(len(product_list), product_list)
    print(len(manual_labeled_product_aspect), manual_labeled_product_aspect)
    for asp, cnt in noun_list_without_stopwords:
        aspect_in_noun_list.append(asp)

    for aspect, count in manual_labeled_product_aspect:
        if aspect not in aspect_in_noun_list:
            aspect_notin_noun_list.append(aspect)
    print(len(aspect_notin_noun_list),aspect_notin_noun_list)
    # for aspect, count in manual_labeled_product_aspect:
        # print(aspect, count)
        # write_to_file('product_aspects_Hitachi router.txt', aspect + '\n')

if __name__ == '__main__':
    main()
