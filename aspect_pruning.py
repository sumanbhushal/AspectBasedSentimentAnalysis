import database, re
from nltk.corpus import wordnet


def compactness_pruning():
    # for each sentence in the review database:
    #     if (a feature phrase found):
    #         for each feature in the sentence :
    #             Measure the distance between every two words;
    #             if (words distance > 3)
    #                 Remove the feature from the list;

    candidate_feature_phrase = database.fetch_final_candidate_aspects()
    sentences_list = database.fetch_sentence_from_sentence_table()

    feature_list_after_compactness_pruning = []
    feature_phase = []
    feature_count_in_dict = {}

    for feature in candidate_feature_phrase:
        word_in_noun_phrase = feature.split()
        if len(word_in_noun_phrase) > 1:
            feature_phase.append(feature)
        else:
            feature_list_after_compactness_pruning.append(feature)

    for fp in feature_phase:
        i = 0
        for sent_id, review_id, sentences in sentences_list:
            word_index_dict = {}
            for fp_word in fp.split():
                for index, word in enumerate(sentences.split()):
                    if word == fp_word:
                        word_index_dict[fp_word] = index
            if (len(word_index_dict) > 2 ) and (len(fp.split("_")) == len(word_index_dict)):
                listForm = list(word_index_dict.values())
                previous_value = (listForm[0])
                current_value = (listForm[1])
                next_value = (listForm[2])
                if current_value - previous_value < 2 and next_value - current_value < 2:
                    i += 1
            elif (len(word_index_dict)>1 and len(fp.split())== len(word_index_dict)):
                listForm = list(word_index_dict.values())
                previous_value = (listForm[0])
                current_value = (listForm[1])
                if current_value - previous_value < 2:
                    i += 1
            else:
                i += 0

            # Count how many times features appear in the sentence
        if feature_count_in_dict.keys() != fp:
            feature_count_in_dict[fp] = i
    for key, value in feature_count_in_dict.items():
        if value > 4:
            feature_list_after_compactness_pruning.append(key)
    database.insert_features_after_compactness_pruning(feature_list_after_compactness_pruning)

def redundancy_pruning(candidate_product_aspect):
    min_psupport_threshold = 3
    product_aspect_after_redundancy_pruning = []

    for term in candidate_product_aspect:
        if term not in product_aspect_after_redundancy_pruning:
            superset = database.fetch_superset_with_sentence_count(term)
            if len(superset) > 1:
                sentence_ids_list = []
                for t in superset:
                    if t != term:
                        sentence_ids = database.get_sentence_ids_for_term(t)
                        if sentence_ids:
                            if (len(sentence_ids)>1):
                                for id in sentence_ids:
                                    sentence_ids_list.append(''.join(str(id)))
                            else:
                                sentence_ids_list.append(str(sentence_ids).strip('[]'))
                if sentence_ids_list:
                    psupport_value_for_term =  database.calcualte_psupport_for_term_with_superset(tuple(sentence_ids_list), term)
                    if psupport_value_for_term[0] > min_psupport_threshold:
                        product_aspect_after_redundancy_pruning.append(term)
            else:
                product_aspect_after_redundancy_pruning.append(term)

    prune_feature = []
    for aspect in product_aspect_after_redundancy_pruning:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        aspect_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', aspect)
        prune_feature.append(aspect_replacing_space_with_underscore)
    return prune_feature


def filter_aspect_based_on_domain_similarity(domain_name, feature_list):
    new_aspect_list = []
    domain = domain_name + ".n.01"
    for aspect in feature_list:
        try:
            w1 = wordnet.synset(domain)
            compare_word = aspect + ".n.01"
            w2 = wordnet.synset(compare_word)
            word_similarity = (w1.wup_similarity(w2))
            if word_similarity > 0.15:
                new_aspect_list.append(aspect)
        except:
            pass
    print(new_aspect_list)
    # return new_wiki_list

