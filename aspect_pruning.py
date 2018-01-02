import database, re
from nltk.corpus import wordnet


def compactness_pruning():
    """
    Compactness pruning (if the words distance every two words is less than 2 and is present in more than 4 sentence)
    """
    candidate_feature_phrase = database.fetch_final_candidate_aspects()
    sentences_list = database.fetch_sentence_from_sentence_table()

    feature_list_after_compactness_pruning = []
    feature_phase = []
    feature_count_in_dict = {}

    # Retrieving candidate aspects with more than two words
    for feature in candidate_feature_phrase:
        word_in_noun_phrase = feature.split()
        if len(word_in_noun_phrase) > 1:
            feature_phase.append(feature)
        else:
            feature_list_after_compactness_pruning.append(feature)

    # Calculating the word distance between any two words in candidate apsects
    for fp in feature_phase:
        i = 0
        for sent_id, review_id, sentences in sentences_list:
            word_index_dict = {}
            for fp_word in fp.split():
                for index, word in enumerate(sentences.split()):
                    if word == fp_word:
                        word_index_dict[fp_word] = index
            if (len(word_index_dict) > 2) and (len(fp.split("_")) == len(word_index_dict)):
                list_form = list(word_index_dict.values())
                previous_value = (list_form[0])
                current_value = (list_form[1])
                next_value = (list_form[2])
                if current_value - previous_value < 2 and next_value - current_value < 2:
                    i += 1
            elif len(word_index_dict) > 1 and len(fp.split()) == len(word_index_dict):
                list_form = list(word_index_dict.values())
                previous_value = (list_form[0])
                current_value = (list_form[1])
                if current_value - previous_value < 2:
                    i += 1
            else:
                i += 0

        # Count how many times features appear in the sentence
        if feature_count_in_dict.keys() != fp:
            feature_count_in_dict[fp] = i

    # Checking if the feature appears in more than 4 sentences
    for key, value in feature_count_in_dict.items():
        if value > 4:
            feature_list_after_compactness_pruning.append(key)

    database.insert_features_after_compactness_pruning(feature_list_after_compactness_pruning)


def redundancy_pruning(candidate_product_aspect):
    """
    Redundancy Pruning: if aspect support value is more than the minimum pure-support value
    :param candidate_product_aspect: candidate product aspect
    :return: list of candidate product aspect after redundancy pruning
    """
    min_psupport_threshold = 3
    product_aspect_after_redundancy_pruning = []

    for term in candidate_product_aspect:
        if term not in product_aspect_after_redundancy_pruning:
            # Fetching the superset of aspect from the database
            superset = database.fetch_superset_with_sentence_count(term)
            if len(superset) > 1:
                sentence_ids_list = []
                for t in superset:
                    if t != term:
                        sentence_ids = database.get_sentence_ids_for_term(t)
                        if sentence_ids:
                            if len(sentence_ids) > 1:
                                for sent_id in sentence_ids:
                                    sentence_ids_list.append(''.join(str(sent_id)))
                            else:
                                sentence_ids_list.append(str(sentence_ids).strip('[]'))
                if sentence_ids_list:
                    # query database to get the p-support of aspect
                    psupport_value_for_term = database.calcualte_psupport_for_term_with_out_superset(tuple(sentence_ids_list), term)

                    # Checking if p-support of aspect satisfy the minimum threshold
                    if psupport_value_for_term[0] > min_psupport_threshold:
                        product_aspect_after_redundancy_pruning.append(term)
            else:
                product_aspect_after_redundancy_pruning.append(term)

    # Replacing white space between the apects word with "_"
    prune_feature = []
    for aspect in product_aspect_after_redundancy_pruning:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        aspect_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', aspect)
        prune_feature.append(aspect_replacing_space_with_underscore)
    return prune_feature


def filter_aspect_based_on_domain_similarity(entity_name, feature_list):
    """
    :param entity_name: Name of the entity
    :param feature_list: list of product aspects to compare the similarity with the entity
    :return: aspect list after similarity resolution
    """
    new_aspect_list = []
    domain = entity_name + ".n.01"
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
    return new_aspect_list
