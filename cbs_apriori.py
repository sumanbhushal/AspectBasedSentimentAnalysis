import database
from copy import deepcopy
from itertools import combinations


def cbs_apriori_itemset():
    Lk = {}
    items_in_transaction = []

    # Minimum support for Apriori algorithm (1% of total review sentence)
    number_of_sentences = len(database.fetch_sentence_from_sentence_table())
    min_sup = round(0.01*number_of_sentences)

    # Get candidate aspect from database
    transaction = database.fetch_nouns_per_sentence()
    for tran_id, review_id, sent_id, itm in transaction:
        for each_item in itm.split(','):
            items_in_transaction.append(each_item)

    # find the frequent 1-itemsets
    C1 = generate_1_itemset(items_in_transaction)
    L1 = prune(C1, min_sup)
    if L1 != '':
        database.insert_frequent_1_itemsets(L1)

    # find the frequent 2-itemsets
    C2 = generate_2_itemset(L1)
    Ct2 = scan_in_database(C2)
    Lk[2] = prune(Ct2, min_sup)
    if Lk[2] != '':
        database.insert_frequent_k_itemsets(Lk)

    # candidate_aspect_after_l2 = []
    # for key, value in Lk[2].items():
    #     for item in eval(key):
    #         if item not in candidate_aspect_after_l2:
    #             candidate_aspect_after_l2.append(item)
    #
    # Lk = {}
    # # find the frequent 3-itemsets
    # C3 = generate_3_itemset(candidate_aspect_after_l2)
    # Ct3 = scan_in_database(C3)
    # Lk[3] = prune(Ct3, min_sup)
    #
    # if Lk[3] != '':
    #     database.insert_frequent_k_itemsets(Lk)


def generate_1_itemset(items_in_transaction):
    """
    Generating frequent-1 itemset
    :param items_in_transaction: items in transaction
    :return: Dictionary of candidate 1-itemset with their count
    """
    C_1 = {}
    for item in items_in_transaction:
        if C_1.keys() != item:
            C_1[item] = items_in_transaction.count(item)
    return C_1


def generate_2_itemset(L):
    """
    Generating frequent-2 itemset
    :param L: frequent-1 itemset (L1)
    :return: List of candidate frequent-2 itemset
    """
    C_2 = []
    for i in combinations(L, 2):
        C_2.append(list(i))
    return list(C_2)


def generate_3_itemset(L):
    """
    Generating frequent-3 itemset
    :param L: frequent-2 itmeset
    :return: List of candidate frequent-3 itemset after prior knowledge filtering
    """
    C_3 = []
    for i in combinations(L, 3):
        if has_infrequent_subset(i):
            C_3.append(list(i))
    return list(C_3)


def has_infrequent_subset(k_itemset):
    """
    Checking subset of Ct is in L(k-1) frequent itemsets
    :param k_itemset:
    :return: boolean if all the subset Ct is present in L(k-1)
    """
    k_1_itemset = database.fetch_frequent_k_itemsets()
    k_subset = find_subsets(k_itemset, 2)
    subset_list = []
    for each_item in k_subset:
        subset_item = ' '.join(each_item)
        if subset_item in k_1_itemset:
            subset_list.append(subset_item)

    if len(k_subset) == len(subset_list):
        return True


def find_subsets(k_item, k):
    """
    Finding subset of Ct
    :param k_item: Ct itemsets
    :param k: (k-1) value
    :return: return the subset of
    """
    return set(combinations(k_item, k))


def prune(candidate_aspect_list, min_sup):
    """
    Apriori Pruning with the minimum support
    :param candidate_aspect_list: candidate aspect list with support count
    :param min_sup: minimum support count
    :return: candidate aspect list that satisfy minimum support
    """
    l_k = deepcopy(candidate_aspect_list)
    for key, value in list(l_k.items()):
        if value < min_sup:
            del l_k[key]
    return l_k


def scan_in_database(Ct):
    """
    Scan database to check if Ct is the subset of the transaction
    :param Ct:
    :return: dictionary of candidate aspect with the support count
    """
    current_candidate = {}
    transaction = database.fetch_nouns_per_sentence()
    for each_Ct in Ct:
        for tran_id, review_id, sent_id, itm in transaction:
            item = set(itm.split(','))
            if set(each_Ct).issubset(item):
                if str(each_Ct) not in current_candidate.keys():
                    current_candidate[str(each_Ct)] = 1
                else:
                    current_candidate[str(each_Ct)] += 1
    return current_candidate


def frequent_itemset_from_db():
    """
    Getting frequent itemset (L1, L2 and L3) and combining into single list
    :return:
    """
    frequent_1_itemsets = database.fetch_frequent_itemsets()
    frequent_k_itemsets = database.fetch_frequent_k_itemsets()
    frequent_itemsets_list = []
    for freq_1_item in frequent_1_itemsets:
        if freq_1_item not in frequent_itemsets_list:
            frequent_itemsets_list.append(freq_1_item)

    for freq_k_item in frequent_k_itemsets:
        if freq_k_item not in frequent_itemsets_list:
            frequent_itemsets_list.append(freq_k_item)

    database.insert_final_candidate_aspects(frequent_itemsets_list)
    # return database.fetch_final_candidate_aspects()
