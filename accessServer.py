from pycorenlp.corenlp import StanfordCoreNLP
import logging
import json
from collections import defaultdict
import csv

class StanfordNLP:
    def __init__(self, host='http://localhost', port='9000'):
        self.nlp = StanfordCoreNLP(host+ ':' + port)  # , quiet=False, logging_level=logging.DEBUG)
        self.props = {
            'annotators': 'tokenize,pos,lemma,ner',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)

    def ner(self, sentence):
        return self.nlp.ner(sentence)

    def annotate(self, sentence):
        return self.nlp.annotate(sentence, properties=self.props)





