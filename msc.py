import re, config, database



def write_to_file(filename, output_content):
    with open(config.Manual_labled_aspect_path + filename, 'a') as output:
        for text in output_content:
            output.write(text)



def calculate_relative_frequency_tags(pos_tagged_review_list):
    """
    Calculation to estimate the relative frequency of different tags following a certain tag
    :param pos_tagged_review_list:
    :return:
    """
    tags_relative_frequency = []
    tags_relative_frequency_dictionary = {}
    pos_tags = ['NN', 'JJ', 'VB', 'DT', '.', 'VBP']
    print(pos_tagged_review_list)
    for tags in pos_tags:
        for word_pos in pos_tagged_review_list:
            for word, pos in word_pos:
                if pos in pos_tags:
                    word_pos_position = (word, pos)
                    prev_pos_current_pos = ( word_pos[word_pos.index(word_pos_position) - 1][1], pos)
                    tags_relative_frequency.append(prev_pos_current_pos)

    for current_prev_tag in tags_relative_frequency:
        if (tags_relative_frequency_dictionary.keys()!= current_prev_tag):
            tags_relative_frequency_dictionary[current_prev_tag] = tags_relative_frequency.count(current_prev_tag)

        combine_tag_frequency = sorted(tags_relative_frequency_dictionary.items(), key=lambda x: x[1], reverse=True)
    print(len(combine_tag_frequency), combine_tag_frequency)


def extract_manual_labeled_aspect(review):
    product_aspect_list = []
    output_aspects = []
    aspect_dictionary = {}

    rg_exp_for_3plus = re.compile('(\\w+-(?:[a-z][a-z]+)\\s+\\w+\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_for_3plus, review))
    #print(re.findall(rg_exp_for_3plus, review))

    # extract explicit product aspect formed with two words and a hyperlink and sentiment score
    rg_exp_for_2plus = re.compile('(\\w+-(?:[a-z][a-z]+)\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_for_2plus, review))

    # extract explict product aspect with alphanumeric characters and sentiment score
    rg_exp_alphanumeric = re.compile('((?:[a-z][a-z]*[0-9]+[a-z0-9]*)\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_alphanumeric, review))

    # extract explict product aspect with two words separated with space and sentiment score
    rg_exp_two_words_aspects = re.compile('(\\w+\\s+\\w+\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_two_words_aspects, review))

    # extract explict product aspect with single words and sentiment score
    rg_exp_single_words_aspects = re.compile('(\\w+\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_single_words_aspects, review))
    # print(len(product_aspect_list), product_aspect_list)

    product_aspect = []
    for aspect in product_aspect_list:
        for aa in aspect:
            rg_exp_brackets = re.compile('(\\[.*?\\])', re.IGNORECASE | re.DOTALL)
            product_aspect.append(re.sub(rg_exp_brackets, '', aa).lower())
    # print(len(product_aspect),product_aspect)

    for asp in product_aspect:
        if (aspect_dictionary.keys()!= asp):
            aspect_dictionary[asp] = product_aspect.count(asp)
    sorted_aspects_with_count = sorted(aspect_dictionary.items(), key=lambda x: x[1], reverse=True)

    for noun, count in sorted_aspects_with_count:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        noun_list_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', noun)
        new_noun_count_pair = (noun_list_replacing_space_with_underscore, count)
        output_aspects.append(new_noun_count_pair)
     #print(len(output_aspects), output_aspects)
    return output_aspects


def extract_new_manual_labeled_aspect():
    review = open(config.Output_file_path + "M_label Hitachi roter.txt", "r").read()
    product_aspect_list = []
    output_aspects = []
    aspect_dictionary = {}

    rg_exp_for_3plus = rg_exp = re.compile('(<feature>\\w+-(?:[a-z][a-z]+\\s+\\w+)<\\/feature>)', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_for_3plus, review))
    # print(re.findall(rg_exp_for_3plus, review))

    # extract explicit product aspect formed with two words and a hyperlink and sentiment score
    rg_exp_for_2plus = re.compile('(<feature>\\w+-(?:[a-z][a-z]+\\s+\\w+)<\\/feature>)', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_for_2plus, review))

    # extract explicit product aspect formed with two words and a hyperlink and sentiment score
    rg_exp_for_1plus = re.compile('(<feature>\\w+-\\w+<\\/feature>)', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_for_1plus, review))

    # extract explict product aspect with alphanumeric characters and sentiment score
    rg_exp_alphanumeric = re.compile('(<feature>(?:[a-z][a-z]*[0-9]+[a-z0-9]*)<\\/feature>)', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_alphanumeric, review))

    # extract explict product aspect with two words separated with space and sentiment score
    rg_exp_two_words_aspects = rg_exp = re.compile('(<feature>\\w+\\s+\\w+<\\/feature>)', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_two_words_aspects, review))

    # extract explict product aspect with single words and sentiment score
    rg_exp_single_words_aspects = re.compile('(<feature>\\w+<\\/feature>)', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_single_words_aspects, review))

    product_aspect = []
    for aspect in product_aspect_list:
        for aa in aspect:
            rg_exp_opening_featrue_tag = re.compile('(<feature>)', re.IGNORECASE | re.DOTALL)
            product_aspect_removing_opening_tag = re.sub(rg_exp_opening_featrue_tag, '', aa)
            rg_exp_closing_feature_tag = re.compile('(<\\/feature>)', re.IGNORECASE | re.DOTALL)
            product_aspect_removing_closing_tag = re.sub(rg_exp_closing_feature_tag, '', product_aspect_removing_opening_tag)
            product_aspect.append(re.sub(rg_exp_closing_feature_tag, '', product_aspect_removing_closing_tag).lower())
    #print(len(product_aspect), product_aspect)

    for asp in product_aspect:
        if (aspect_dictionary.keys()!= asp):
            aspect_dictionary[asp] = product_aspect.count(asp)
    sorted_aspects_with_count = sorted(aspect_dictionary.items(), key=lambda x: x[1], reverse=True)

    for noun, count in sorted_aspects_with_count:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        noun_list_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', noun)
        new_noun_count_pair = (noun_list_replacing_space_with_underscore, count)
        output_aspects.append(new_noun_count_pair)
    #print(len(output_aspects), output_aspects)
    return output_aspects


def generate_unique_list_of_manual_labeled_aspect(filename):
    file = open(config.Output_file_path + filename + ".txt", "r").read()
    manual_labeled_list = file.split('\n')
    unique_aspect_list = []
    for asp in manual_labeled_list:
        if asp not in unique_aspect_list:
            unique_aspect_list.append(asp)
    for aspect in unique_aspect_list:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        aspect_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', aspect)
        write_to_file(filename+"_ml.txt", aspect_replacing_space_with_underscore + '\n')
    print(len(unique_aspect_list),unique_aspect_list)