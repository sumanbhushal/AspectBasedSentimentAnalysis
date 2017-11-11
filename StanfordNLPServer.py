from stanfordcorenlp import StanfordCoreNLP
import json


class SNLPServer:
    def __init__(self):
        self.nlp = StanfordCoreNLP('http://localhost', port=9000, timeout=2000)

        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)

    def ner(self, sentence):
        return self.nlp.ner(sentence)

    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))

if __name__ == '__main__':
    nlpServer = SNLPServer()
    text = 'I purchased this cameras just over a year ago and I am in love with it. I was just starting out with ' \
           'photography, and this camera made it very easy and less confusing. The D5000 has a much better screen and ' \
           'in my opinion has a bette design.'
    print("Annotate:", nlpServer.annotate(text))
    print ("POS:", nlpServer.pos(text))
    print( "Tokens:", nlpServer.word_tokenize(text))
    print( "NER:", nlpServer.ner(text))
    print( "Parse:", nlpServer.parse(text))
    print ("Dep Parse:", nlpServer.dependency_parse(text))

    # C:\Users\Suman Bhushal\Google Drive\RUC Materials\4th Semester_\Thesis\Python\AspectExtraction\stanford-corenlp-full-2017-06-09
    # java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000