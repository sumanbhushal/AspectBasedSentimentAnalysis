import database


def compactness_pruning():
    # for each sentence in the review database:
    #     if (a feature phrase found):
    #         for each feature in the sentence :
    #             Measure the distance between every two words;
    #             if (words distance > 3)
    #                 Remove the feature from the list;
    noun_for_each_sentence = get_sentences_with_terms()
    noun_list = get_all_noun_from_all_sentences(noun_for_each_sentence)
    sentences_in_reviews = database.fetch_sentence_from_sentence_table()
    words_in_sentence = []
    feature_phase = []

    # for sent_id, review_id, sentences in sentences_in_reviews:
    #     words_in_sentence.append(sentences.split())

    for noun in noun_list:
        word_in_noun_phrase = noun.split()
        if len(word_in_noun_phrase) > 1:
            feature_phase.append(noun)

    for sent_id, review_id, sentences in sentences_in_reviews:
        words_in_sentence.append((sentences.lower()).split())
        for fp in feature_phase:
            if fp in sentences.lower():
                word_index_dict = {}
                for fp_word in fp.split():
                    print(fp_word)
                    for sent in words_in_sentence:
                        if fp_word in sent:
                            # print(fp, sent.index(fp_word))
                            word_index_dict[fp_word] = sent.index(fp_word)
                print(sent_id, word_index_dict)

def redundancy_pruning():
    min_psupport_threshold = 3
    noun_for_each_sentence= get_sentences_with_terms()
    noun_list = get_all_noun_from_all_sentences(noun_for_each_sentence)

    get_term_in_number_of_sents (noun_for_each_sentence, noun_list)
    get_aspect_superset_with_count(noun_list)



def get_sentences_with_terms():
    terms_in_sentence = []
    sentences_with_terms = database.fetch_candidate_aspect_db()
    for term_id, review_id, sent_id, term in sentences_with_terms:
        terms_in_sentence.append(term.split(','))
    return terms_in_sentence


def get_all_noun_from_all_sentences(sentence_list):

    noun_list = []
    for sentence in sentence_list:
        for noun in sentence:
            noun_list.append(noun)
    return noun_list


def get_term_in_number_of_sents(sentences, noun_list):
    term_psupport_dict = {}
    for term in noun_list:
        # print(term)
        if term_psupport_dict.keys() != term:
            term_psupport_dict[term] = 0
            for s in sentences:
                if term in s:
                    term_psupport_dict[term]+=1
    print(term_psupport_dict)

def get_aspect_superset_with_count(noun_list):
    output_superset_with_count = []
    for aspect in noun_list:
        list_of_aspect_superset = []
        aspect_count_dict = {}
        for s in noun_list:
            if aspect in s:
                list_of_aspect_superset.append(s)

        for asp in list_of_aspect_superset:
            if aspect_count_dict.keys() != asp:
                aspect_count_dict[asp] = list_of_aspect_superset.count(asp)
        print(aspect_count_dict)
        output_superset_with_count.append(sorted(aspect_count_dict.items(), key=lambda x: x[1], reverse=True))
    # print(output_superset_with_count)
    return output_superset_with_count

    # for aspect in noun_list:
    #     list_of_aspect_superset = [s for s in noun_list if aspect in s]


