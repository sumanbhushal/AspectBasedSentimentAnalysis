import nltk, re

#Chunking - to group NN/NNS
def noun_chunking(pos_tagged_text):
    """
    Creating chunk regular expression to get the nouns and nouns phrase
    :param pos_tagged_text:
    :return:
    """
    noun_list_after_chunk = []
    chunkRegExpress = r"""ProductAspect: {<NN.*>+}"""
    chunkParsar = nltk.RegexpParser(chunkRegExpress)
    for review_id, sent_id, pos_tagged_content in pos_tagged_text:
        chunked = chunkParsar.parse(pos_tagged_content)
        noun_list_per_sentence=[]
        for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'ProductAspect'):

            noun_list_per_sentence.append(" ".join(word for word, pos in subtree.leaves()).lower())
        combine_value = (review_id, sent_id, noun_list_per_sentence)
        noun_list_after_chunk.append(combine_value)
    return noun_list_after_chunk

#Chunking - to group NN/NNS
def noun_chunking_for_stanford_pos(pos_tagged_text):
    """
    Creating chunk regular expression to get the nouns and nouns phrase
    :param pos_tagged_text:
    :return:
    """
    noun_list_after_chunk = []
    noun_list = []
    noun_list_Dict = {}
    chunkRegExpress = r"""ProductAspect: {<NN.*>+}"""
    chunkParsar = nltk.RegexpParser(chunkRegExpress)
    for review_id, sent_id, pos_tagged_content in pos_tagged_text:
        pos_tagged_list = eval(pos_tagged_content)
        chunked = chunkParsar.parse(pos_tagged_list)
        noun_list_per_sentence=[]
        for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'ProductAspect'):

            noun_list_per_sentence.append(" ".join(word for word, pos in subtree.leaves()).lower())
            noun_list.append(" ".join(word for word, pos in subtree.leaves()).lower())  # Generating one list of noun_words
        if (noun_list_per_sentence):
            combine_value = (review_id, sent_id, noun_list_per_sentence)
            noun_list_after_chunk.append(combine_value)


    # Getting list of nouns with count (if necessary eliminating aspect which has 1 or less count)
    for aspect in noun_list:
        # if (noun_list.count(aspect) > 1):
        if (noun_list_Dict.keys() != aspect):
            noun_list_Dict[aspect] = noun_list.count(aspect)
    outputAspect = sorted(noun_list_Dict.items(), key=lambda x: x[1], reverse=True)
    return noun_list_after_chunk

#Chunking - to group JJ-NN/NNS
def adj_noun_chunking_for_stanford_pos(pos_tagged_text):
    """
    Creating chunk regular expression to get the nouns and nouns phrase
    :param pos_tagged_text:
    :return:
    """
    adj_noun_list_after_chunk = []
    adj_noun_list = []
    noun_list_Dict = {}
    # chunkRegExpress = r"""ProductAspect: {<NN.*><VBZ.*>+}"""
    chunkRegExpress = r"""ProductAspect: {<JJ.?><NN.*>+}"""
    # chunkRegExpress = r"""ProductAspect: {<NN.*><VBZ.?>+}"""
    chunkParsar = nltk.RegexpParser(chunkRegExpress)
    for review_id, sent_id, pos_tagged_content in pos_tagged_text:
        pos_tagged_list = eval(pos_tagged_content)
        chunked = chunkParsar.parse(pos_tagged_list)
        adj_noun_list_per_sentence=[]
        for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'ProductAspect'):

            adj_noun_list_per_sentence.append(" ".join(word for word, pos in subtree.leaves()).lower())
            adj_noun_list.append(" ".join(word for word, pos in subtree.leaves()).lower())  # Generating one list of noun_words
        combine_value = (review_id, sent_id, adj_noun_list_per_sentence)
        adj_noun_list_after_chunk.append(combine_value)

    # Getting list of nouns with count (if necessary eliminating aspect which has 1 or less count)
    # for aspect in adj_noun_list:
    #     # if (adj_noun_list.count(aspect) > 1):
    #     if (noun_list_Dict.keys() != aspect):
    #         noun_list_Dict[aspect] = adj_noun_list.count(aspect)
    # outputAspect = sorted(noun_list_Dict.items(), key=lambda x: x[1], reverse=True)
    # print(len(outputAspect),outputAspect)
    return adj_noun_list_after_chunk

# Chunking - JJ (adjective as feaatures)
def adj_chunking_for_stanford_pos(pos_tagged_text):
    """
    Creating chunk regular expression to get the nouns and nouns phrase
    :param pos_tagged_text:
    :return:
    """
    adjective_list_after_chunk = []
    adjective_list = []
    adjective_list_Dict = {}
    chunkRegExpress = r"""ProductAspect: {<JJ.*>+}"""
    chunkParsar = nltk.RegexpParser(chunkRegExpress)
    for review_id, sent_id, pos_tagged_content in pos_tagged_text:
        pos_tagged_list = eval(pos_tagged_content)
        chunked = chunkParsar.parse(pos_tagged_list)
        noun_list_per_sentence=[]
        for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'ProductAspect'):

            noun_list_per_sentence.append(" ".join(word for word, pos in subtree.leaves()).lower())
            adjective_list.append(" ".join(word for word, pos in subtree.leaves()).lower())  # Generating one list of noun_words
        combine_value = (review_id, sent_id, noun_list_per_sentence)
        adjective_list_after_chunk.append(combine_value)

    # Getting list of nouns with count (if necessary eliminating aspect which has 1 or less count)
    # for aspect in adjective_list:
    #     # if (adjective_list.count(aspect) > 1):
    #     if (adjective_list_Dict.keys() != aspect):
    #         adjective_list_Dict[aspect] = adjective_list.count(aspect)
    # outputAspect = sorted(adjective_list_Dict.items(), key=lambda x: x[1], reverse=True)
    # print(len(outputAspect),outputAspect)
    return adjective_list_after_chunk


# Chunking - NN-VBZ (eg. on/off controls)
def noun_verb_chunking_for_stanford_pos(pos_tagged_text):
    """
    Creating chunk regular expression to get the nouns and nouns phrase
    :param pos_tagged_text:
    :return:
    """
    noun_verb_list_after_chunk = []
    noun_verb_list = []
    chunkRegExpress = r"""ProductAspect: {<NN.*><VBZ.?>+}"""
    chunkParsar = nltk.RegexpParser(chunkRegExpress)
    for review_id, sent_id, pos_tagged_content in pos_tagged_text:
        pos_tagged_list = eval(pos_tagged_content)
        chunked = chunkParsar.parse(pos_tagged_list)
        noun_verb_list_per_sentence=[]
        for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'ProductAspect'):

            noun_verb_list_per_sentence.append(" ".join(word for word, pos in subtree.leaves()).lower())
        combine_value = (review_id, sent_id, noun_verb_list_per_sentence)
        noun_verb_list_after_chunk.append(combine_value)

    return noun_verb_list_after_chunk


# Chunking - VBG-NN (verb, gerund/present participle- taking, Noun)
def verb_noun_chunking_for_stanford_pos(pos_tagged_text):
    """
    Creating chunk regular expression to get the nouns and nouns phrase
    :param pos_tagged_text:
    :return:
    """
    verb_noun_list_after_chunk = []
    verb_noun_list = []
    chunkRegExpress = r"""ProductAspect: {<VBG.*><NN.?>+}"""
    chunkParsar = nltk.RegexpParser(chunkRegExpress)
    for review_id, sent_id, pos_tagged_content in pos_tagged_text:
        pos_tagged_list = eval(pos_tagged_content)
        chunked = chunkParsar.parse(pos_tagged_list)
        verb_noun_list_per_sentence=[]
        for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'ProductAspect'):

            verb_noun_list_per_sentence.append(" ".join(word for word, pos in subtree.leaves()).lower())
        combine_value = (review_id, sent_id, verb_noun_list_per_sentence)
        verb_noun_list_after_chunk.append(combine_value)
    return verb_noun_list_after_chunk


def extract_aspect_from_opinion(pos_tagged_sentences):
    product_aspect = []
    for pos_tagged_sents in pos_tagged_sentences:
        adjective_list = []
        noun_list = []
        for word, pos in pos_tagged_sents:
            if pos =='JJ' or pos =='JJR' or pos == 'JJS':
                # print('opin', word)
                opinion_pos = (word, pos)
                adjective_list.append(opinion_pos)
            if pos == 'NN' or pos =='NNS':
                # print(word)
                noun_pos = (word, pos)
                noun_list.append(noun_pos)

        for opinion_word_with_pos in adjective_list:
            noun_and_distance_from_adj = []
            adjective_position = pos_tagged_sents.index(opinion_word_with_pos)
            #print(opinion_word_with_pos[0])
            for noun_with_pos in noun_list:
                noun_position = pos_tagged_sents.index(noun_with_pos)
                noun_distance_from_adjective = abs(noun_position - adjective_position)
                noun_and_adj_distance = (noun_with_pos[0], noun_distance_from_adjective)
                noun_and_distance_from_adj.append(noun_and_adj_distance)

            #print(noun_and_distance_from_adj)
            if len(noun_and_distance_from_adj) != 0:
                min_distance = min(distance for nn, distance in noun_and_distance_from_adj)
                #print(min_distance)
                for nn, distance in noun_and_distance_from_adj:
                    if distance == min_distance:
                        product_aspect.append(nn)
    print(len(product_aspect), product_aspect)


#Extraction Noun from sentence
def extract_noun(pos_tagged_review):
    prev_word = ''
    prev_tag = ''
    curr_word = ''
    noun_list = []
    noun_list_Dict = {}
    # Extracting Aspects
    for review_id, sent_id, pos_tagged_content in pos_tagged_review:
        for word, pos in pos_tagged_content:
            if (pos == 'NN' or pos == 'NNP'):
                if (prev_tag == 'NN' or prev_tag == 'NNP'):
                    curr_word = prev_word + ' ' + word
                else:
                    noun_list.append(prev_word.lower())
                    curr_word = word
            prev_word = curr_word
            prev_tag = pos

    # Eliminating aspect which has 1 or less count
    for aspect in noun_list:
        if (noun_list.count(aspect) > 1):
            if (noun_list_Dict.keys() != aspect):
                noun_list_Dict[aspect] = noun_list.count(aspect)
    outputAspect = sorted(noun_list_Dict.items(), key=lambda x: x[1], reverse=True)
    # print(len(outputAspect), outputAspect)
    return outputAspect

#Extraction Noun from sentence
def extract_noun_from_standford_pos(pos_tagged_review):
    prev_word = ''
    prev_tag = ''
    curr_word = ''
    noun_list = []
    noun_list_Dict = {}
    # Extracting Aspects
    for review_id, sent_id, pos_tagged_content in pos_tagged_review:
        pos_list = eval(pos_tagged_content)
        for word, pos in pos_list:
            if (pos == 'NN' or pos == 'NNP'):
                if (prev_tag == 'NN' or prev_tag == 'NNP'):
                    curr_word = prev_word + ' ' + word
                else:
                    noun_list.append(prev_word.lower())
                    curr_word = word
            prev_word = curr_word
            prev_tag = pos

    # Eliminating aspect which has 1 or less count
    for aspect in noun_list:
        # if (noun_list.count(aspect) > 1):
        if (noun_list_Dict.keys() != aspect):
            noun_list_Dict[aspect] = noun_list.count(aspect)
    outputAspect = sorted(noun_list_Dict.items(), key=lambda x: x[1], reverse=True)
    # print(len(outputAspect), outputAspect)
    return outputAspect

def generate_ngrams(input_text, n):
    ngram_list = []
    input = input_text.split(' ')
    for i in range(len(input) - n+1):
        ngram_list.append(input[i:i+n])
    #print(ngram_list)
    return ngram_list


