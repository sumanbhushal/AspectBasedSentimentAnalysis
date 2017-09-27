import nltk

#Chunking - to group NN/NNS
def noun_chunking(pos_tagged_text):
    """
    Creating chunk regular expression to get the nouns and nouns phrase
    :param pos_tagged_text:
    :return:
    """
    noun_list_after_chunk = []
    aspect_dictionary = {}
    chunkRegExpress = r"""ProductAspect: {<NN.*>+}"""
    chunkParsar = nltk.RegexpParser(chunkRegExpress)
    for pos_tagged_content in pos_tagged_text:
        chunked = chunkParsar.parse(pos_tagged_content)
        #chunked.draw()
        #print(chunked)
        for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'ProductAspect'):
            noun_list_after_chunk.append(" ".join(word for word, pos in subtree.leaves()).lower())

    for aspect in noun_list_after_chunk:
        if (aspect_dictionary.keys()!= aspect):
            aspect_dictionary[aspect] = noun_list_after_chunk.count(aspect)
    outputAspect = sorted(aspect_dictionary.items(), key=lambda x: x[1], reverse=True)
    return outputAspect


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
    noun_collection = []
    for word in pos_tagged_review:
        if word[1][0] == 'N':
            noun_collection.append(word[0])
    return noun_collection


def generate_ngrams(input_text, n):
    ngram_list = []
    input = input_text.split(' ')
    for i in range(len(input) - n+1):
        ngram_list.append(input[i:i+n])
    #print(ngram_list)
    return ngram_list


