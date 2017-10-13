import pymysql, pre_processing

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
# cursor.close()
# connection.close()