import pymysql, pre_processing

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Nepal12',
        db='thesis')

    cursor = connection.cursor()
except pymysql.connections.Error as err:
    print(err)


def insert_into_review_table(review):
    """
    :param review: reviews to insert into database
    """
    insert_query = ("INSERT INTO review "
                    "(review)"
                    "VALUES (%s)")
    cursor.execute(insert_query, review)
    connection.commit()


def insert_domain_data_into_review_table(review):
    """
    Insert reviews without manual annotation
    :param review: List of reviews
    """
    truncate_sentence_table_sql = 'TRUNCATE TABLE review'
    cursor.execute(truncate_sentence_table_sql)
    for review_sent in review:
        insert_query = ("INSERT INTO review "
                        "(review)"
                        "VALUES (%s)")
        cursor.execute(insert_query, review_sent)
    connection.commit()


def insert_sentence_into_sentence_table():
    """
    Get reviews from review table and split sentences and insert into database after lemmatization
    """
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
    """
    :param review: collection of reviews from file
    :return: list of sentence
    """
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
    """
    Fetch all the sentence form database
    :return: List of all the sentence from database
    """
    select_sql = 'SELECT * from sentences'
    cursor.execute(select_sql)
    return cursor.fetchall()


def insert_postagged_sent_into_db(pos_tagged_sentences):
    """
    Inserting Stanford POS tagged Sentence into database
    :param pos_tagged_sentences: POS tagged sentence list
    """
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


def fetach_pos_tagged_sentence():
    """
    Fetch POS tagged sentence list
    :return: List of POS tagged sentence list
    """
    select_sql_query = 'SELECT * From pos_tagged_sentences'
    cursor.execute(select_sql_query)
    # row = cursor.fetchall()
    pos_tagged_review = list(cursor)
    return pos_tagged_review


def insert_nouns_list_per_sentence_into_db(nouns_per_sent):
    """
    Insert nouns list per sentence into database
    :param nouns_per_sent: List of nouns per sentence
    """
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
    """
    Fetch nouns per sentence
    :return: List of nouns per sentence
    """
    select_sql = 'SELECT * from nouns_list_per_sentence'
    cursor.execute(select_sql)
    return cursor.fetchall()


def insert_single_candidate_aspect_per_row(candidate_aspects):
    """
    Insert each candidate aspect (noun) in each rows
    :param candidate_aspects: List of candidate aspects
    """
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


def fetch_noun_nounphrase():
    """
    Fetch nouns and noun phrases (candidate aspects)
    :return: List of nouns and noun phrases
    """
    select_sql = 'SELECT candidate_aspect FROM thesis.candidate_aspect'
    cursor.execute(select_sql)
    return [x[0] for x in cursor.fetchall()]


def fetch_candidate_aspects():
    """
    Fetch candidate aspects
    :return: List of all candidate aspects
    """
    select_sql = 'SELECT * from candidate_aspect'
    cursor.execute(select_sql)
    return cursor.fetchall()


def fetch_candidate_aspects_with_sentence_count():
    """
    Fetch candidate aspects and number of occurrence in  review sentences
    :return: List of candidate aspect and respect occurrence count
    """
    select_sql = 'SELECT count(*) as times, candidate_aspect FROM thesis.candidate_aspect group by candidate_aspect order by times desc;'
    cursor.execute(select_sql)
    return cursor.fetchall()


def insert_frequent_1_itemsets(frequent_1_itemset):
    """
    Insert frequent-1- itemset from Apriori algorithm
    :param frequent_1_itemset: List of frequent-1-itemset
    """
    trucate_table('frequent_itemsets')
    for key, value in frequent_1_itemset.items():
        insert_query = ("INSERT INTO frequent_itemsets "
                        "(frequent_itemsets)"
                        "VALUES (%s)")
        cursor.execute(insert_query, key)
    connection.commit()


def insert_frequent_k_itemsets(frequent_itemset):
    """
    Insert frequent-k-itemsets from Apriori algorithm
    :param frequent_itemset: List of frequent-k-itemsets
    """
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
    """
    Fetch frequent-1-itemsets from database
    :return: List of frequent-1-itemsets
    """
    select_sql = 'SELECT frequent_itemsets FROM thesis.frequent_itemsets;'
    cursor.execute(select_sql)
    return [x[0] for x in cursor.fetchall()]


def fetch_frequent_k_itemsets():
    """
    Fetch frequent-k-itemsets
    :return: List of frequent-k-itemsets
    """
    select_sql = 'SELECT frequent_itemsets FROM thesis.frequent_itemsets_k;'
    cursor.execute(select_sql)
    return [x[0] for x in cursor.fetchall()]


def insert_final_candidate_aspects(frequent_itemset):
    """
    Insert final frequent itemset into database after Apriori algoirthm
    :param frequent_itemset: final frequent itemset
    :return:
    """
    trucate_table('candidate_aspects_final')
    for cand_item in frequent_itemset:
        insert_query = ("INSERT INTO candidate_aspects_final "
                        "(aspect)"
                        "VALUES (%s)")
        cursor.execute(insert_query, cand_item)
    connection.commit()


def fetch_final_candidate_aspects():
    """
    Fetch final frequent itemsets from database
    :return: List of final frequent itemsets
    """
    select_sql = 'SELECT aspect FROM thesis.candidate_aspects_final;'
    cursor.execute(select_sql)
    return [x[0] for x in cursor.fetchall()]


def insert_features_after_compactness_pruning(features_set):
    """
    Insert candidate aspects after compactness pruning into database
    :param features_set: List of candidate aspects after compactness pruning
    """
    trucate_table('pruning')
    for feature in features_set:
        insert_query = ("INSERT INTO pruning "
                        "(candidate_features)"
                        "VALUES (%s)")
        cursor.execute(insert_query, feature)
    connection.commit()


def fetch_freatures_after_compactness_pruning():
    """
    Fetch candidate aspects after compactness pruning
    :return: List of candidate aspects
    """
    select_sql = 'SELECT candidate_features FROM thesis.pruning;'
    cursor.execute(select_sql)
    return [x[0] for x in cursor.fetchall()]


def fetch_feature_for_wikipedia_crawl():
    """
    Fetch the Entity form database (i.e. aspect with the maximum count)
    :return: Entity
    """
    select_sql = 'SELECT count(*) as ct, candidate_aspect FROM thesis.candidate_aspect group by candidate_aspect ' \
                 'order by ct desc;'
    cursor.execute(select_sql)
    entity = cursor.fetchone()
    return entity[1]


def trucate_table(table_name):
    """
    Truncate table from database based on provided name
    :param table_name: Name of the table to be truncate
    """
    truncate_table_sql = 'TRUNCATE TABLE ' + table_name
    cursor.execute(truncate_table_sql)
    connection.commit()


def presence_of_aspect_in_sentence(candidate_aspect):
    """
    Check if the aspect is present in the sentence, if yes count sentence and return total number of sentence
    for p-support count
    :param candidate_aspect: candidate aspect
    :return: total number of sentence that contain aspect
    """
    sql_query = "SELECT distinct count(sentence_id) FROM thesis.candidate_aspect where candidate_aspect like '%" \
                + candidate_aspect + "%';"
    cursor.execute(sql_query)
    total_number_of_sent = cursor.fetchone()
    return total_number_of_sent[0]


def fetch_superset_with_sentence_count(aspect):
    """
    Call to database procedure to check if the superset of the aspect and
    return all the superset of the candidate aspects
    :param aspect: candidate aspect
    :return: list of superset of the candidate aspect
    """
    cursor.callproc('superset_with_sentence_count', (aspect,))
    return [x[0] for x in cursor.fetchall()]


def get_sentence_ids_for_term(t):
    """
    Return the sentence_ids that contain the aspect
    :param t: Name of candidate aspect
    :return: List of sentence ids that contain the aspect
    """
    sql_query = "SELECT sentence_id FROM thesis.candidate_aspect where candidate_aspect = '" + t + "';"
    cursor.execute(sql_query)
    return [x[0] for x in cursor.fetchall()]


def calcualte_psupport_for_term_with_out_superset(ids, term):
    """
    Calculate p-support for the each candidate aspect
    :param ids: Sentence Ids
    :param term: Candidate aspect
    :return: p-support value (Number of sentence that contains aspect but not superset of the aspect)
    """
    if len(ids) > 1:
        ids_set = str(ids)
    else:
        ids_set = str("(" + ids[0] + ")")
    sql_query = "SELECT count(*) FROM thesis.candidate_aspect where sentence_id not in " + ids_set + \
                " and candidate_aspect = '" + term + "';"
    cursor.execute(sql_query)
    return cursor.fetchone()


def fetch_sentnece_by_id(sent_id):
    """
    Fetch Sentece by its id
    :param sent_id: sentence id
    :return: sentence with the give id
    """
    sql_query = "SELECT sentence FROM thesis.sentences WHERE sentences_id = " + sent_id + ";"
    cursor.execute(sql_query)
    return [x[0] for x in cursor.fetchall()]


def insert_final_product_aspect_list(product_aspects_list_final):
    """
    Insert final aspect list into database
    :param product_aspects_list_final: product aspect list
    """
    trucate_table('product_aspects')
    for aspect in product_aspects_list_final:
        insert_query = ("INSERT INTO product_aspects "
                        "(aspect)"
                        "VALUES (%s)")
        cursor.execute(insert_query, aspect)
    connection.commit()


def fetch_final_product_aspect_list():
    """
    Fetch the product aspects
    :return: List of product aspects
    """
    select_sql = 'SELECT aspect FROM thesis.product_aspects;'
    cursor.execute(select_sql)
    return [x[0] for x in cursor.fetchall()]


def insert_sentiment_analysis_result(sentiment_analysis_result_insert_into_db):
    """
    Insert final sentiment anaysis result in the database
    :param sentiment_analysis_result_insert_into_db: Result of sentiment analysis
    """
    trucate_table('sentiment_analysis')
    for aspect in sentiment_analysis_result_insert_into_db:
        # print(str(aspect[4]).strip('[]'))
        insert_value = (aspect[0], aspect[1], aspect[2], aspect[3], str(aspect[4]).strip('[]'), str(aspect[5]).strip('[]'), str(aspect[6]).strip('[]'))
        insert_query = ("INSERT INTO sentiment_analysis "
                        "(product_aspect, pos_score, neg_score, neu_score, pos_sent_ids, neg_sent_ids, neu_sent_ids)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(insert_query, insert_value)
    connection.commit()


def insert_duration_time(execution_time):
    """
    Insert Execution time to generate opinion summary
    :param execution_time: Execution time
    """
    trucate_table('execution_time')
    insert_query = ("INSERT INTO execution_time "
                    "(duration)"
                    "VALUES (%s)")
    cursor.execute(insert_query, execution_time)
    connection.commit()