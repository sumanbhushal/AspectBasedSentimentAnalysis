import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

raw_consumerReviews = "I bought an iPhone a few days ago. It is such a nice phone. " \
                      "The touch screen is really cool. The voice quality is clear too. " \
                      "It is much better than my old Blackberry, which was a terrible phone and so difficult to type with its tiny keys. " \
                      "However, my mother was mad with me as I did not tell her before I bought the phone. " \
                      "She also thought the phone was too expensive."

# word tokenization
cosReview_word_tokens = word_tokenize(raw_consumerReviews)
print(cosReview_word_tokens)


#stopwords - using English
def filter_stopword(review):

    stop_words = set(stopwords.words('english'))
    cosReview_filtered_stopwords = []
    for words in review:
        if words[0] not in stop_words:
            cosReview_filtered_stopwords.append(words)
    return cosReview_filtered_stopwords

#text_after_stopwords = filter_stopword()
#print(text_after_stopwords)

#POS tagging
def pos_tagging(consumber_review):
    tagged = nltk.pos_tag(consumber_review)
    return tagged

#Chunking - to group NN/NNS
def noun_chunking(pos_tagged_text):
    noun_list_after_chunk = []
    aspect_dictionary = {}
    chunkRegExpress = r"""ProductAspect: {<NN.*>+}"""
    chunkParsar = nltk.RegexpParser(chunkRegExpress)
    chunked = chunkParsar.parse(pos_tagged_text)
    #chunked.draw()
    #print(chunked)
    for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'ProductAspect'):
        #noun_list_after_chunk.append(" ".join([a for (a,b) in subtree.leaves()]))
        noun_list_after_chunk.append(" ".join(word for word, pos in subtree.leaves()).lower())

    for aspect in noun_list_after_chunk:
        if (aspect_dictionary.keys()!= aspect):
            aspect_dictionary[aspect] = noun_list_after_chunk.count(aspect)
    outputAspect = sorted(aspect_dictionary.items(), key=lambda x: x[1], reverse=True)
    print(outputAspect)
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

all_word = pos_tagging(cosReview_word_tokens)
print(all_word)
extract_noun_set = noun_chunking(all_word)
print(extract_noun_set)
# noun_set = extract_noun(extract_noun_set)

print(extract_feature(extract_noun_set))





