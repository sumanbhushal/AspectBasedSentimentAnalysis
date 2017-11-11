import config, database, product_aspects_extraction, pre_processing, opinion_extraction, msc, pos_tagging, aspect_pruning, n_grams, StanfordNLPServer
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
    # word_tokenize_review_list = pre_processing.word_tokenize_review(sentence_list)

    # pos_tagged_review_list = pos_tagging.pos_tagging(word_tokenize_review_list)
    # noun_list = product_aspects_extraction.extract_noun(pos_tagged_review_list)

    ### Stanford POS tagging
    # pos_tagged_review_list = pos_tagging.stanford_pos_tagging(sentence_list)
    # database.insert_postagged_sent_into_db(pos_tagged_review_list)
    pos_tagged_review_list = database.fetach_pos_tagged_sentence()
    # for pos_sent in pos_tagged_review_list:
    #     msc.write_to_file('stanford_pos_tagged_sentences.txt', str(pos_sent) + '\n')

    ### Chunking to get the candidate product aspects
    noun_list_per_sent = product_aspects_extraction.noun_chunking_for_stanford_pos(pos_tagged_review_list)
    adj_noun_list = product_aspects_extraction.adj_noun_chunking_for_stanford_pos(pos_tagged_review_list)
    adjective_list = product_aspects_extraction.adj_chunking_for_stanford_pos(pos_tagged_review_list)
    noun_verb = product_aspects_extraction.noun_verb_chunking_for_stanford_pos(pos_tagged_review_list)
    verb_noun = product_aspects_extraction.verb_noun_chunking_for_stanford_pos(pos_tagged_review_list)
    # # print(len(noun_verb), noun_verb)
    # print(len(verb_noun), verb_noun)


    # Stopword
    noun_list_without_stopwords = pre_processing.filter_stopwords(verb_noun)
    # database.insert_single_candidate_aspect_per_row(noun_list_without_stopwords)
    # print(len(noun_list_without_stopwords), noun_list_without_stopwords)

    # # Lemmatization
    # lemmatized = pre_processing.lemmatization(noun_list_without_stopwords)
    #
    # # Synonyms resolution
    # product_list = pre_processing.get_synonyms_set(lemmatized)
    # # print(len(product_list), product_list)

    ### ngrams
    # n_grams.generate_unigram(word_tokenize_review_list)
    # n_grams.evaluation_matrix_with_unigram()
    # n_grams.generate_bigram(word_tokenize_review_list)
    # n_grams.evaluation_matrix_with_bigrams()
    # msc.generate_tigram(word_tokenize_review_list)
    # msc.generate_quadgram(word_tokenize_review_list)
    # msc.generate_pentagram(word_tokenize_review_list)

    ### Chunking
    #noun_list_with_chunking= product_aspects_extraction.noun_chunking(pos_tagged_review_list)
    # database.insert_candidate_aspect_into_db(noun_list_with_chunking)

    # Get candidate aspect from database
    candidate_aspect_list = database.fetch_candidate_aspects_with_sentence_count()

    ### Aspect Pruning
    product_aspect_after_redundancy_pruning = aspect_pruning.redundancy_pruning()
    print(product_aspect_after_redundancy_pruning)

    ### Extract Manual labeled aspect and write to file
    # manual_labeled_product_aspect = msc.extract_manual_labeled_aspect(review_list)
    # msc.generate_unique_list_of_manual_labeled_aspect("product_aspects_Nikon coolpix 4300")+96352854


    ### Evaluations
    precision = evaluation_matrix.precision(product_aspect_after_redundancy_pruning)
    recall = evaluation_matrix.recall(product_aspect_after_redundancy_pruning)
    f_measure = evaluation_matrix.f_measure(precision, recall)

    ### Extracting Opinion and Generating Opinion summary
    # op_list = opinion_extraction.extract_opinon_of_feature(pos_tagged_review_list)

    # sentence_list = pre_processing.sentence_tokenize_of_review(cleanup_review)
    # # write_to_file('review.txt', sentence_list)
    # pos_tagged_review_list = pos_tagging.pos_tagging(word_tokenize_review_list)
    # noun_list = product_aspects_extraction.noun_chunking(pos_tagged_review_list)

    # # opinion_list = opinion_extraction.opinion_from_tagged_sents(pos_tagged_review_list)


    # print(len(noun_list_without_stopwords),noun_list_without_stopwords)
    # # pre_processing.get_synonym_sets()
    # # print(len(noun_list_without_stopwords),noun_list_without_stopwords)
    # # calculate_relative_frequency_tags(pos_tagged_review_list)
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
