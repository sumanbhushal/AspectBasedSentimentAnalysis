import nltk, database, config
from nltk import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet


def extract_opinon_of_feature(pos_tagged_sentence_list):
    features_list = ['adjustment']
    for features in features_list:
        opinions = []
        sentences_with_feature = []
        for sent_id, review_id, sentences in pos_tagged_sentence_list:
            sentence_as_list = eval(sentences)
            for word, tag in sentence_as_list:
                if features == word:
                    sentences_with_feature.append(sentences)
                    # print(sentences.index(index_of_word), sentences)

        for sent in sentences_with_feature:
            sent_as_list = eval(sent)
            feature_index_dict = {}
            opinion_index_dict = {}
            feature_index = []
            for word, tag in sent_as_list:
                if features == word:
                    index_of_word = (word, tag)
                    feature_index = sent_as_list.index(index_of_word)
                if tag == 'JJ' or tag == 'JJR' or tag == 'JJS':
                    index_of_opinion_word = (word, tag)
                    opinion_index_dict[word] = sent_as_list.index(index_of_opinion_word)

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
        # word_orientation(opinions)
        generate_summary(features, len(sentences_with_feature), opinions)


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
    opinion_orientation_of_feature = 0
    for word in input_word:
        syns = wordnet.synsets(word)
        if (len(syns) != 0):
            word = syns[0].name()
            each_word_orientation = sentiwordnet.senti_synset(word)
            print(word, each_word_orientation)
            if each_word_orientation.pos_score() != 0:
                opinion_orientation_of_feature += (each_word_orientation.pos_score() - each_word_orientation.neg_score())
            elif each_word_orientation.neg_score() != 0:
                opinion_orientation_of_feature -= each_word_orientation.neg_score()
                print(opinion_orientation_of_feature)
    print(" Totatl Orientation", opinion_orientation_of_feature)
    normalized_value = (opinion_orientation_of_feature) / len(input_word)
    print(" Totatl Orientation", normalized_value)

        # word_for_orientation = word + '.a.01'
        # each_word_orientation = sentiwordnet.senti_synset(word_for_orientation)
        # print(word_for_orientation, each_word_orientation)
        # syns = wordnet.synsets(word)
        # for i in syns:
        #     if i.pos() in ['a', 's']:
        #         print(i.lemmas())


def generate_summary(feature, sentence_count, input_word):
    opinion_orientation_of_feature = 0
    pos, neg, neu = 0, 0, 0
    for word in input_word:
        syns = wordnet.synsets(word)
        if (len(syns) != 0):
            word = syns[0].name()
            each_word_orientation = sentiwordnet.senti_synset(word)
            if each_word_orientation.pos_score() != 0:
                if each_word_orientation.pos_score() - each_word_orientation.neg_score() > 0:
                    pos += 1
                else:
                    neg += 1
            elif each_word_orientation.neg_score() != 0:
                # opinion_orientation_of_feature -= each_word_orientation.neg_score()
                neg += 1
            else:
                neu += 1

    print("Feature = ", feature)
    print("total posts =", sentence_count, "\n" "positives =", pos, ", negatives =", neg, ", neutrals =", neu)

def extract_opinion_of_aspect_using_lexicon():

    positive_lexicon = read_lexicon(config.LEXICONS_PATH + "positive-words.txt")
    negative_lexicon = read_lexicon(config.LEXICONS_PATH + "negative-words.txt")
    features_list = ['lens', 'zoom', 'battery', 'pictures', 'canon', 'g3']

    lex_list = []
    for pos_lex in positive_lexicon:
        lex_list.append(pos_lex)
    for neg_lex in negative_lexicon:
        lex_list.append(neg_lex)

    sentence_in_reviews = database.fetach_pos_tagged_sentence()

    subjective_sentence = []
    for sent_id, review_id, sentences in sentence_in_reviews:
        opinion_word_and_postion = []
        feature_word_and_position = []
        sentence = eval(sentences)
        index = 0
        for word, tag in sentence:
            for lex_word in lex_list:
                if word == lex_word:
                    # sentences_with_feature.append(sentences)
                    word_tag = (word, tag)
                    word_index = (word, index)
                    opinion_word_and_postion.append(word_index)
                    # print(sent_id, pos_word, word_index, sentence)

            for feature in features_list:
                if feature == word:
                    word_tag = (word, tag)
                    feature_index = (feature, index)
                    feature_word_and_position.append(feature_index)
            index += 1

        # for word, tag in sentence:
        # get index of opinion word
        # got idex of features in sentence
        # if index of featrue is < index of opion_word
        # if more than one, take the close feature
        # If not present in backwards direction look at forward
        if (opinion_word_and_postion):
            # opinion_position = 0
            # opinion_word = ''
            # feature_word = ''
            for o_word, o_index in opinion_word_and_postion:
                # opinion_word = sentence[value]
                opinion_position = o_index
                opinion_word = o_word

                if(feature_word_and_position):
                    for p_word, p_index in feature_word_and_position:
                        feature_position = p_index
                        feature_word = p_word

                        calculate_difference_in_distance = opinion_position - feature_position
                        if feature_position < opinion_position and calculate_difference_in_distance <= 4:
                            print("compare", sent_id, opinion_word,opinion_position, feature_word, feature_position)
                            for i in range(calculate_difference_in_distance):
                                ind_value = sentence[feature_position+i]
                                print ("distance", ind_value)
                            print("--------------------")
                        elif feature_position > opinion_position:
                            distance_difference = feature_position - opinion_position
                            if(distance_difference < 2):
                                print("Right to opinion", opinion_word,opinion_position, feature_word, feature_position)

def read_lexicon(path):
    lexicon = []

    with open(path, 'r') as file:
        for line in file:
                lexicon.append(line.strip())
    return lexicon

extract_opinion_of_aspect_using_lexicon()