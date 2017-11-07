import database
from copy import deepcopy
from itertools import combinations



def apriori_itemset():
    min_sup = 2
    L = {}
    items_in_transaction = []

    # Get candidate aspect from database
    transaction = database.fetch_candidate_aspect_per_sentence()
    for tran_id, review_id, sent_id, itm in transaction:
        for each_item in itm.split(','):
           items_in_transaction.append(each_item)

    # finds the frequent 1-itemsets
    C1 = generate_1_itemset(items_in_transaction)
    L[1] = prune(C1, min_sup)
    k = 2
    while L[k-1]:
        # print(L[k-1])

        # generate candidate k-itemsets
        Ck = apriori_gen(L[k-1])

        current_Ck = scan_in_database(Ck)

        # prune step
        L[k] = prune(current_Ck, min_sup)
        k += 1
    print(L)


def generate_1_itemset(items_in_transaction):
    c1 = {}
    for item in items_in_transaction:
        if (c1.keys() != item):
            c1[item] = items_in_transaction.count(item)
    return c1

def prune(candidate_aspect_list, min_sup):
    l_k = deepcopy(candidate_aspect_list)
    for key, value in list(l_k.items()):
        if value < min_sup:
            del l_k[key]
    return l_k

def apriori_gen(L):
    C_k = []
    for i in combinations(L, 2):
        if has_infrequent_subset(i, L):
            C_k.append(list(i))
    return list(C_k)


def has_infrequent_subset(k_itemset, k_1_itemset):
    final_itemset = deepcopy(k_itemset)
    for each_item in final_itemset:
        if each_item not in k_1_itemset:
            final_itemset.remove(each_item)
            break
    return final_itemset

def scan_in_database(Ct):
    current_candidate = {}
    transaction = database.fetch_candidate_aspect_per_sentence()
    for each_Ct in Ct:
        # print(each_Ct)
        for tran_id, review_id, sent_id, itm in transaction:
            item = set(itm.split(','))
            # print(item)

            if set(each_Ct).issubset(item):
                count = 1
                # if (current_candidate.keys() != each_Ct):
                #     current_candidate[each_Ct] = each_Ct

                if str(each_Ct) not in current_candidate.keys():
                    current_candidate[str(each_Ct)] = 1
                else:
                    current_candidate[str(each_Ct)] += 1
        # for i in combinations(itm.split(','), 2):
        #     print(i)
    return current_candidate



itemset = apriori_itemset()
# generate_k_combinations(itemset, 2)