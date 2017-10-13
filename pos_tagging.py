from nltk import pos_tag


# POS tagging
def pos_tagging(tokeninzed_sentence_list):
    """
    :param tokeninzed_sentence_list: word tokenize consumer review
    :return: List of word with POS tagging
    """
    ids_pos_value = []
    for review_id, sent_id, sentences in tokeninzed_sentence_list:
        review_id = review_id
        sent_id = sent_id
        pos_tagged = pos_tag(sentences)
        combine_value = (review_id, sent_id,pos_tagged)
        ids_pos_value.append(combine_value)
    return ids_pos_value