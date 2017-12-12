import config, database, product_aspects_extraction, pre_processing, opinion_extraction, msc, pos_tagging, \
    aspect_pruning, n_grams, StanfordNLPServer, cbs_apriori, wikipedia_crawler
import nltk, re
import evaluation_matrix

def read_file():
    """
    Read file with review contents
    :return: content of file
    """
    file = open(config.DATASETS_PATH + "Canon G3.txt", "r").read()
    return file


def main():
    review_list = read_file()
    # sentence_list = database.fetch_sentences_from_review(review_list)
    sentence_list = database.fetch_sentence_from_sentence_table()

    pre_processing.pronoun_resolution(sentence_list)
    ### Stanford POS tagging
    # pos_tagged_sentences_list = pos_tagging.stanford_pos_tagging(sentence_list)
    # database.insert_postagged_sent_into_db(pos_tagged_sentences_list)
    # pos_tagged_sentences_list = database.fetach_pos_tagged_sentence()
    # for pos_sent in pos_tagged_sentences_list:
    #     msc.write_to_file('stanford_pos_tagged_sentences.txt', str(pos_sent) + '\n')


    ### Extracting Nouns and Noun phrases
    # noun_nounphrases_per_sent = product_aspects_extraction.noun_chunking_for_stanford_pos(pos_tagged_sentences_list)
    # print(len(noun_nounphrases_per_sent), noun_nounphrases_per_sent)

    # insert noun list and noun_chunk per sentence
    # # database.insert_nouns_chunks_per_sentence_into_db(noun_nounphrases_per_sent)
    # database.insert_nouns_list_per_sentence_into_db(noun_nounphrases_per_sent)

    # database.insert_single_candidate_aspect_per_row(noun_nounphrases_per_sent)
    # # database.insert_single_noun_chunk_per_row(noun_nounphrases_per_sent)

    # # apriori algorithim for frequent itemsets
    # cbs_apriori.cbs_apriori_itemset()
    # frequent_itemsets = cbs_apriori.frequent_itemset_from_db()
    # print(len(frequent_itemsets), frequent_itemsets)

    # wiki_feature_list = wikipedia_crawler.product_features_from_wikipedia()
    # print("wiki", len(wiki_feature_list), wiki_feature_list)

    ## Aspect Pruning
    # product_aspect_after_compact_pruning = aspect_pruning.compactness_pruning()
    # database.insert_features_after_compactness_pruning(product_aspect_after_compact_pruning)
    # product_aspect_after_redundancy_pruning = aspect_pruning.redundancy_pruning()
    # # print("After Pruning", len(product_aspect_after_redundancy_pruning), product_aspect_after_redundancy_pruning)

    # Lemmatization
    # lemmatized = pre_processing.lemmatization(frequent_itemsets)

    # final_feature_list = list(set(wiki_feature_list + lemmatized))
    # print("Final list", len(final_feature_list), final_feature_list)
    # # # Synonyms resolution
    # product_list = pre_processing.get_synonyms_set(lemmatized)
    # print(len(product_list), product_list)
    #
    #
    # ### Extract Manual labeled aspect and write to file
    # manual_labeled_product_aspect = msc.extract_manual_labeled_aspect(review_list)
    #
    # # msc.generate_unique_list_of_manual_labeled_aspect("product_aspects_Nikon coolpix 4300")
    # new_list = []
    # for word, count in manual_labeled_product_aspect:
    #     if count > 5:
    #         # msc.write_to_file('CanonG3_feature_list.txt', word + '\n')
    #         new_list.append(word)
    #
    # print("Mannual Labeled data", len(new_list), new_list)

    ### Evaluations
    # precision = evaluation_matrix.precision(lemmatized)
    # recall = evaluation_matrix.recall(lemmatized)
    # f_measure = evaluation_matrix.f_measure(precision, recall)

    # ### Extracting Opinion and Generating Opinion summary
    # # op_list = opinion_extraction.extract_opinon_of_feature(pos_tagged_sentences_list)
    #
    #
    # # # calculate_relative_frequency_tags(pos_tagged_sentences_list)
    # #
    # # aspect_notin_noun_list=[]
    # # aspect_in_noun_list = []
    #
    #
    # # for asp, cnt in noun_list:
    # #     aspect_in_noun_list.append(asp)
    # #
    # # for aspect, count in manual_labeled_product_aspect:
    # #     if aspect not in aspect_in_noun_list:
    # #         aspect_notin_noun_list.append(aspect)
    # # print(len(aspect_notin_noun_list),aspect_notin_noun_list)
    #
    #
    # # Extracting manual labelled features from the file
    # # my_manual_list = msc.extract_new_manual_labeled_aspect()
    # # for aspect, count in my_manual_list:
    # #     msc.write_to_file('my_product_aspects_list_router.txt', aspect + '\n')
if __name__ == '__main__':
    main()
