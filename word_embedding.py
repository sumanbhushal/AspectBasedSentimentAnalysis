import gensim, database,pre_processing

sentence_list = database.fetch_sentence_from_sentence_table()
word_tokenize_review_list = pre_processing.word_tokenize_review(sentence_list)
corp = []
for sent_id, review_id, tok in word_tokenize_review_list:
    corp.append(tok)

print(corp)
model = gensim.models.Word2Vec(corp, min_count=3, size= 32)
# model.save('testmodel')

# model = gensim.models.Word2Vec.load('testmodel')
print(model.most_similar(['router']))
print(model['router'])