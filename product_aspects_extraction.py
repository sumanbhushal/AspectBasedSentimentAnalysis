import nltk, re, pre_processing, database


def noun_chunking_for_stanford_pos():
    """
    Creating chunk regular expression for getting Nouns and Nouns phrases (NN | JJ-NN)
    :param :
    :return:
    """
    noun_list_after_chunk = []
    noun_list = []
    distinct_noun_list = []

    pos_tagged_text = database.fetach_pos_tagged_sentence()
    # chunkRegExpress = r"""NP: {<NN.*>}"""
    chunkRegExpress = r"""NP: {<JJ>*<NN.*>}"""
    chunkParsar = nltk.RegexpParser(chunkRegExpress)
    for review_id, sent_id, pos_tagged_content in pos_tagged_text:
        pos_tagged_list = eval(pos_tagged_content)
        chunked = chunkParsar.parse(pos_tagged_list)
        noun_list_per_sentence=[]
        for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'NP'):
            noun_list_per_sentence.append(" ".join(word for word, pos in subtree.leaves() if word not in noun_list_per_sentence))
            noun_list.append(" ".join(word for word, pos in subtree.leaves()).lower())
        if (noun_list_per_sentence):
            combine_value = (review_id, sent_id, noun_list_per_sentence)
            noun_list_after_chunk.append(combine_value)

    noun_list_without_stopwords = pre_processing.filter_stopwords(noun_list_after_chunk)

    # insert noun list and noun_chunk per sentence
    database.insert_nouns_list_per_sentence_into_db(noun_list_without_stopwords)
    database.insert_single_candidate_aspect_per_row(noun_list_without_stopwords)
    return noun_list_without_stopwords
