import database
from copy import deepcopy
from itertools import combinations

def cbs_apriori_itemset():
    min_sup = 3
    L1 = {}
    Lk = {}
    items_in_transaction = []
    # Get candidate aspect from database
    transaction = database.fetch_candidate_aspect_per_sentence()
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
    current_C2 = scan_in_database(C2)
    Lk[2] = prune(current_C2, min_sup)

    # find the frequent 3-itemsets
    C3 = generate_3_itemset(L1)
    current_C3 = scan_in_database(C3)
    Lk[3] = prune(current_C3, min_sup)

    if Lk != '':
        database.insert_frequent_k_itemsets(Lk)
    # print(len(Lk[2]), Lk[2])


def generate_1_itemset(items_in_transaction):
    C_1 = {}
    for item in items_in_transaction:
        if (C_1.keys() != item):
            C_1[item] = items_in_transaction.count(item)
    return C_1

def generate_2_itemset(L):
    C_2 = []
    for i in combinations(L, 2):
        C_2.append(list(i))
    return list(C_2)

def generate_3_itemset(L):
    C_2 = []
    for i in combinations(L, 3):
        C_2.append(list(i))
    return list(C_2)

def has_infrequent_subset(k_itemset, k_1_itemset):
    final_itemset = deepcopy(k_itemset)
    for each_item in final_itemset:
        if each_item not in k_1_itemset:
            final_itemset.remove(each_item)
            break
    return final_itemset

def prune(candidate_aspect_list, min_sup):
    l_k = deepcopy(candidate_aspect_list)
    for key, value in list(l_k.items()):
        if value < min_sup:
            del l_k[key]
    return l_k

def scan_in_database(Ct):
    current_candidate = {}
    transaction = database.fetch_candidate_aspect_per_sentence()
    for each_Ct in Ct:
        for tran_id, review_id, sent_id, itm in transaction:
            item = set(itm.split(','))
            if set(each_Ct).issubset(item):
                if str(each_Ct) not in current_candidate.keys():
                    current_candidate[str(each_Ct)] = 1
                else:
                    current_candidate[str(each_Ct)] += 1
    return current_candidate
