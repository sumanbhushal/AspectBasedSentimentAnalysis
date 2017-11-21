import urllib.request
import re, database

def wiki_crawler():
    entity_name = database.fetch_feature_for_wikipedia_crawl()
    print(entity_name)
    base_url = 'https://en.wikipedia.org/wiki'
    entity_url = base_url + '/' + entity_name
    print(entity_url)
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

# print(len(wiki_crawler('phone')),wiki_crawler('phone'))
