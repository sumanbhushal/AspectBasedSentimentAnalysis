import database, StanfordNLPServer


def stanford_pos_tagging(sentence_list):
    """
    Stanford POS Tagging and insert into database
    :param sentence_list: Sentence List for POS tagging
    """
    ids_pos_value = []
    for sent_id, review_id, sentences in sentence_list:
        nlp_server = StanfordNLPServer.SNLPServer()  # Calling StanfordNLPServer Class
        pos_tagged = getattr(nlp_server, 'pos')  # SNLPServer.pos (It allows to call methods based on the contents of a string instead of typing the method name.)
        combine_value = (sent_id, review_id, pos_tagged(sentences))
        ids_pos_value.append(combine_value)
    database.insert_postagged_sent_into_db(ids_pos_value)
