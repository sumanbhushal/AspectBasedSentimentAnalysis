import nltk, database, config
from nltk import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import math


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
    # features_list = ['lens', 'zoom', 'battery life', 'picture', 'canon', 'g3']
    features_list = database.fetch_freatures_after_compactness_pruning()
    # print(len(features_list), features_list)

    lex_list = []
    for pos_lex in positive_lexicon:
        lex_list.append(pos_lex)
    for neg_lex in negative_lexicon:
        lex_list.append(neg_lex)

    sentence_in_reviews = database.fetach_pos_tagged_sentence()
    sentence_containing_feature_opinion = []

    for sent_id, review_id, sentences in sentence_in_reviews:
        opinion_word_and_postion = []
        feature_word_and_position = []
        sentence = eval(sentences)
        index = 0
        prev_word = ''

        for word, tag in sentence:
            current_word = ''
            for lex_word in lex_list:
                if word == lex_word:
                    # sentences_with_feature.append(sentences)
                    word_tag = (word, tag)
                    word_tag_index = (word, tag, index)
                    opinion_word_and_postion.append(word_tag_index)
                    # print(sent_id, lex_word, word_index, sentence)

            for feature in features_list:
                # print("FEATRURE", feature.split()[0])
                if len(feature.split()) == 1:
                    if feature == word:
                        word_tag = (word, tag)
                        feature_tag_index = (feature, tag, index)
                        feature_word_and_position.append(feature_tag_index)
                else:
                    complete_word = ''
                    for i in range(len(feature.split())):
                        # print("Feature", feature)
                        if feature.split()[i] == word:
                            if prev_word != '':
                                current_word = prev_word + ' ' + feature.split()[i]
                            else:
                                current_word = feature.split()[i]
                            prev_word = current_word
                    if len(current_word) != 1 and current_word != '':
                        complete_word = current_word
                    if complete_word == feature:
                        word_tag = (word, tag)
                        feature_tag_index = (feature, tag, index)
                        feature_word_and_position.append(feature_tag_index)
                        # print("Complete word", complete_word, len(complete_word.split()),word, sent_id)

            index += 1

        # for word, tag in sentence:
        # get index of opinion word
        # got idex of features in sentence
        # if index of featrue is < index of opion_word
        # if more than one, take the close feature
        # If not present in backwards direction look at forward
        if (opinion_word_and_postion):
            for o_word, o_tag, o_index in opinion_word_and_postion:
                opinion_position = o_index
                opinion_word = o_word

                if(feature_word_and_position):
                    print(feature_word_and_position)
                    for p_word, p_tag, p_index in feature_word_and_position:
                        feature_position = p_index
                        feature_word = p_word

                        calculate_difference_in_distance = opinion_position - feature_position
                        end_element = calculate_difference_in_distance + 1
                        subjective_sentence = []
                        if feature_position < opinion_position and calculate_difference_in_distance <= 4:
                            # print("compare", sent_id, opinion_word,opinion_position, feature_word, feature_position)
                            for i in range(end_element):
                                ind_value = sentence[feature_position+i]
                                subjective_sentence.append(ind_value)
                                # print(sent_id, "distance", ind_value)
                            # print("----------------")
                            sent_in_freq_tag = compare_opinion_syntax(subjective_sentence)
                            if (sent_in_freq_tag == True):
                                feature_opinion_sent = (feature_word, opinion_word, o_tag, sent_id)
                                sentence_containing_feature_opinion.append(feature_opinion_sent)

                        elif feature_position > opinion_position:
                            distance_difference = feature_position - opinion_position
                            end_element = distance_difference + 1
                            if(distance_difference < 2):
                                for i in range(end_element):
                                    ind_value = sentence[opinion_position + i]
                                    subjective_sentence.append(ind_value)
                                    # print("Right to opinion", opinion_word,opinion_position, feature_word, feature_position)
                                    # print("Right syntaz", ind_value)
                                # print("----------------")
                                sent_in_freq_tag = compare_opinion_syntax(subjective_sentence)
                                if (sent_in_freq_tag == True):
                                    feature_opinion_sent = (feature_word, opinion_word, o_tag, sent_id)
                                    sentence_containing_feature_opinion.append(feature_opinion_sent)
    print("FEATURE", len(sentence_containing_feature_opinion), sentence_containing_feature_opinion)
    return sentence_containing_feature_opinion

def read_lexicon(path):
    lexicon = []

    with open(path, 'r') as file:
        for line in file:
                lexicon.append(line.strip())
    return lexicon

def compare_opinion_syntax(noun_opinion):
    feature_opinion_syntax = []
    feature_syntax_list = [['NN', 'VBP', 'JJ'],
                           ['NN', 'VBZ', 'JJ'],
                           ['NN', 'VBZ', 'RB', 'JJ'],
                           ['NN', 'NN', 'VBZ', 'JJ'],
                           ['NN', 'NN', 'VBZ', 'RB', 'JJ'],
                           ['NNS', 'VBZ', 'JJ'],
                           ['JJ', 'NN'],
                           ['JJ', 'NNS'],
                           ['JJR', 'NNS'],
                           ['JJS', 'NN'],
                           ['NN', 'JJ'],
                           ['NN', 'NN', 'JJ'],
                           ['NN', 'IN', 'RB', 'RB', 'JJ'],
                           ['NN', 'IN', 'RB', 'RB', 'JJ'],
                           ['NN', 'VBZ'],
                           ['NNP', 'RB', 'VBZ'],
                           ['NN', 'VBZ', 'DT', 'JJ'],
                           ['NN', 'VBZ', 'DT', 'RB', 'JJ'],
                           ['NN', 'VBZ', 'RB', 'DT', 'JJ'],
                           ['NN', 'RB', 'JJ'],
                           ['NN', 'RB', 'JJ', 'CC', 'JJ'],
                           ['NN', 'POS', 'JJ'],
                           ['NN', 'VBD', 'NNS'],
                           ['NN', 'NN', 'DT', 'NN'],
                           ['NN', 'VBZ', 'RB', 'JJ', 'TO', 'VB'],
                           ['NN', 'VBZ', 'JJR', 'IN', 'JJ']
                            ]
    for word, pos in noun_opinion:
        feature_opinion_syntax.append(pos)
    if feature_opinion_syntax in feature_syntax_list:
        return True


def genearte_summary_feature_opinion():
    feature_opinion_sent_list = extract_opinion_of_aspect_using_lexicon()
    # feature_opinion_sent_list = [('g3', 'worth', 'JJ', 14), ('zoom', 'nice', 'JJ', 53), ('battery', 'solid', 'JJ', 57),
    #                              ('pictures', 'easy', 'JJ', 61), ('zoom', 'works', 'VBZ', 63), ('zoom', 'bad', 'JJ', 163),
    #                              ('zoom', 'worse', 'JJ', 263), ('zoom', 'works', 'VBZ', 363), ('battery', 'nice', 'JJ', 157),
    #                              ('battery', 'best', 'JJ', 257)]
    feature_score_dict = {}
    for feature, opinion, o_tag, sent_id in feature_opinion_sent_list:
        opinion_tag = get_wordnet_pos(o_tag)
        negation(str(sent_id))

        syns = wordnet.synsets(opinion)

        if (feature not in feature_score_dict.keys()):
            feature_score_dict[feature] = {}
            feature_score_dict[feature]['Score'] = {}
            feature_score_dict[feature]['Sentence_id'] = {}
            feature_score_dict[feature]['Score']['pos'] = 0
            feature_score_dict[feature]['Score']['neg'] = 0
            feature_score_dict[feature]['Score']['neu'] = 0
            feature_score_dict[feature]['Sentence_id']['pos_id'] = []
            feature_score_dict[feature]['Sentence_id']['neg_id'] = []
            feature_score_dict[feature]['Sentence_id']['neu_id'] = []

        tag_synset_name = []
        for i in syns:
            if i.pos() in [opinion_tag]:
                synset_name = i.name()
                tag_synset_name.append(synset_name)
                # synset_name = i.name().split('.')[0] + '.' + opinion_tag + '.01'
            elif i.pos() in ['s']:
                tag_synset_name.append(i.name())

        if (len(tag_synset_name) != 0):
            pos, neg, neu = 0, 0, 0
            sentence_id = []
            each_word_orientation = sentiwordnet.senti_synset(tag_synset_name[0])
            # print(feature, each_word_orientation, sent_id)
            if each_word_orientation.pos_score() != 0 and each_word_orientation.neg_score() == 0:
                for f_key, f_value in feature_score_dict[feature].items():

                    if f_key == 'Score':
                        for score_key, score_value in f_value.items():
                            if score_key == 'pos':
                                if score_value:
                                    pos = score_value
                                    pos += 1
                                else:
                                    pos += 1
                    if f_key == 'Sentence_id':
                        for s_key, s_value in f_value.items():
                            if s_key == 'pos_id':
                                if s_value:
                                    sentence_id = s_value
                                    # sentence_id = list(str(s_value).split(','))
                                    sentence_id.append(sent_id)
                                    break
                                else:
                                    sentence_id.append(sent_id)

                feature_score_dict[feature]['Score']['pos'] = pos
                feature_score_dict[feature]['Sentence_id']['pos_id'] = sentence_id
            # For Negative
            elif each_word_orientation.neg_score() != 0 and each_word_orientation.pos_score() == 0:
                for f_key, f_value in feature_score_dict[feature].items():
                    if f_key == 'Score':
                        for score_key, score_value in f_value.items():
                            if score_key == 'neg':
                                if score_value:
                                    neg = score_value
                                    neg += 1
                                else:
                                    neg += 1
                    if f_key == 'Sentence_id':
                        for s_key, s_value in f_value.items():
                            if s_key == 'neg_id':
                                if s_value:
                                    sentence_id = s_value
                                    # sentence_id = list(str(s_value).split(','))
                                    sentence_id.append(sent_id)
                                    break
                                else:
                                    sentence_id.append(sent_id)

                feature_score_dict[feature]['Score']['neg'] = neg
                feature_score_dict[feature]['Sentence_id']['neg_id'] = sentence_id
            # For neutral
            elif each_word_orientation.pos_score() == 0 and each_word_orientation.neg_score() == 0:
                for f_key, f_value in feature_score_dict[feature].items():
                    if f_key == 'Score':
                        for score_key, score_value in f_value.items():
                            if score_key == 'neu':
                                if score_value:
                                    neu = score_value
                                    neu += 1
                                else:
                                    neu += 1
                    if f_key == 'Sentence_id':
                        for s_key, s_value in f_value.items():
                            if s_key == 'neu_id':
                                if s_value:
                                    sentence_id = s_value
                                    # sentence_id = list(str(s_value).split(','))
                                    sentence_id.append(sent_id)
                                    break
                                else:
                                    sentence_id.append(sent_id)

                feature_score_dict[feature]['Score']['neu'] = neu
                feature_score_dict[feature]['Sentence_id']['neu_id'] = sentence_id
            # For both positive and negative value
            elif each_word_orientation.pos_score() != 0 and each_word_orientation.neg_score() != 0:
                if each_word_orientation.pos_score() - each_word_orientation.neg_score() > 0:
                    for f_key, f_value in feature_score_dict[feature].items():
                        if f_key == 'Score':
                            for score_key, score_value in f_value.items():
                                if score_key == 'pos':
                                    if score_value:
                                        pos = score_value
                                        pos += 1
                                    else:
                                        pos += 1
                        if f_key == 'Sentence_id':
                            for s_key, s_value in f_value.items():
                                if s_key == 'pos_id':
                                    if s_value:
                                        sentence_id = s_value
                                        # sentence_id = list(str(s_value).split(','))
                                        sentence_id.append(sent_id)
                                        break
                                    else:
                                        sentence_id.append(sent_id)

                    feature_score_dict[feature]['Score']['pos'] = pos
                    feature_score_dict[feature]['Sentence_id']['pos_id'] = sentence_id
                elif each_word_orientation.neg_score() - each_word_orientation.pos_score() > 0:
                    for f_key, f_value in feature_score_dict[feature].items():
                        if f_key == 'Score':
                            for score_key, score_value in f_value.items():
                                if score_key == 'neg':
                                    if score_value:
                                        neg = score_value
                                        neg += 1
                                    else:
                                        neg += 1
                        if f_key == 'Sentence_id':
                            for s_key, s_value in f_value.items():
                                if s_key == 'neg_id':
                                    if s_value:
                                        sentence_id = s_value
                                        # sentence_id = list(str(s_value).split(','))
                                        sentence_id.append(sent_id)
                                        break
                                    else:
                                        sentence_id.append(sent_id)

                    feature_score_dict[feature]['Score']['neg'] = neg
                    feature_score_dict[feature]['Sentence_id']['neg_id'] = sentence_id
                elif each_word_orientation.pos_score() - each_word_orientation.neg_score() == 0 :
                    for f_key, f_value in feature_score_dict[feature].items():
                        if f_key == 'Score':
                            for score_key, score_value in f_value.items():
                                if score_key == 'neu':
                                    if score_value:
                                        neu = score_value
                                        neu += 1
                                    else:
                                        neu += 1
                        if f_key == 'Sentence_id':
                            for s_key, s_value in f_value.items():
                                if s_key == 'neu_id':
                                    if s_value:
                                        sentence_id = s_value
                                        # sentence_id = list(str(s_value).split(','))
                                        sentence_id.append(sent_id)
                                        break
                                    else:
                                        sentence_id.append(sent_id)

                    feature_score_dict[feature]['Score']['neu'] = neu
                    feature_score_dict[feature]['Sentence_id']['neu_id'] = sentence_id

    print(feature_score_dict)
    for feature_key, feature_values in feature_score_dict.items():
        pos, neg, neu = 0,0,0
        pos_sentences = []
        neg_sentences = []
        neu_sentences = []
        # print(feature_key, feature_values)
        for s_key, s_value in feature_values.items():
            # print(s_key, s_value)
            if s_key == 'Score':
                for score_key, score_value in s_value.items():
                    if score_key == 'pos':
                        pos = score_value
                    if score_key == 'neg':
                        neg = score_value
                    if score_key == 'neu':
                        neu = score_value
            if s_key == 'Sentence_id':
                for sent_id_key, sent_id_value in s_value.items():
                    if sent_id_key == 'pos_id':
                        pos_sentences = sent_id_value
                    if sent_id_key == 'neg_id':
                        neg_sentences = sent_id_value
                    if sent_id_key == 'neu_id':
                        neu_sentences = sent_id_value


        print("Feature = ", feature_key, "Positive = ", pos, "Negative = ", neg, "Neutral = ", neu,
              "Positive Sentence ", pos_sentences,
              "Negative sentence ", neg_sentences,
              "Neutral Sentence ", neu_sentences)


def get_wordnet_pos(opinion_tag):

    if opinion_tag in ['JJ', 'JJR', 'JJS']:
        return 'a'
    elif opinion_tag in ['VBZ', 'VBP', 'VBD']:
        return 'v'
    elif opinion_tag in ['NN', 'NNS']:
        return 'n'
    elif opinion_tag in ['RB']:
        return 'r'
    else:
        return None

def plot_in_graph():
    feature_score_dict = {'g3': {'Score': {'pos': 1, 'neg': 0, 'neu': 0}, 'Sentence_id': {'pos_id': [14], 'neg_id': [], 'neu_id': []}},
               'zoom': {'Score': {'pos': 1, 'neg': 2, 'neu': 2}, 'Sentence_id': {'pos_id': [53], 'neg_id': [163, 263], 'neu_id': [63, 363]}},
               'battery': {'Score': {'pos': 3, 'neg': 0, 'neu': 0}, 'Sentence_id': {'pos_id': [57, 157, 257], 'neg_id': [], 'neu_id': []}},
               'pictures': {'Score': {'pos': 1, 'neg': 0, 'neu': 0}, 'Sentence_id': {'pos_id': [61], 'neg_id': [], 'neu_id': []}}}
    features = []
    for feature_key, feature_values in feature_score_dict.items():
        pos, neg, neu = 0,0,0
        pos_sentences = []
        neg_sentences = []
        neu_sentences = []
        features.append(feature_key)
        # print(feature_key, feature_values)
        for s_key, s_value in feature_values.items():
            # print(s_key, s_value)

            if s_key == 'Score':
                for score_key, score_value in s_value.items():
                    if score_key == 'pos':
                        pos = score_value
                    if score_key == 'neg':
                        neg = score_value
                    if score_key == 'neu':
                        neu = score_value
            if s_key == 'Sentence_id':
                for sent_id_key, sent_id_value in s_value.items():
                    if sent_id_key == 'pos_id':
                        pos_sentences = sent_id_value
                    if sent_id_key == 'neg_id':
                        neg_sentences = sent_id_value
                    if sent_id_key == 'neu_id':
                        neu_sentences = sent_id_value

        print("Feature = ", feature_key, "Positive = ", pos, "Negative = ", neg, "Neutral = ", neu,
              "Positive Sentence ", pos_sentences,
              "Negative sentence ", neg_sentences,
              "Neutral Sentence ", neu_sentences)


def negation(sentence_id):
    print(sentence_id)
    sentence = database.fetch_sentnece_by_id(sentence_id)
    print(sentence)
    negative_word_list = ["aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
                          "ain’t", "aren’t", "can’t", "couldn’t", "daren’t", "didn’t", "doesn’t",
                          "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt","mustnt", "neither",
                          "don’t", "hadn’t", "hasn’t", "haven’t", "isn’t", "mightn’t", "mustn’t", "neednt", "needn’t",
                          "never", "none", "nope", "nor", "not", "nothing", "nowhere", "oughtnt", "shant", "shouldnt",
                          "uhuh", "wasnt", "werent", "oughtn’t", "shan’t", "shouldn’t", "uhuh",
                          "wasn’t", "weren’t", "without", "wont", "wouldnt", "won’t", "wouldn’t", "rarely", "seldom", "despite"]
# extract_opinion_of_aspect_using_lexicon()
genearte_summary_feature_opinion()