import nltk, pre_processing, database


def noun_chunking_for_stanford_pos():
    """
    Creating chunk regular expression for getting Nouns and Nouns phrases (NN | NN| JJ-NN)
    """
    noun_list_after_chunk = []

    pos_tagged_text = database.fetach_pos_tagged_sentence()  # fetching POS tagged Sentence from database
    # chunkRegExpress = r"""NP: {<NN.*>}"""
    chunk_reg_express = r"""NP: {<JJ>*<NN.*>}"""  # chunking rules
    chunk_parsar = nltk.RegexpParser(chunk_reg_express)

    for review_id, sent_id, pos_tagged_content in pos_tagged_text:
        pos_tagged_list = eval(pos_tagged_content)
        chunked = chunk_parsar.parse(pos_tagged_list)
        noun_list_per_sentence = []
        for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'NP'):  # fileter word with NP as chunk label
            noun_list_per_sentence.append(" ".join(word for word, pos in subtree.leaves() if word not in noun_list_per_sentence))

        if noun_list_per_sentence:
            combine_value = (review_id, sent_id, noun_list_per_sentence)
            noun_list_after_chunk.append(combine_value)

    # Filtering stopwords from candidate aspect list
    noun_list_without_stopwords = pre_processing.filter_stopwords(noun_list_after_chunk)

    # insert noun list  per sentence (will be used as transaction)and each noun in individual row in database
    database.insert_nouns_list_per_sentence_into_db(noun_list_without_stopwords)
    database.insert_single_candidate_aspect_per_row(noun_list_without_stopwords)
