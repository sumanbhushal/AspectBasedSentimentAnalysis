import config, database, product_aspects_extraction, pre_processing, opinion_extraction, msc, pos_tagging
import nltk


def read_file():
    """
    Read file with review contents
    :return: content of file
    """
    file = open(config.Datasets_path + "Hitachi router.txt", "r").read()
    return file


def main():
    # review_list = read_file()
    # sentence_list = database.fetch_sentences_from_review(review_list)
    sentence_list = database.fetch_sentence_from_sentence_table()
    word_tokenize_review_list = pre_processing.word_tokenize_review(sentence_list)
    pos_tagged_review_list = pos_tagging.pos_tagging(word_tokenize_review_list)
    #noun_list = product_aspects_extraction.extract_noun(pos_tagged_review_list)
    noun_list_with_chunking= product_aspects_extraction.noun_chunking(pos_tagged_review_list)
    database.insert_candidate_aspect_into_db(noun_list_with_chunking)
    #print(len(noun_list_with_chunking), noun_list_with_chunking)

    # sentence_list = pre_processing.sentence_tokenize_of_review(cleanup_review)
    # # write_to_file('review.txt', sentence_list)
    # pos_tagged_review_list = pos_tagging.pos_tagging(word_tokenize_review_list)
    # noun_list = product_aspects_extraction.noun_chunking(pos_tagged_review_list)
    # noun_list_without_stopwords = pre_processing.filter_stopwords(noun_list)
    # lemmatized = pre_processing.lemmatization(noun_list_without_stopwords)
    # product_list = pre_processing.get_synonyms_set(lemmatized)
    #
    # # op_list = opinion_extraction.extract_opinion(pos_tagged_review_list)
    # # opinion_list = opinion_extraction.opinion_from_tagged_sents(pos_tagged_review_list)
    #
    # # precision = evaluation_matrix.precision(len(lemmatized), 179)
    # print(len(noun_list_without_stopwords),noun_list_without_stopwords)
    # # pre_processing.get_synonym_sets()
    # # print(len(noun_list_without_stopwords),noun_list_without_stopwords)
    # # calculate_relative_frequency_tags(pos_tagged_review_list)
    #
    # aspect_notin_noun_list=[]
    # aspect_in_noun_list = []
    # manual_labeled_product_aspect = msc.extract_manual_labeled_aspect(review_list)
    # print(len(product_list), product_list)
    # print(len(manual_labeled_product_aspect), manual_labeled_product_aspect)
    # for asp, cnt in noun_list_without_stopwords:
    #     aspect_in_noun_list.append(asp)
    #
    # for aspect, count in manual_labeled_product_aspect:
    #     if aspect not in aspect_in_noun_list:
    #         aspect_notin_noun_list.append(aspect)
    # print(len(aspect_notin_noun_list),aspect_notin_noun_list)
    # for aspect, count in manual_labeled_product_aspect:
        # print(aspect, count)
        # write_to_file('product_aspects_Hitachi router.txt', aspect + '\n')

if __name__ == '__main__':
    main()
