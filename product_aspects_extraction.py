import nltk

#Chunking - to group NN/NNS
def noun_chunking(pos_tagged_text):
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
    print(noun_list_after_chunk)
    return outputAspect

#Extraction Noun from sentence
def extract_noun(pos_tagged_review):
    noun_collection = []
    for word in pos_tagged_review:
        if word[1][0] == 'N':
            noun_collection.append(word[0])
    return noun_collection

#Extracting features comparing with features list
def extract_feature(noun_list):
    all_features = []
    feature_set = ['phone', 'screen', 'voice quality']
    for noun in noun_list:
        if noun[0] in feature_set:
            all_features.append(noun[0])
    return all_features

# all_words = nltk.FreqDist(pos_tagging(text_after_stopwords))
# print(all_words.most_common(5))


if __name__ == '__main__':
    all_word = pos_tagging(cosReview_word_tokens)
    print(all_word)
    extract_noun_set = noun_chunking(all_word)
    print(extract_noun_set)
    # noun_set = extract_noun(extract_noun_set)
    print(extract_feature(extract_noun_set))



