import database


def compactness_pruning():
    # for each sentence in the review database:
    #     if (a feature phrase found):
    #         for each feature in the sentence :
    #             Measure the distance between every two words;
    #             if (words distance > 3)
    #                 Remove the feature from the list;

    candidate_feature_phrase = database.fetch_frequent_itemsets()
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
            if len(word_index_dict) > 2:
                listForm = list(word_index_dict.values())
                previous_value = (listForm[0])
                current_value = (listForm[1])
                next_value = (listForm[2])
                if current_value - previous_value < 3 and next_value - current_value < 3:
                    i += 1
            if len(word_index_dict) > 1:
                listForm = list(word_index_dict.values())
                previous_value = (listForm[0])
                current_value = (listForm[1])
                if current_value - previous_value < 3:
                    i += 1

            # Count how many times features appear in the sentence
        if feature_count_in_dict.keys() != fp:
            feature_count_in_dict[fp] = i

    # print(feature_count_in_dict)
    for key, value in feature_count_in_dict.items():
        if value > 3:
            feature_list_after_compactness_pruning.append(key)
    return feature_list_after_compactness_pruning

def redundancy_pruning():
    min_psupport_threshold = 4
    product_aspect_after_redundancy_pruning = []
    candidate_product_aspect = database.fetch_freatures_after_compactness_pruning()

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
    print(product_aspect_after_redundancy_pruning)
    return product_aspect_after_redundancy_pruning

#
# def get_sentences_with_terms():
#     terms_in_sentence = []
#     sentences_with_terms = database.fetch_candidate_aspect_per_sentence()
#     for term_id, review_id, sent_id, term in sentences_with_terms:
#         terms_in_sentence.append(term.split(','))
#     return terms_in_sentence

#
# def get_all_noun_from_all_sentences(sentence_list):
#
#     noun_list = []
#     for sentence in sentence_list:
#         for noun in sentence:
#             noun_list.append(noun)
#     return noun_list

#
# def get_term_in_number_of_sents(sentences, noun_list):
#     term_psupport_dict = {}
#     for term in noun_list:
#         # print(term)
#         if term_psupport_dict.keys() != term:
#             term_psupport_dict[term] = 0
#             for s in sentences:
#                 if term in s:
#                     term_psupport_dict[term]+=1
#     print(term_psupport_dict)
#
# def get_aspect_superset_with_count(noun_list):
#     output_superset_with_count = []
#     for aspect in noun_list:
#         list_of_aspect_superset = []
#         aspect_count_dict = {}
#         for s in noun_list:
#             if aspect in s:
#                 list_of_aspect_superset.append(s)
#
#         for asp in list_of_aspect_superset:
#             if aspect_count_dict.keys() != asp:
#                 aspect_count_dict[asp] = list_of_aspect_superset.count(asp)
#         print(aspect_count_dict)
#         output_superset_with_count.append(sorted(aspect_count_dict.items(), key=lambda x: x[1], reverse=True))
#     # print(output_superset_with_count)
#     return output_superset_with_count

    # for aspect in noun_list:
    #     list_of_aspect_superset = [s for s in noun_list if aspect in s]


