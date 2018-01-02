import urllib.request
import re, database, pre_processing
from nltk.corpus import wordnet


def wiki_crawler(entity_name):
    """
    Creating url for Wikipedia Crawling
    :param entity_name: Name of entity
    :return: return list of candidate aspects from Wikipedia
    """
    base_url = 'https://en.wikipedia.org/wiki'
    entity_url = base_url + '/' + entity_name
    return extract_internal_link(entity_url)


def extract_internal_link(entity_url):
    """
    Extracting internal links from Wekipedia and retrieving candidate aspects from internal link
    :param entity_url: url refering Wekipedia
    :return: candidate aspects list
    """
    try:
        internal_link_word = []
        word_dict = {}
        request = urllib.request.urlopen(entity_url)
        request_data = str(request.read())
        final_list = []
        # print(request_data)

        # Extracting only internal link with the help of regular expression
        rg_exp_link = re.compile('(<a\\s+href="\\/wiki\\/\\w*?")', re.IGNORECASE | re.DOTALL)
        internal_link_list = re.findall(rg_exp_link, request_data)

        # Retrieving candidate aspects from internal link
        for link in internal_link_list:
            rg_exp_word = re.compile('(<a\\s+href="\\/wiki\\/)', re.IGNORECASE | re.DOTALL)
            word_without_link = re.sub(rg_exp_word, '', link)
            rg_exp_qouble_quto = re.compile('(")', re.IGNORECASE | re.DOTALL)
            final_word_list = re.sub(rg_exp_qouble_quto, '', word_without_link)

            internal_link_word.append(final_word_list)

        for word in internal_link_word:
            if word_dict.keys() != word:
                word_dict[word] = internal_link_word.count(word)

        for key, value in word_dict.items():
            final_list.append(key.lower())

        return final_list
    except Exception as e:
        print(str(e))


def product_features_from_wikipedia():
    """
    Get Entity from database and use it to crawl wikipeida
    Compare the candidate aspects with Wikipedia aspect list
    :return: entity name, genuine aspect list
    """
    entity_name = database.fetch_feature_for_wikipedia_crawl()
    noun_nounphrases_per_sent = database.fetch_noun_nounphrase()
    extracted_noun_nounphrases = []
    for aspect in noun_nounphrases_per_sent:
        # for count, aspect in extracted_aspect_list:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        aspect_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', aspect)
        extracted_noun_nounphrases.append(aspect_replacing_space_with_underscore)

    wiki_list = wiki_crawler(entity_name)
    wiki_feature_after_lemmatization = pre_processing.lemmatization(wiki_list)

    # Comparing frequent candidate aspects without aspects retrieve from Wikipedia
    exp_asp_intersection_wiki = []
    match_with_wiki_dict = {}
    for asp in extracted_noun_nounphrases:
        for s in filter(lambda x: asp == x, wiki_feature_after_lemmatization):
            exp_asp_intersection_wiki.append(asp)
    for asp in exp_asp_intersection_wiki:
        if match_with_wiki_dict.keys() != asp:
            match_with_wiki_dict[asp] = exp_asp_intersection_wiki.count(asp)

    # Checking the length of the aspects and take those with greater than 2
    new_list = []
    for key, value in match_with_wiki_dict.items():
        if len(key) > 2:
            new_list.append(key)

    final_wiki_list = filter_wiki_list(entity_name, new_list)
    return entity_name, final_wiki_list


def filter_wiki_list(entity_name, wiki_feature_list):
    """
    Measuring Similarity between Entity and features
    :param entity_name: Name of the entity
    :param wiki_feature_list: Wikipedia feature list
    :return: Aspect list after grouping similar aspects
    """
    new_wiki_list = []
    domain = entity_name + ".n.01"
    for wiki_asp in wiki_feature_list:
        try:
            w1 = wordnet.synset(domain)
            compare_word = wiki_asp + ".n.01"
            w2 = wordnet.synset(compare_word)
            word_similarity = (w1.wup_similarity(w2))
            if word_similarity > 0.5:
                new_wiki_list.append(wiki_asp)
        except:
            pass
    return new_wiki_list
