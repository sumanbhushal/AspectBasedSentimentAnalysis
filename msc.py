import re


def extract_manual_labeled_aspect(review):
    product_aspect_list = []
    aspect_dictionary = {}
    rg_exp_for_3plus = re.compile('(\\w+-(?:[a-z][a-z]+)\\s+\\w+\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_for_3plus, review))

    # Removing explicit product aspect formed with two words and a hyperlink and sentiment score
    rg_exp_for_2plus = re.compile('(\\w+-(?:[a-z][a-z]+)\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_for_2plus, review))

    # Removing explict product aspect with alphanumeric characters and sentiment score
    rg_exp_alphanumeric = re.compile('((?:[a-z][a-z]*[0-9]+[a-z0-9]*)\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_alphanumeric, review))

    # Removing explict product aspect with two words separated with space and sentiment score
    rg_exp_two_words_aspects = re.compile('(\\w+\\s+\\w+\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_two_words_aspects, review))

    # Removing explict product aspect with single words and sentiment score
    rg_exp_single_words_aspects = re.compile('(\\w+\\[.*?\\])', re.IGNORECASE | re.DOTALL)
    product_aspect_list.append(re.findall(rg_exp_single_words_aspects, review))
    # print(len(product_aspect_list), product_aspect_list)

    product_aspect = []
    for aspect in product_aspect_list:
        for aa in aspect:
            rg_exp_brackets = re.compile('(\\[.*?\\])', re.IGNORECASE | re.DOTALL)
            product_aspect.append(re.sub(rg_exp_brackets, '', aa).lower())
    # print(len(product_aspect),product_aspect)

    for aspect in product_aspect:
        if (aspect_dictionary.keys()!= aspect):
            aspect_dictionary[aspect] = product_aspect.count(aspect)
    output_aspects = sorted(aspect_dictionary.items(), key=lambda x: x[1], reverse=True)
    return output_aspects
    #print(len(outputAspect), outputAspect)