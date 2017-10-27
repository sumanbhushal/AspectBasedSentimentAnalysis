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
    sql = 'SELECT * from review'
    cursor.execute(sql)
    reviews = cursor.fetchall()
    truncate_sentence_table_sql = 'TRUNCATE TABLE sentences'
    cursor.execute(truncate_sentence_table_sql)
    for id, review in reviews:
        for rw in review.split("\n"):
            if rw != '':
                insert_sentence_query(id, rw)


def insert_sentence_query(review_id, sentence):
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
    select_sql = 'SELECT * from sentences'
    cursor.execute(select_sql)
    return cursor.fetchall()


def fetch_sentence_from_sentence_table():
    select_sql = 'SELECT * from sentences'
    cursor.execute(select_sql)
    return cursor.fetchall()

# Inserting POS tagged Sentence into database
def insert_postagged_sent_into_db(pos_tagged_sentences):
    for review_id, sent_id, sent in pos_tagged_sentences:
        convert_sent_into_string = str(sent).strip('[]')
        insert_value = (sent_id, review_id, convert_sent_into_string)
        insert_query = ("INSERT INTO pos_tagged_sentences "
                        "(sentence_id, review_id, pos_tagged_sentences)"
                        "VALUES (%s, %s, %s)")
        cursor.execute(insert_query, insert_value)
    connection.commit()

# Fetching POS tagged Sentence from Database
def fetach_pos_tagged_sentence():
    select_sql_query = 'SELECT * From pos_tagged_sentences'
    cursor.execute(select_sql_query)
    return cursor.fetchall()


def insert_candidate_aspect_into_db(candidate_aspects):
    for review_id, sent_id, can_asp in candidate_aspects:

        if can_asp:
            candidate_asp = ''
            for cand_asp in can_asp:
                if cand_asp != can_asp[-1]:
                    candidate_asp += cand_asp + ','
                else:
                    candidate_asp += cand_asp

            insert_value = (review_id, sent_id, candidate_asp)
            insert_query = ("INSERT INTO candidate_aspect_per_sentence "
                            "(review_id, sentence_id, candidate_aspects)"
                            "VALUES (%s, %s, %s)")
            cursor.execute(insert_query, insert_value)
    connection.commit()

def fetch_candidate_aspect_db():
    select_sql = 'SELECT * from candidate_aspect_per_sentence'
    cursor.execute(select_sql)
    return cursor.fetchall()


def insert_unigrams_into_db(review_id, sent_id, unigram_list):
    for unigram in unigram_list:
        convert_unigram_into_string = str(unigram).strip('[]')
        insert_value = (review_id, sent_id, convert_unigram_into_string)
        insert_query = ("INSERT INTO unigram "
                        "(review_id, sentence_id, unigram)"
                        "VALUES (%s, %s, %s)")
        cursor.execute(insert_query, insert_value)
    connection.commit()

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