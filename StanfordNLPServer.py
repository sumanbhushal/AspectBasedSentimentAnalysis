from stanfordcorenlp import StanfordCoreNLP
import json


class SNLPServer:
    def __init__(self):
        self.nlp = StanfordCoreNLP('http://localhost', port=9000, timeout=2000)

        self.props = {
            'annotators': 'pos',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)
    # C:\Users\Suman Bhushal\Google Drive\RUC Materials\4th Semester_\Thesis\Python\AspectExtraction\stanford-corenlp-full-2017-06-09
    # java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
