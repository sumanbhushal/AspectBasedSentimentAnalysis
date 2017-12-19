import pymysql, pre_processing
from apyori import apriori

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Nepal12',
        db='thesis')
except pymysql.connector.Error as err:
    print(err)


cursor = connection.cursor()


def insert_into_review_table(review):
    insert_query = ("INSERT INTO review "
                    "(review)"
                    "VALUES (%s)")
    cursor.execute(insert_query, review)
    connection.commit()


def insert_sentence_into_sentence_table():
    truncate_sentence_table_sql = 'TRUNCATE TABLE sentences'
    cursor.execute(truncate_sentence_table_sql)

    sql = 'SELECT * from review'
    cursor.execute(sql)
    reviews = cursor.fetchall()
    for id, review in reviews:
        for rw in review.split("\n"):
            if not rw.isspace() and rw != '':
                sentence = pre_processing.lemmatization_sentence(rw)
                insert_sentence_query(id, sentence.lower())


def insert_sentence_query(review_id, sentence):
    if sentence != ' ':
        insert_value = (review_id, sentence)
        insert_query = ("INSERT INTO sentences "
                        "(review_id, sentence)"
                        "VALUES (%s, %s)")
        cursor.execute(insert_query, insert_value)
    connection.commit()


def fetch_sentences_from_review(review):
    truncate_review_table_sql = 'TRUNCATE TABLE review'
    cursor.execute(truncate_review_table_sql)

    for rw in review.split("[t]"):
        if rw != '':
            filter_rw = pre_processing.review_cleanup_labeled_data(rw)
            filter_symbol_rw = pre_processing.review_cleanup_symbols(filter_rw)
            insert_into_review_table(filter_symbol_rw)

    insert_sentence_into_sentence_table()
    return fetch_sentence_from_sentence_table()


def fetch_sentence_from_sentence_table():
    select_sql = 'SELECT * from sentences'
    cursor.execute(select_sql)
    return cursor.fetchall()

# Inserting POS tagged Sentence into database
def insert_postagged_sent_into_db(pos_tagged_sentences):
    truncate_pos_tagged_sentences_table_sql = 'TRUNCATE TABLE pos_tagged_sentences'
    cursor.execute(truncate_pos_tagged_sentences_table_sql)

    for sent_id, review_id, sent in pos_tagged_sentences:
        convert_sent_into_string = str(sent)
        insert_value = (sent_id, review_id, convert_sent_into_string)
        insert_query = ("INSERT INTO pos_tagged_sentences "
                        "(sentence_id, review_id, pos_tagged_sentences)"
                        "VALUES (%s, %s, %s)")
        cursor.execute(insert_query, insert_value)
    connection.commit()

# Fetching POS tagged Sentence from Database
def fetach_pos_tagged_sentence():
    pos_tagged_review = []
    select_sql_query = 'SELECT * From pos_tagged_sentences'
    cursor.execute(select_sql_query)
    # row = cursor.fetchall()
    pos_tagged_review = list(cursor)
    return pos_tagged_review


# def insert_nouns_chunks_per_sentence_into_db(nouns_per_sent):
#     trucate_table('nouns_chunks_per_sentence')
#     for sent_id, review_id, noun_set in nouns_per_sent:
#         if noun_set != '':
#             nouns_in_sent = ''
#             index = 0
#             for noun in noun_set:
#                 if index != len(noun_set)-1:
#                     nouns_in_sent += noun + ','
#                     index += 1
#                 else:
#                     nouns_in_sent += noun
#
#             insert_value = (review_id, sent_id, nouns_in_sent)
#             insert_query = ("INSERT INTO nouns_chunks_per_sentence "
#                             "(review_id, sentence_id, nouns)"
#                             "VALUES (%s, %s, %s)")
#             cursor.execute(insert_query, insert_value)
#     connection.commit()

def insert_nouns_list_per_sentence_into_db(nouns_per_sent):
    trucate_table('nouns_list_per_sentence')
    for sent_id, review_id, noun_set in nouns_per_sent:
        if noun_set != '':
            nouns_in_sent = ''
            index = 0
            for noun in noun_set:
                if index != len(noun_set)-1:
                    nouns_in_sent += noun + ','
                    index += 1
                else:
                    nouns_in_sent += noun

            insert_value = (review_id, sent_id, nouns_in_sent)
            insert_query = ("INSERT INTO nouns_list_per_sentence "
                            "(review_id, sentence_id, nouns)"
                            "VALUES (%s, %s, %s)")
            cursor.execute(insert_query, insert_value)
    connection.commit()


def fetch_nouns_per_sentence():
    select_sql = 'SELECT * from nouns_list_per_sentence'
    cursor.execute(select_sql)
    return cursor.fetchall()

def fetch_noun_nounphrase():
    select_sql = 'SELECT candidate_aspect FROM thesis.candidate_aspect'
    cursor.execute(select_sql)
    return [x[0] for x in cursor.fetchall()]

def insert_single_candidate_aspect_per_row(candidate_aspects):
    trucate_table('candidate_aspect')
    for review_id, sent_id, can_asp in candidate_aspects:
        if can_asp:
            for cand_asp in can_asp:
                insert_value = (review_id, sent_id, cand_asp)
                insert_query = ("INSERT INTO candidate_aspect "
                                "(review_id, sentence_id, candidate_aspect)"
                                "VALUES (%s, %s, %s)")
                cursor.execute(insert_query, insert_value)
    connection.commit()

# def insert_single_noun_chunk_per_row(candidate_aspects):
#     trucate_table('noun_chunks_per_row')
#     for review_id, sent_id, can_asp in candidate_aspects:
#         if can_asp:
#             for cand_asp in can_asp:
#                 insert_value = (review_id, sent_id, cand_asp)
#                 insert_query = ("INSERT INTO noun_chunks_per_row "
#                                 "(review_id, sentence_id, noun)"
#                                 "VALUES (%s, %s, %s)")
#                 cursor.execute(insert_query, insert_value)
#     connection.commit()

def fetch_candidate_aspects():
    select_sql = 'SELECT * from candidate_aspect'
    cursor.execute(select_sql)
    return cursor.fetchall()

def fetch_candidate_aspects_with_sentence_count():
    select_sql = 'SELECT count(*) as times, candidate_aspect FROM thesis.candidate_aspect group by candidate_aspect order by times desc;'
    cursor.execute(select_sql)
    return cursor.fetchall()

def insert_frequent_1_itemsets(frequent_1_itemset):
    trucate_table('frequent_itemsets')
    for key, value in frequent_1_itemset.items():
        insert_query = ("INSERT INTO frequent_itemsets "
                        "(frequent_itemsets)"
                        "VALUES (%s)")
        cursor.execute(insert_query, key)
    connection.commit()

def insert_frequent_k_itemsets(frequent_itemset):
    trucate_table('frequent_itemsets_k')
    for L in frequent_itemset:
        for key, value in frequent_itemset[L].items():
            fq_item = str(key).strip('')
            freq_item = eval(fq_item)
            insert_value = ' '.join(freq_item)
            insert_query = ("INSERT INTO frequent_itemsets_k "
                            "(frequent_itemsets)"
                            "VALUES (%s)")
            cursor.execute(insert_query, insert_value)
    connection.commit()

def fetch_frequent_itemsets():
    select_sql = 'SELECT frequent_itemsets FROM thesis.frequent_itemsets;'
    cursor.execute(select_sql)
    return [x[0] for x in cursor.fetchall()]

def fetch_frequent_k_itemsets():
    select_sql = 'SELECT frequent_itemsets FROM thesis.frequent_itemsets_k;'
    cursor.execute(select_sql)
    return [x[0] for x in cursor.fetchall()]

def insert_final_candidate_aspects(frequent_itemset):
    trucate_table('candidate_aspects_final')
    for cand_item in frequent_itemset:
        insert_query = ("INSERT INTO candidate_aspects_final "
                        "(aspect)"
                        "VALUES (%s)")
        cursor.execute(insert_query, cand_item)
    connection.commit()

def fetch_final_candidate_aspects():
    select_sql = 'SELECT aspect FROM thesis.candidate_aspects_final;'
    cursor.execute(select_sql)
    return [x[0] for x in cursor.fetchall()]

def insert_features_after_compactness_pruning(features_set):
    trucate_table('pruning')
    for feature in features_set:
        insert_query = ("INSERT INTO pruning "
                        "(candidate_features)"
                        "VALUES (%s)")
        cursor.execute(insert_query, feature)
    connection.commit()

def fetch_freatures_after_compactness_pruning():
    select_sql = 'SELECT candidate_features FROM thesis.pruning;'
    cursor.execute(select_sql)
    return [x[0] for x in cursor.fetchall()]

def fetch_feature_for_wikipedia_crawl():
    select_sql = 'SELECT count(*) as ct, nouns FROM thesis.nouns_list_per_sentence group by nouns order by ct desc;'
    cursor.execute(select_sql)
    entity = cursor.fetchone()
    return entity[1]

def insert_unigrams_into_db(review_id, sent_id, unigram_list):
    for unigram in unigram_list:
        insert_value = (review_id, sent_id, unigram)
        insert_query = ("INSERT INTO unigram "
                        "(review_id, sentence_id, unigram)"
                        "VALUES (%s, %s, %s)")
        cursor.execute(insert_query, insert_value)
    connection.commit()

def fetch_unigrams():
    select_sql = 'SELECT count(*) as times, unigram FROM thesis.unigram  group by unigram order by times desc;'
    cursor.execute(select_sql)
    return cursor.fetchall()

def fetch_bigrams():
    select_sql = 'SELECT count(*) as times, bigrams FROM thesis.bigrams group by bigrams order by times desc;'
    cursor.execute(select_sql)
    return cursor.fetchall()

def insert_bigrams_into_db(review_id, sent_id, bigrams_list):
    for bigrams in bigrams_list:
        convert_bigrams_into_string = str(bigrams).strip('[]')
        insert_value = (review_id, sent_id, convert_bigrams_into_string)
        insert_query = ("INSERT INTO bigrams "
                        "(review_id, sentence_id, bigrams)"
                        "VALUES (%s, %s, %s)")
        cursor.execute(insert_query, insert_value)
    connection.commit()

def insert_trigrams_into_db(review_id, sent_id, trigrams_list):
    for trigrams in trigrams_list:
        convert_trigrams_into_string = str(trigrams).strip('[]')
        insert_value = (review_id, sent_id, convert_trigrams_into_string)
        insert_query = ("INSERT INTO trigrams "
                        "(review_id, sentence_id, trigrams)"
                        "VALUES (%s, %s, %s)")
        cursor.execute(insert_query, insert_value)
    connection.commit()

def insert_quadgrams_into_db(review_id, sent_id, quadgrams_list):
    for quadgrams in quadgrams_list:
        convert_quadgrams_into_string = str(quadgrams).strip('[]')
        insert_value = (review_id, sent_id, convert_quadgrams_into_string)
        insert_query = ("INSERT INTO quadgrams "
                        "(review_id, sentence_id, quadgrams)"
                        "VALUES (%s, %s, %s)")
        cursor.execute(insert_query, insert_value)
    connection.commit()

def insert_pentagrams_into_db(review_id, sent_id, pentagrams_list):
    for pentagrams in pentagrams_list:
        convert_pentagrams_into_string = str(pentagrams).strip('[]')
        insert_value = (review_id, sent_id, convert_pentagrams_into_string)
        insert_query = ("INSERT INTO pentagrams "
                        "(review_id, sentence_id, pentagrams)"
                        "VALUES (%s, %s, %s)")
        cursor.execute(insert_query, insert_value)
    connection.commit()

def trucate_table(table_name):
    truncate_table_sql = 'TRUNCATE TABLE '+ table_name
    cursor.execute(truncate_table_sql)
    connection.commit()

# Redundancy Pruning
def presence_of_aspect_in_sentence(candidate_aspect):
    sql_query = "SELECT distinct count(sentence_id) FROM thesis.candidate_aspect where candidate_aspect like '%" + candidate_aspect + "%';"
    cursor.execute(sql_query)
    total_number_of_sent =cursor.fetchone()
    return total_number_of_sent[0]

def fetch_superset_with_sentence_count(aspect):
    cursor.callproc('superset_with_sentence_count', (aspect,))
    return [x[0] for x in cursor.fetchall()]

def get_sentence_ids_for_term(t):
    sql_query = "SELECT sentence_id FROM thesis.candidate_aspect where candidate_aspect = '" + t + "';"
    cursor.execute(sql_query)
    return [x[0] for x in cursor.fetchall()]

def calcualte_psupport_for_term_with_superset(ids, term):
    if len(ids)> 1:
        ids_set = str(ids)
    else:
        ids_set = str("(" + ids[0] + ")")
    sql_query = "SELECT count(*) FROM thesis.candidate_aspect where sentence_id not in " + ids_set + " and candidate_aspect = '" + term + "';"
    cursor.execute(sql_query)
    return cursor.fetchone()

# def calcualte_psupport_for_term(term):
#     sql_query = "SELECT count(*) FROM thesis.nouns_per_sentence where nouns = '" + term + "';"
#     cursor.execute(sql_query)
#     return [x[0] for x in cursor.fetchall()]

# def test():
#     candidate_aspect = fetch_candidate_aspect_db()
#     ca_list = []
#     for id, review_id, sent_id, ca in candidate_aspect:
#         ca_list.append(ca.split(','))
#
#         results = list(apriori(ca_list))
#         print(results)
# test()
# cursor.close()
# connection.close()


def fetch_sentnece_by_id(sent_id):
    sql_query = "SELECT sentence FROM thesis.sentences WHERE sentences_id = " + sent_id + ";"
    cursor.execute(sql_query)
    return cursor.fetchall()