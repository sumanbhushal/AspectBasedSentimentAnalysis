from nltk.corpus import wordnet


def similarity_grouping(aspect, aspect_list):
    """
    Similarity Aspect Grouping
    :param aspect: aspect
    :param aspect_list: aspect list
    :return: return the aspect similarity to another aspect
    """
    new_list_without_aspect = [a for a in aspect_list if a not in aspect]
    aspect_word = aspect + ".n.01"
    for asp in new_list_without_aspect:
        try:
            w1 = wordnet.synset(aspect_word)
            compare_word = asp + ".n.01"
            w2 = wordnet.synset(compare_word)
            word_similarity = (w1.wup_similarity(w2))
            if word_similarity > 0.7:
                return asp
        except:
            pass


def redundent_grouping(aspect, aspect_list):
    """
    Redundent Grouping
    :param aspect: aspect name
    :param aspect_list: aspect list
    :return: return match aspect in list
    """
    new_list_without_aspect = [a for a in aspect_list if a != aspect]
    if len(aspect.split()) > 1:
        match_aspect = []
        for word in aspect.split():
            for list_asp in new_list_without_aspect:
                if word == list_asp:
                    match_aspect.append(list_asp)
        return match_aspect
