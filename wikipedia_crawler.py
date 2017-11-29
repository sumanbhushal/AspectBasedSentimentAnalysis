import urllib.request
import re, database, pre_processing

def wiki_crawler():
    entity_name = database.fetch_feature_for_wikipedia_crawl()
    base_url = 'https://en.wikipedia.org/wiki'
    entity_url = base_url + '/' + entity_name
    return extract_internal_link(entity_url)

def extract_internal_link(entity_url):
    try:
        internal_link_word = []
        word_dict = {}
        request = urllib.request.urlopen(entity_url)
        request_data = str(request.read())
        final_list = []
        # print(request_data)

        rg_exp_link = re.compile('(<a\\s+href="\\/wiki\\/\\w*?")', re.IGNORECASE | re.DOTALL)

        internal_link_list = re.findall(rg_exp_link, request_data)
        # print(internal_link_list)
        for link in internal_link_list:
            rg_exp_word = re.compile('(<a\\s+href="\\/wiki\\/)', re.IGNORECASE | re.DOTALL)
            word_without_link = re.sub(rg_exp_word, '', link)
            rg_exp_qouble_quto = re.compile('(")', re.IGNORECASE | re.DOTALL)
            final_word_list = re.sub(rg_exp_qouble_quto, '', word_without_link)

            internal_link_word.append(final_word_list)

        for word in internal_link_word:
            if(word_dict.keys()!= word):
                word_dict[word] = internal_link_word.count(word)

        for key, value in word_dict.items():
            final_list.append(key.lower())

        return final_list
    except Exception as e:
        print(str(e))

def product_features_from_wikipedia():
    # wikipedia Crawler
    noun_nounphrases_per_sent = database.fetch_noun_nounphrase()
    extracted_noun_nounphrases = []
    for aspect in noun_nounphrases_per_sent:
        # for count, aspect in extracted_aspect_list:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        aspect_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', aspect)
        extracted_noun_nounphrases.append(aspect_replacing_space_with_underscore)
    wiki_list = wiki_crawler()

    exp_asp_intersection_wiki = []
    match_with_wiki_dict = {}
    for asp in extracted_noun_nounphrases:
        for s in filter(lambda x: asp == x, wiki_list):
            exp_asp_intersection_wiki.append(asp)
    for asp in exp_asp_intersection_wiki:
        if (match_with_wiki_dict.keys() != asp):
            match_with_wiki_dict[asp] = exp_asp_intersection_wiki.count(asp)

    new_list = []
    for key, value in match_with_wiki_dict.items():
        if len(key) > 2:
            new_list.append(key)

    feature_after_lemmatization = pre_processing.lemmatization(new_list)
    return feature_after_lemmatization

# print(len(wiki_crawler('phone')),wiki_crawler('phone'))
