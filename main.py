import config, database, product_aspects_extraction, pre_processing, opinion_extraction, msc, pos_tagging, aspect_pruning
import nltk
import evaluation_matrix

def read_file():
    """
    Read file with review contents
    :return: content of file
    """
    file = open(config.Datasets_path + "Hitachi router.txt", "r").read()
    return file


def main():
    review_list = read_file()
    # sentence_list = database.fetch_sentences_from_review(review_list)
    sentence_list = database.fetch_sentence_from_sentence_table()
    word_tokenize_review_list = pre_processing.word_tokenize_review(sentence_list)
    # pos_tagged_review_list = pos_tagging.standford_pos_tagging(word_tokenize_review_list)
    pos_tagged_review_list = database.fetach_pos_tagged_sentence()
    # pos_tagged_review_list = pos_tagging.pos_tagging(word_tokenize_review_list)
    print(pos_tagged_review_list)
    noun_list = product_aspects_extraction.extract_noun(pos_tagged_review_list)

    print(len(noun_list), noun_list)
    # database.insert_postagged_sent_into_db(pos_tagged_review_list)
    # msc.generate_bigram(word_tokenize_review_list)


    #noun_list_with_chunking= product_aspects_extraction.noun_chunking(pos_tagged_review_list)
    #database.insert_candidate_aspect_into_db(noun_list_with_chunking)
    # aspect_pruning.redundancy_pruning()
    #print(len(noun_list_with_chunking), noun_list_with_chunking)

    # sentence_list = pre_processing.sentence_tokenize_of_review(cleanup_review)
    # # write_to_file('review.txt', sentence_list)
    # pos_tagged_review_list = pos_tagging.pos_tagging(word_tokenize_review_list)
    # noun_list = product_aspects_extraction.noun_chunking(pos_tagged_review_list)
    # noun_list_without_stopwords = pre_processing.filter_stopwords(noun_list)
    # lemmatized = pre_processing.lemmatization(noun_list_without_stopwords)
    # product_list = pre_processing.get_synonyms_set(lemmatized)
    #
    ##op_list = opinion_extraction.extract_opinon_of_feature(pos_tagged_review_list)
    # # opinion_list = opinion_extraction.opinion_from_tagged_sents(pos_tagged_review_list)

    # precision = evaluation_matrix.recall(noun_list)
    # print(len(noun_list_without_stopwords),noun_list_without_stopwords)
    # # pre_processing.get_synonym_sets()
    # # print(len(noun_list_without_stopwords),noun_list_without_stopwords)
    # # calculate_relative_frequency_tags(pos_tagged_review_list)
    #
    # aspect_notin_noun_list=[]
    # aspect_in_noun_list = []
    # manual_labeled_product_aspect = msc.extract_manual_labeled_aspect(review_list)
    # print(len(noun_list), noun_list)
    # print(len(manual_labeled_product_aspect), manual_labeled_product_aspect)
    # for asp, cnt in noun_list:
    #     aspect_in_noun_list.append(asp)
    #
    # for aspect, count in manual_labeled_product_aspect:
    #     if aspect not in aspect_in_noun_list:
    #         aspect_notin_noun_list.append(aspect)
    # print(len(aspect_notin_noun_list),aspect_notin_noun_list)
    # for aspect, count in manual_labeled_product_aspect:
        # print(aspect, count)
        # write_to_file('product_aspects_Hitachi router.txt', aspect + '\n')

    # Extracting manual labelled features from the file
    # my_manual_list = msc.extract_new_manual_labeled_aspect()
    # for aspect, count in my_manual_list:
    #     msc.write_to_file('my_product_aspects_list_router.txt', aspect + '\n')
if __name__ == '__main__':
    main()
