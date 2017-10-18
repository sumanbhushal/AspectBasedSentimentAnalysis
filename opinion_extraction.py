import nltk, database
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet



def extract_opinon_of_feature(pos_tagged_sentence_list):
    features_list = ['adjustment']
    for features in features_list:
        opinions = []
        sentences_with_feature = []
        for sent_id, review_id, sentences in pos_tagged_sentence_list:
            for word, tag in sentences:
                if features == word:
                    sentences_with_feature.append(sentences)
                    # print(sentences.index(index_of_word), sentences)

        for sent in sentences_with_feature:
            feature_index_dict = {}
            opinion_index_dict = {}
            feature_index = []
            for word, tag in sent:
                if features == word:
                    index_of_word = (word, tag)
                    feature_index = sent.index(index_of_word)
                if tag == 'JJ' or tag == 'JJR' or tag == 'JJS':
                    index_of_opinion_word = (word, tag)
                    opinion_index_dict[word] = sent.index(index_of_opinion_word)

            if opinion_index_dict:
                distance_btw_feature_opinion = {}
                min_distance = 0
                for key in opinion_index_dict:
                    if len(opinion_index_dict) > 1:
                        distance_btw_feature_opinion_word = abs(feature_index - opinion_index_dict.get(key))
                        #print(feature_index, opinion_index_dict.get(key), distance_btw_feature_opinion_word, key)
                        distance_btw_feature_opinion[key] = distance_btw_feature_opinion_word
                    else:
                        distance_btw_feature_opinion[key] = opinion_index_dict.get(key)

                if distance_btw_feature_opinion:
                    opinions.append(min(distance_btw_feature_opinion, key=distance_btw_feature_opinion.get))
                    #print(min(distance_btw_feature_opinion, key=distance_btw_feature_opinion.get))
        print(opinions)
        word_orientation(opinions)


def extract_opinion(pos_tagged_sentence_list):
    adjective_list = []
    chunkRegExpress = r"""Opinion: {<JJ.*>+}"""
    chunkParsar = nltk.RegexpParser(chunkRegExpress)
    for pos_tagged_content in pos_tagged_sentence_list:
        chunked = chunkParsar.parse(pos_tagged_content)
        # chunked.draw()
        # print(chunked)
        for subtree in chunked.subtrees(filter=lambda chunk_label: chunk_label.label() == 'Opinion'):
            adjective_list.append(" ".join(word for word, pos in subtree.leaves()).lower())
    #print(len(adjective_list),adjective_list)


# WordNet to get the syns set and use SentiWordNet to find the orientation of the word
def word_orientation(input_word):
    for word in input_word:
        word_for_orientation = word + '.a.01'
        each_word_orientation = sentiwordnet.senti_synset(word_for_orientation)
        print(word_for_orientation, each_word_orientation)
        # syns = wordnet.synsets(word)
        # print(syns[0].name())
        # for i in syns:
        #     if i.pos() in ['a', 's']:
        #         print(word, i.lemmas()[0].name())
                # for j in i.lemmas():
                #     print(word, j[0].name())
        # if (len(syns) != 0):
        #     word = syns[0].name()
        #     word_orientation = sentiwordnet.senti_synset(word)
        #     print(word_orientation)
        #     print(word_orientation.pos_score())
    #print(syns[0])

