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

# insert_into_review_table('kkkkdfkadfkdsfjdf')


def get_sentence_from_review():
    sql = 'SELECT * from review'
    cursor.execute(sql)
    reviews = cursor.fetchall()
    for id, review in reviews:
        for rw in review.split("\n"):
            if rw != '':
                insert_sentence_into_sentence_table(id, rw)

    select_sql = 'SELECT * from sentences'
    print(cursor.execute(select_sql))

def insert_sentence_into_sentence_table(review_id, sentence):
    insert_value = (review_id, sentence)
    insert_query = ("INSERT INTO sentences "
                    "(review_id, sentence)"
                    "VALUES (%s, %s)")
    cursor.execute(insert_query, insert_value)
    connection.commit()


get_sentence_from_review()
# cursor.close()
# connection.close()