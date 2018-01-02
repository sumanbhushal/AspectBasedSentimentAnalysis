import database, config
from nltk import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet
import aspect_grouping
from itertools import combinations


def extract_opinion_of_aspect_using_lexicon():
    """
    Extract opinion words from the review sentences using lexicon (Hu and Liu, 2004)
    :return: feature, sentiment word, POS tag for sentiment word and sentence id, e.g. ('zoom', 'nice', 'JJ', 53)
    """

    # Reading the opinion lexicon
    positive_lexicon = read_lexicon(config.LEXICONS_PATH + "positive-words.txt")
    negative_lexicon = read_lexicon(config.LEXICONS_PATH + "negative-words.txt")

    # Fetch the final product aspect list obtained from aspect extraction
    features_list_database = database.fetch_final_product_aspect_list()
    features_list = []
    for f in features_list_database:
        # Handling aspect with single word and multiple word
        if len(f.split()) == 1 and f not in features_list:
            features_list.append(f)
        else:
            redundant_aspect_list = []
            for i in range(len(f.split())):
                combine = combinations(f.split(), i + 1)
                for c in combine:
                    redundant_aspect_list.append(" ".join(c))

            for asp in redundant_aspect_list:
                if asp not in features_list:
                    features_list.append(asp)

    # combining the positive and negative word from lexicon
    lex_word_list = []
    for pos_lex in positive_lexicon:
        lex_word_list.append(pos_lex)
    for neg_lex in negative_lexicon:
        lex_word_list.append(neg_lex)

    # Fetch POS tagged sentence list for comparing to get the sentence and opinion word with its POS tag
    sentence_in_reviews = database.fetach_pos_tagged_sentence()
    sentence_containing_feature_opinion = []

    # Find the sentence with aspect, opinion and their position
    for sent_id, review_id, sentences in sentence_in_reviews:
        opinion_word_and_position = []
        feature_word_and_position = []
        sentence = eval(sentences)
        index = 0
        prev_word = ''

        # Extract the opinion word with its tag and index
        for word, tag in sentence:
            current_word = ''
            for lex_word in lex_word_list:
                if word == lex_word:
                    word_tag_index = (word, tag, index)
                    opinion_word_and_position.append(word_tag_index)

            # Extract the aspect with its tag and index
            for feature in features_list:
                # Extracting aspect with single word and multiple word
                if len(feature.split()) == 1:
                    if feature == word:
                        feature_tag_index = (feature, tag, index)
                        feature_word_and_position.append(feature_tag_index)
                else:
                    complete_word = ''
                    for i in range(len(feature.split())):
                        if feature.split()[i] == word:
                            if prev_word != '':
                                current_word = prev_word + ' ' + feature.split()[i]
                            else:
                                current_word = feature.split()[i]
                            prev_word = current_word
                    if len(current_word) != 1 and current_word != '':
                        complete_word = current_word
                    if complete_word == feature:
                        feature_tag_index = (feature, tag, index)
                        feature_word_and_position.append(feature_tag_index)
            index += 1
        # Checking backward, if feature position < opinion position and If difference <= 4
        # if more than one, take the close feature
        # If not present in backwards direction look at forward and check if distance < 3
        if opinion_word_and_position:
            for o_word, o_tag, o_index in opinion_word_and_position:
                opinion_position = o_index
                opinion_word = o_word

                if feature_word_and_position:
                    for p_word, p_tag, p_index in feature_word_and_position:
                        feature_position = p_index
                        feature_word = p_word

                        calculate_difference_in_distance = opinion_position - feature_position
                        end_element = calculate_difference_in_distance + 1
                        subjective_sentence = []
                        # Checking Backward
                        if feature_position < opinion_position and calculate_difference_in_distance <= 4:
                            for i in range(end_element):
                                ind_value = sentence[feature_position + i]
                                subjective_sentence.append(ind_value)
                            # Calling method to check the syntatic structure
                            sent_in_freq_tag = compare_opinion_syntax(subjective_sentence)
                            if sent_in_freq_tag == True:
                                feature_opinion_sent = (feature_word, opinion_word, o_tag, sent_id)
                                sentence_containing_feature_opinion.append(feature_opinion_sent)
                        # Checking Forward
                        elif feature_position > opinion_position:
                            distance_difference = feature_position - opinion_position
                            end_element = distance_difference + 1
                            if distance_difference < 3:
                                for i in range(end_element):
                                    ind_value = sentence[opinion_position + i]
                                    subjective_sentence.append(ind_value)
                                # Calling method to check the syntatic structure
                                sent_in_freq_tag = compare_opinion_syntax(subjective_sentence)
                                if sent_in_freq_tag == True:
                                    feature_opinion_sent = (feature_word, opinion_word, o_tag, sent_id)
                                    sentence_containing_feature_opinion.append(feature_opinion_sent)
    return sentence_containing_feature_opinion


def read_lexicon(path):
    """
    Read the opinion lexicon
    :param path: path for opinion lexicon
    :return: List of opinion words
    """
    lexicon = []

    with open(path, 'r') as file:
        for line in file:
            lexicon.append(line.strip())
    return lexicon


def compare_opinion_syntax(noun_opinion):
    """
    Validate the syntatic structure of text
    :param noun_opinion: POS tag between aspect and opinion
    :return: return True if the relationship is matched
    """
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
                           ['NN', 'VBZ', 'JJR', 'IN', 'JJ'],
                           ['NN', 'IN', 'DT', 'JJ']
                           ]
    for word, pos in noun_opinion:
        feature_opinion_syntax.append(pos)
    if feature_opinion_syntax in feature_syntax_list:
        return True


def genearate_summary_feature_opinion():
    """
    Generate Sentiment Summary based on feature, sentiment word, POS tag for sentiment word and
    sentence id, e.g. ('zoom', 'nice', 'JJ', 53)
    Insert final restult of sentiment orientation of the aspect in database along with sentence ids
    """
    feature_opinion_sent_list = extract_opinion_of_aspect_using_lexicon()

    feature_score_dict = {}
    for feature, opinion, o_tag, sent_id in feature_opinion_sent_list:
        # Convert Stanford POS tag to WordNet pos tag (e.g. JJ => a)
        opinion_tag = get_wordnet_pos(o_tag)

        # negation handling
        negation = is_negation(str(sent_id))

        # Get the synsets of the opinion word from WordNet to match the POS tag of opinion word
        syns = wordnet.synsets(opinion)

        if feature not in feature_score_dict.keys():
            feature_score_dict[feature] = {}
            feature_score_dict[feature]['Score'] = {}
            feature_score_dict[feature]['Sentence_id'] = {}
            feature_score_dict[feature]['Score']['pos'] = 0
            feature_score_dict[feature]['Score']['neg'] = 0
            feature_score_dict[feature]['Score']['neu'] = 0
            feature_score_dict[feature]['Sentence_id']['pos_id'] = []
            feature_score_dict[feature]['Sentence_id']['neg_id'] = []
            feature_score_dict[feature]['Sentence_id']['neu_id'] = []

        # Get the synset with the respective POS
        tag_synset_name = []
        for i in syns:
            if i.pos() in [opinion_tag]:
                synset_name = i.name()
                tag_synset_name.append(synset_name)
            elif i.pos() in ['s']:
                tag_synset_name.append(i.name())

        if len(tag_synset_name) != 0:
            pos, neg, neu = 0, 0, 0
            sentence_id = []

            # Get the sentiment score (positive and negative score) from SentiWordNet
            each_word_orientation = sentiwordnet.senti_synset(tag_synset_name[0])
            # For Positive Sentiment
            if each_word_orientation.pos_score() != 0 and each_word_orientation.neg_score() == 0:
                if not negation:
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
                                        sentence_id.append(sent_id)
                                        break
                                    else:
                                        sentence_id.append(sent_id)
                    feature_score_dict[feature]['Score']['pos'] = pos
                    feature_score_dict[feature]['Sentence_id']['pos_id'] = sentence_id
                else:
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
                                        sentence_id.append(sent_id)
                                        break
                                    else:
                                        sentence_id.append(sent_id)

                    feature_score_dict[feature]['Score']['neg'] = neg
                    feature_score_dict[feature]['Sentence_id']['neg_id'] = sentence_id
            # For Negative
            elif each_word_orientation.neg_score() != 0 and each_word_orientation.pos_score() == 0:
                if not negation:
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
                else:
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
                elif each_word_orientation.pos_score() - each_word_orientation.neg_score() == 0:
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
                                        sentence_id.append(sent_id)
                                        break
                                    else:
                                        sentence_id.append(sent_id)

                    feature_score_dict[feature]['Score']['neu'] = neu
                    feature_score_dict[feature]['Sentence_id']['neu_id'] = sentence_id

    """ Similarity Grouping (photo = > picture)"""
    aspect_list_for_grouping = []
    aspect_after_similarity_grouping = {}
    for feature_key, feature_values in feature_score_dict.items():
        aspect_list_for_grouping.append(feature_key)

    for feature_key, feature_values in feature_score_dict.items():
        if feature_key in aspect_list_for_grouping:
            similar_aspect = aspect_grouping.similarity_grouping(feature_key, aspect_list_for_grouping)
            if similar_aspect:
                new_pos_value, new_neg_value, new_neu_value = 0, 0, 0
                new_pos_sentences = []
                new_neg_sentences = []
                new_neu_sentences = []
                Score = {}
                Sentence_id = {}
                similar_aspect_value_to_append = feature_score_dict.get(similar_aspect)

                for s_key, s_value in feature_values.items():
                    if s_key == 'Score':
                        for score_key, score_value in s_value.items():
                            if score_key == 'pos':
                                new_pos_value = score_value
                            if score_key == 'neg':
                                new_neg_value = score_value
                            if score_key == 'neu':
                                new_neu_value = score_value
                    if s_key == 'Sentence_id':
                        for sent_id_key, sent_id_value in s_value.items():
                            if sent_id_key == 'pos_id':
                                new_pos_sentences.extend(sent_id_value)
                            if sent_id_key == 'neg_id':
                                new_neg_sentences.extend(sent_id_value)
                            if sent_id_key == 'neu_id':
                                new_neu_sentences.extend(sent_id_value)
                for s_key, s_value in similar_aspect_value_to_append.items():
                    if s_key == 'Score':
                        for score_key, score_value in s_value.items():
                            if score_key == 'pos':
                                new_pos_value = new_pos_value + score_value
                            if score_key == 'neg':
                                new_neg_value = new_neg_value + score_value
                            if score_key == 'neu':
                                new_neu_value = new_neu_value + score_value
                    if s_key == 'Sentence_id':
                        for sent_id_key, sent_id_value in s_value.items():
                            if sent_id_key == 'pos_id':
                                new_pos_sentences.extend(sent_id_value)
                            if sent_id_key == 'neg_id':
                                new_neg_sentences.extend(sent_id_value)
                            if sent_id_key == 'neu_id':
                                new_neu_sentences.extend(sent_id_value)
                Score['pos'] = new_pos_value
                Score['neg'] = new_neg_value
                Score['neu'] = new_neu_value
                Sentence_id['pos_id'] = new_pos_sentences
                Sentence_id['neg_id'] = new_neg_sentences
                Sentence_id['neu_id'] = new_neu_sentences

                aspect_after_similarity_grouping[feature_key] = {}
                aspect_after_similarity_grouping[feature_key]['Score'] = Score
                aspect_after_similarity_grouping[feature_key]['Sentence_id'] = Sentence_id
                aspect_list_for_grouping.remove(similar_aspect)
            else:
                aspect_after_similarity_grouping[feature_key] = feature_values

    """ Redundant Grouping (picture = > picture quality)"""
    sorted_dictionary = {}
    # Sorted dictionary based on longer aspect list (e.g, picture quality then picture)
    for data in sorted(aspect_after_similarity_grouping, key=lambda x: len(x), reverse=True):
        sorted_dictionary[data] = aspect_after_similarity_grouping[data]

    aspect_list_after_similarity_grouping = []
    final_aspect_after_grouping = {}
    for feature_key, feature_values in sorted(sorted_dictionary.items()):
        aspect_list_after_similarity_grouping.append(feature_key)

    for feature_key, feature_values in sorted_dictionary.items():
        if feature_key in aspect_list_after_similarity_grouping:
            redundent_aspect = aspect_grouping.redundent_grouping(feature_key, aspect_list_after_similarity_grouping)
            if redundent_aspect:
                new_pos_value, new_neg_value, new_neu_value = 0, 0, 0
                new_pos_sentences = []
                new_neg_sentences = []
                new_neu_sentences = []
                Score = {}
                Sentence_id = {}

                for s_key, s_value in feature_values.items():
                    if s_key == 'Score':
                        for score_key, score_value in s_value.items():
                            if score_key == 'pos':
                                new_pos_value = score_value
                            if score_key == 'neg':
                                new_neg_value = score_value
                            if score_key == 'neu':
                                new_neu_value = score_value
                    if s_key == 'Sentence_id':
                        for sent_id_key, sent_id_value in s_value.items():
                            if sent_id_key == 'pos_id':
                                new_pos_sentences.extend(sent_id_value)
                            if sent_id_key == 'neg_id':
                                new_neg_sentences.extend(sent_id_value)
                            if sent_id_key == 'neu_id':
                                new_neu_sentences.extend(sent_id_value)
                for aspect in redundent_aspect:
                    redundent_aspect_value_to_append = sorted_dictionary.get(aspect)

                    for s_key, s_value in redundent_aspect_value_to_append.items():
                        if s_key == 'Score':
                            for score_key, score_value in s_value.items():
                                if score_key == 'pos':
                                    new_pos_value = new_pos_value + score_value
                                if score_key == 'neg':
                                    new_neg_value = new_neg_value + score_value
                                if score_key == 'neu':
                                    new_neu_value = new_neu_value + score_value
                        if s_key == 'Sentence_id':
                            for sent_id_key, sent_id_value in s_value.items():
                                if sent_id_key == 'pos_id':
                                    new_pos_sentences.extend(sent_id_value)
                                if sent_id_key == 'neg_id':
                                    new_neg_sentences.extend(sent_id_value)
                                if sent_id_key == 'neu_id':
                                    new_neu_sentences.extend(sent_id_value)
                        Score['pos'] = new_pos_value
                        Score['neg'] = new_neg_value
                        Score['neu'] = new_neu_value

                    Sentence_id['pos_id'] = new_pos_sentences
                    Sentence_id['neg_id'] = new_neg_sentences
                    Sentence_id['neu_id'] = new_neu_sentences
                    aspect_list_after_similarity_grouping.remove(aspect)

                final_aspect_after_grouping[feature_key] = {}
                final_aspect_after_grouping[feature_key]['Score'] = Score
                final_aspect_after_grouping[feature_key]['Sentence_id'] = Sentence_id
            else:
                final_aspect_after_grouping[feature_key] = feature_values

    sentiment_analysis_result_insert_into_db = []
    for feature_key, feature_values in final_aspect_after_grouping.items():
        pos, neg, neu = 0, 0, 0
        pos_sentences = []
        neg_sentences = []
        neu_sentences = []
        for s_key, s_value in feature_values.items():
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
        all_value_per_aspect = (feature_key, pos, neg, neu, pos_sentences, neg_sentences, neu_sentences)
        sentiment_analysis_result_insert_into_db.append(all_value_per_aspect)

        print("Feature = ", feature_key, "Positive = ", pos, "Negative = ", neg, "Neutral = ", neu,
              "Positive Sentence ", pos_sentences,
              "Negative sentence ", neg_sentences,
              "Neutral Sentence ", neu_sentences)

    # Inserting final sentiment result in database
    database.insert_sentiment_analysis_result(sentiment_analysis_result_insert_into_db)


def get_wordnet_pos(opinion_tag):
    """
    Convert Stanford POS tag to WordNet pos tag (e.g. JJ => a)
    :param opinion_tag: Stanford POS tag (e.g. JJ)
    :return: WordNet pos tag (e.g. a)
    """
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


def is_negation(sentence_id):
    """
    Handling Negation
    :param sentence_id: sentence id
    :return: return True if sentence contain negation word
    """
    sentence = database.fetch_sentnece_by_id(sentence_id)
    word_tokenize_sent = word_tokenize(" ".join(str(x) for x in sentence))
    negative_word_list = ["aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
                          "ain’t", "aren’t", "can’t", "couldn’t", "daren’t", "didn’t", "doesn’t",
                          "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
                          "don’t", "hadn’t", "hasn’t", "haven’t", "isn’t", "mightn’t", "mustn’t", "neednt", "needn’t",
                          "never", "none", "nope", "nor", "not", "nothing", "nowhere", "oughtnt", "shant", "shouldnt",
                          "uhuh", "wasnt", "werent", "oughtn’t", "shan’t", "shouldn’t", "uhuh",
                          "wasn’t", "weren’t", "without", "wont", "wouldnt", "won’t", "wouldn’t", "rarely", "seldom",
                          "despite", "n't"]

    for word in word_tokenize_sent:
        for neg_word in negative_word_list:
            if word == neg_word:
                return True
