from nltk.corpus import wordnet


def similarity_grouping(aspect, aspect_list):
    aspect_word = aspect + ".n.01"
    new_list_without_aspect = [a for a in aspect_list if a not in aspect_word]
    for asp in new_list_without_aspect:
        try:
            w1 = wordnet.synset(aspect_word)
            compare_word = asp + ".n.01"
            w2 = wordnet.synset(compare_word)
            word_similarity = (w1.wup_similarity(w2))
            # print(asp, word_similarity)
            if word_similarity > 0.7:
                return asp
        except:
            pass