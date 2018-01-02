import re, config, database


def write_to_file(filename, output_content):
    """
    Write the content to external file
    :param filename: Name of file to name to external file name
    :param output_content: Content to write in the file
    """
    with open(config.MANUAL_LABLED_ASPECT_PATH + filename, 'a') as output:
        for text in output_content:
            output.write(text)


def calculate_relative_frequency_tags(pos_tagged_review_list):
    """
    Calculation to estimate the relative frequency of different tags following a certain tag
    :param pos_tagged_review_list: POS tagged sentence list
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
                    prev_pos_current_pos = (word_pos[word_pos.index(word_pos_position) - 1][1], pos)
                    tags_relative_frequency.append(prev_pos_current_pos)

    for current_prev_tag in tags_relative_frequency:
        if tags_relative_frequency_dictionary.keys() != current_prev_tag:
            tags_relative_frequency_dictionary[current_prev_tag] = tags_relative_frequency.count(current_prev_tag)

        combine_tag_frequency = sorted(tags_relative_frequency_dictionary.items(), key=lambda x: x[1], reverse=True)
        print(len(combine_tag_frequency), combine_tag_frequency)


def extract_manual_labeled_aspect(review):
    """
    Extract Manual labeled aspect from review file for evaluation purpose
    :param review: List of review
    :return: List of manual labeled aspect
    """
    product_aspect_list = []
    output_aspects = []
    aspect_dictionary = {}

    rg_exp_main = r"\w+.*\[?[+/-]\d\]?\#\#"
    product_aspect_list.append(re.findall(rg_exp_main, review))
    # print(product_aspect_list)
    product_aspect = []
    for aspect in product_aspect_list:
        for aa in aspect:
            # rg_exp_brackets = r"\[?[+/-]\d\]?\#\#|\[?[+/-]\d\]?\[?\w\]?|\[?[+/-]\d\]?"
            # product_aspect.append(re.sub(rg_exp_brackets, '', aa).lower())
            if len(aa.split(',')) == 1:
                rg_exp_brackets = r"\[?[+/-]\d\]?\#\#"
                product_aspect.append(re.sub(rg_exp_brackets, '', aa).lower())
            else:
                for split_word in aa.split(','):
                    if split_word == aa.split(',')[-1]:  # get the value of last element in the list
                        rg_exp_brackets = r"\[?[+/-]\d\]?\#\#"
                        product_aspect.append(re.sub(rg_exp_brackets, '', split_word.strip()).lower())
                    else:
                        rg_exp_brackets = r"\[?[+/-]\d\]?\[?\w\]?|\[?[+/-]\d\]?"
                        # print("check", split_word)
                        product_aspect.append(re.sub(rg_exp_brackets, '', split_word.strip()).lower())

    for asp in product_aspect:
        if aspect_dictionary.keys() != asp:
            aspect_dictionary[asp] = product_aspect.count(asp)
    sorted_aspects_with_count = sorted(aspect_dictionary.items(), key=lambda x: x[1], reverse=True)

    # replace the white space with the "_"
    for noun, count in sorted_aspects_with_count:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        noun_list_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', noun)
        new_noun_count_pair = (noun_list_replacing_space_with_underscore, count)
        output_aspects.append(new_noun_count_pair)
    return output_aspects


def extract_manual_annotated_aspect(filename, review_list):
    """
    Extract Manual labeled aspect and write to file
    :param filename: Name of file to name to external file name
    :param review_list: review lists to extract manual labeled aspects
    """
    manual_labeled_product_aspect = extract_manual_labeled_aspect(review_list)

    for word, count in manual_labeled_product_aspect:
        write_to_file(filename + "_ml_with_count.txt", word + '\n')


def extract_manual_annotated_asp_min_rev_sent_count(filename, review_list):
    """
    Extract Manual annotated aspect with 1% of minimum review sentence count
    :param filename: Name of file to name to external file name
    :param review_list: review lists to extract manual labeled aspects
    """
    manual_labeled_product_aspect = extract_manual_labeled_aspect(review_list)
    number_of_sentences = len(database.fetch_sentence_from_sentence_table())
    min_sent_count = round(0.01 * number_of_sentences)  # Minimum support count = 1% of total review sentences
    new_list = []
    for word, count in manual_labeled_product_aspect:
        if count > min_sent_count:
            write_to_file(filename + "_ml_sent_count.txt", word + '\n')
            new_list.append(word)
