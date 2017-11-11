import gensim, database,pre_processing, config

sentence_list = database.fetch_sentence_from_sentence_table()
word_tokenize_review_list = pre_processing.word_tokenize_review(sentence_list)
corp = []
for sent_id, review_id, tok in word_tokenize_review_list:
    corp.append(tok)

print(corp)
# file = open(config.currentWorkingDirectory+ "\\glove.6B.50d.txt", "r").read()
model = gensim.models.Word2Vec(corp, min_count=3, size= 32)
# model.save('testmodel')

# model = gensim.models.Word2Vec.load('glove.6B.50d.txt')
print(model.most_similar(['router']))
# print(model['router'])