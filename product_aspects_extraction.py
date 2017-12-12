import nltk, re, pre_processing

# Chunking - Getting Nouns and Nouns phrases (NN | JJ-NN)
def noun_chunking_for_stanford_pos(pos_tagged_text):
    """
    Creating chunk regular expression to get the nouns and nouns phrase
    :param pos_tagged_text:
    :return:
    """
    noun_list_after_chunk = []
    noun_list = []
    noun_list_Dict = {}
    # chunkRegExpress = r"""NP: {<NN.*>}"""
    chunkRegExpress = r"""NP: {<JJ>*<NN.*>}"""
    chunkParsar = nltk.RegexpParser(chunkRegExpress)
    for review_id, sent_id, pos_tagged_content in pos_tagged_text:
        pos_tagged_list = eval(pos_tagged_content)
        chunked = chunkParsar.parse(pos_tagged_list)
        noun_list_per_sentence=[]
        for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'NP'):
            noun_list_per_sentence.append(" ".join(word for word, pos in subtree.leaves()).lower())
            noun_list.append(" ".join(word for word, pos in subtree.leaves()).lower())
        if (noun_list_per_sentence):
            combine_value = (review_id, sent_id, noun_list_per_sentence)
            noun_list_after_chunk.append(combine_value)

    noun_list_without_stopwords = pre_processing.filter_stopwords(noun_list_after_chunk)
    return noun_list_without_stopwords
