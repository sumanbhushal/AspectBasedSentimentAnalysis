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

def extract_manual_annotated_aspect(filename, review_list):
    ### Extract Manual labeled aspect and write to file
    manual_labeled_product_aspect = msc.extract_manual_labeled_aspect(review_list)

    new_list = []
    for word, count in manual_labeled_product_aspect:
            msc.write_to_file(filename + "_ml.txt", word + '\n')
            new_list.append(word)
    print("Mannual Labeled data", len(new_list), new_list)


def extract_manual_annotated_asp_min_rev_sent_count(filename, review_list):
    ### Extract Manual labeled aspect and write to file
    manual_labeled_product_aspect = msc.extract_manual_labeled_aspect(review_list)
    number_of_sentences = len(database.fetch_sentence_from_sentence_table())
    min_sent_count = round(0.01* number_of_sentences)
    new_list = []
    for word, count in manual_labeled_product_aspect:
        if count > min_sent_count:
            msc.write_to_file(filename + "_ml_sent_count.txt", word + '\n')
            new_list.append(word)
    print("Mannual Labeled data With Sentence Count", len(new_list), new_list)

def main():
    review_list = read_file()

    """Extract each sentence from review, pre-process and store in database"""
    # sentence_list = database.fetch_sentences_from_review(review_list)
    # sentence_list = database.fetch_sentence_from_sentence_table()

    """Extract Manual annotated aspect also with minimum sentence count """
    # extract_manual_annotated_aspect("Canon G3", review_list)
    # extract_manual_annotated_asp_min_rev_sent_count("Canon G3", review_list)

    """Stanford POS tagging and storing in database"""
    # pos_tagging.stanford_pos_tagging(sentence_list)

    """Extracting Nouns, Noun phrases and Adjective-Noun phrases and store in database as transaction"""
    # noun_nounphrases_per_sent = product_aspects_extraction.noun_chunking_for_stanford_pos()

    """Apriori algorithim for frequent itemsets"""
    # cbs_apriori.cbs_apriori_itemset()
    frequent_itemsets = cbs_apriori.frequent_itemset_from_db()
    # print(len(frequent_itemsets), frequent_itemsets)

    """Wikipedia Crawling to get the product aspects"""
    domain_name, wiki_feature_list = wikipedia_crawler.product_features_from_wikipedia()
    # print("wiki", len(wiki_feature_list), wiki_feature_list)

    """Aspect Pruning (Compactness pruning, Redundancy pruning)"""
    aspect_pruning.compactness_pruning()
    candidate_aspect_filtered_wiki_list = []
    candidate_product_aspect = database.fetch_freatures_after_compactness_pruning()
    for can_asp in candidate_product_aspect:
        if can_asp not in wiki_feature_list:
            candidate_aspect_filtered_wiki_list.append(can_asp)
    product_aspect_after_redundancy_pruning = aspect_pruning.redundancy_pruning(candidate_aspect_filtered_wiki_list)

    # aspect_pruning.filter_aspect_based_on_domain_similarity(domain_name, product_aspect_after_redundancy_pruning )

    """Final Product Aspect List ( Wiki list + after pruning List"""
    final_feature_list = list(set(wiki_feature_list + product_aspect_after_redundancy_pruning))
    product_aspects_list_final = []
    for product_asp in final_feature_list:
        product_aspects_list_final.append(" ".join(product_asp.split("_")))
    print("Final list", len(product_aspects_list_final), product_aspects_list_final)


    """Evaluations"""
    # precision = evaluation_matrix.precision(final_feature_list)
    # recall = evaluation_matrix.recall(final_feature_list)
    # f_measure = evaluation_matrix.f_measure(precision, recall)

    # ### Extracting Opinion and Generating Opinion summary
    # # op_list = opinion_extraction.extract_opinon_of_feature(pos_tagged_sentences_list)

if __name__ == '__main__':
    main()
