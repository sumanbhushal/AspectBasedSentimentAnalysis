import config, database, product_aspects_extraction, opinion_extraction,\
    pos_tagging, aspect_pruning, cbs_apriori, wikipedia_crawler
import evaluation_matrix
from datetime import datetime


def read_file():
    """
    Read file with review contents
    :return: content of file
    """
    file = open(config.DATASETS_PATH + "Canon G3-[.txt", "r").read()
    return file


def main():
    start_time = datetime.now()
    """Read file with reviews """
    review_list = read_file()

    """Extract each sentence from review, pre-process and store in database"""
    sentence_list = database.fetch_sentences_from_review(review_list)
    # sentence_list = database.fetch_sentence_from_sentence_table()

    """Extract Manual annotated aspect also with minimum sentence count """
    # msc.extract_manual_annotated_aspect("Canon G3", review_list)
    # msc.extract_manual_annotated_asp_min_rev_sent_count("Canon G3", review_list)

    """Stanford POS tagging and storing in database"""
    pos_tagging.stanford_pos_tagging(sentence_list)

    """Extracting Nouns, Noun phrases and Adjective-Noun phrases and store in database as transaction"""
    product_aspects_extraction.noun_chunking_for_stanford_pos()

    """Apriori algorithim for frequent itemsets"""
    cbs_apriori.cbs_apriori_itemset()
    cbs_apriori.frequent_itemset_from_db()

    """Wikipedia Crawling to get the product aspects"""
    domain_name, wiki_feature_list = wikipedia_crawler.product_features_from_wikipedia()

    """Aspect Pruning (Compactness pruning)"""
    aspect_pruning.compactness_pruning()

    # Removing aspects from the candidate frequent aspect list that matches aspects form Wikipedia
    candidate_aspect_filtered_wiki_list = []
    candidate_product_aspect = database.fetch_freatures_after_compactness_pruning()
    for can_asp in candidate_product_aspect:
        if can_asp not in wiki_feature_list:
            candidate_aspect_filtered_wiki_list.append(can_asp)

    """Aspect Pruning (Redundancy pruning)"""
    product_aspect_after_redundancy_pruning = aspect_pruning.redundancy_pruning(candidate_aspect_filtered_wiki_list)

    """Final Product Aspect List ( Wiki list + after pruning List )"""
    final_feature_list = list(set(wiki_feature_list + product_aspect_after_redundancy_pruning))
    product_aspects_list_final = []
    for product_asp in final_feature_list:
        product_aspects_list_final.append(" ".join(product_asp.split("_")))
    database.insert_final_product_aspect_list(product_aspects_list_final)

    """Evaluations"""
    # precision = evaluation_matrix.precision(final_feature_list)
    # recall = evaluation_matrix.recall(final_feature_list)
    # evaluation_matrix.f_measure(precision, recall)

    """Sentiment Orientation Classification and Generating Opinion Summary"""
    opinion_extraction.genearate_summary_feature_opinion()

    """Calculating total time duration required generate opinion summary"""
    end_time = datetime.now()
    execution_time = end_time - start_time
    print("Duration. {} ".format(execution_time))
    database.insert_duration_time(execution_time)

if __name__ == '__main__':
    main()
