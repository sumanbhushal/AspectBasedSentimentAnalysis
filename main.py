import config, database, product_aspects_extraction, pre_processing, opinion_extraction, msc, pos_tagging, \
    aspect_pruning, n_grams, StanfordNLPServer, cbs_apriori
import nltk
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

    ### Stanford POS tagging
    # pos_tagged_sentences_list = pos_tagging.stanford_pos_tagging(sentence_list)
    # database.insert_postagged_sent_into_db(pos_tagged_sentences_list)
    fetch_pos_tagged_sentences_list = database.fetach_pos_tagged_sentence()
    # for pos_sent in pos_tagged_sentences_list:
    #     msc.write_to_file('stanford_pos_tagged_sentences.txt', str(pos_sent) + '\n')


    ### geting Nouns
    nouns_list = product_aspects_extraction.extract_nouns_from_standford_pos(fetch_pos_tagged_sentences_list)
    noun_list_per_sent = product_aspects_extraction.noun_chunking_for_stanford_pos(fetch_pos_tagged_sentences_list)
    # database.insert_nouns_per_sentence_into_db(noun_list_per_sent)

    # Stopwords
    noun_list_without_stopwords = pre_processing.filter_stopwords(nouns_list)
    # print("Stop Words",len(noun_list_without_stopwords), noun_list_without_stopwords)
    # database.insert_candidate_aspect_into_db(noun_list_without_stopwords)
    # database.insert_single_candidate_aspect_per_row(noun_list_without_stopwords)


    # apriori algorithim for frequent itemsets
    # cbs_apriori.cbs_apriori_itemset()
    frequent_itemsets = database.fetch_frequent_itemsets()

    ### Aspect Pruning
    product_aspect_after_compact_pruning = aspect_pruning.compactness_pruning()
    # database.insert_features_after_compactness_pruning(product_aspect_after_compact_pruning)
    product_aspect_after_redundancy_pruning = aspect_pruning.redundancy_pruning()
    print("After Pruning", len(product_aspect_after_redundancy_pruning), product_aspect_after_redundancy_pruning)

    # Lemmatization
    lemmatized = pre_processing.lemmatization(product_aspect_after_redundancy_pruning)
    print("Lemma", len(lemmatized), lemmatized)
    #
    # # Synonyms resolution
    # product_list = pre_processing.get_synonyms_set(lemmatized)
    # # print(len(product_list), product_list)


    ### Chunking to get the candidate product aspects
    # noun_list_per_sent = product_aspects_extraction.noun_chunking_for_stanford_pos(pos_tagged_sentences_list)
    # adj_noun_list = product_aspects_extraction.adj_noun_chunking_for_stanford_pos(pos_tagged_sentences_list)
    # adjective_list = product_aspects_extraction.adj_chunking_for_stanford_pos(pos_tagged_sentences_list)
    # noun_verb = product_aspects_extraction.noun_verb_chunking_for_stanford_pos(pos_tagged_sentences_list)
    # verb_noun = product_aspects_extraction.verb_noun_chunking_for_stanford_pos(pos_tagged_sentences_list)
    # # # print(len(noun_verb), noun_verb)
    # print(len(verb_noun), verb_noun)




    ### ngrams
    # n_grams.generate_unigram(word_tokenize_review_list)
    # n_grams.evaluation_matrix_with_unigram()
    # n_grams.generate_bigram(word_tokenize_review_list)
    # n_grams.evaluation_matrix_with_bigrams()
    # msc.generate_tigram(word_tokenize_review_list)
    # msc.generate_quadgram(word_tokenize_review_list)
    # msc.generate_pentagram(word_tokenize_review_list)

    ### Chunking
    #noun_list_with_chunking= product_aspects_extraction.noun_chunking(pos_tagged_sentences_list)
    # database.insert_candidate_aspect_into_db(noun_list_with_chunking)

    # Get candidate aspect from database
    # candidate_aspect_list = database.fetch_candidate_aspects_with_sentence_count()
    # print(candidate_aspect_list)

    ### Aspect Pruning
    # product_aspect_after_redundancy_pruning = aspect_pruning.redundancy_pruning()
    # print(product_aspect_after_redundancy_pruning)

    ### Extract Manual labeled aspect and write to file
    # manual_labeled_product_aspect = msc.extract_manual_labeled_aspect(review_list)
    # msc.generate_unique_list_of_manual_labeled_aspect("product_aspects_Nikon coolpix 4300")+96352854


    ### Evaluations
    precision = evaluation_matrix.precision(lemmatized)
    recall = evaluation_matrix.recall(lemmatized)
    f_measure = evaluation_matrix.f_measure(precision, recall)

    ### Extracting Opinion and Generating Opinion summary
    # op_list = opinion_extraction.extract_opinon_of_feature(pos_tagged_sentences_list)

    # sentence_list = pre_processing.sentence_tokenize_of_review(cleanup_review)
    # # write_to_file('review.txt', sentence_list)
    # pos_tagged_sentences_list = pos_tagging.pos_tagging(word_tokenize_review_list)
    # noun_list = product_aspects_extraction.noun_chunking(pos_tagged_sentences_list)

    # # opinion_list = opinion_extraction.opinion_from_tagged_sents(pos_tagged_sentences_list)


    # print(len(noun_list_without_stopwords),noun_list_without_stopwords)
    # # pre_processing.get_synonym_sets()
    # # print(len(noun_list_without_stopwords),noun_list_without_stopwords)
    # # calculate_relative_frequency_tags(pos_tagged_sentences_list)
    #
    # aspect_notin_noun_list=[]
    # aspect_in_noun_list = []


    # print(len(manual_labeled_product_aspect), manual_labeled_product_aspect)
    # for asp, cnt in noun_list:
    #     aspect_in_noun_list.append(asp)
    #
    # for aspect, count in manual_labeled_product_aspect:
    #     if aspect not in aspect_in_noun_list:
    #         aspect_notin_noun_list.append(aspect)
    # print(len(aspect_notin_noun_list),aspect_notin_noun_list)


    # Extracting manual labelled features from the file
    # my_manual_list = msc.extract_new_manual_labeled_aspect()
    # for aspect, count in my_manual_list:
    #     msc.write_to_file('my_product_aspects_list_router.txt', aspect + '\n')
if __name__ == '__main__':
    main()
