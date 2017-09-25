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


