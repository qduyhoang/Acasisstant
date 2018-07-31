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

if __name__ == '__main__':
    sNLP = StanfordNLP()

    with open('wiki_01', 'r') as inputfile:
        reader = csv.DictReader(inputfile)
        with open('outputfile.txt', 'w') as outputfile:
            fieldnames = ['words', 'lemmas', 'pos', 'ner', 'category']      
            writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
            writer.writeheader()
            for revision in reader:
                text =  revision['text']
                sentences = sNLP.annotate(text)
                category = revision['category']
                words, lemmas, pos, ner = [], [], [], []
                #Start annotating text
                sentences = sNLP.annotate(text)
                for sentence in sentences['sentences']:
                    tokens = sentence['tokens']
                    for token in tokens:
                        words.append(token['word'])
                        lemmas.append(token['lemma'])
                        pos.append(token['pos'])
                        ner.append(token['ner'])
                writer.writerow({
                    'words': words, 
                    'lemmas': lemmas, 
                    'pos': pos, 
                    'ner': ner,
                    'category': category})

    with open('outputfile.txt', 'r') as inputfile:
        reader = csv.DictReader(inputfile)
        for row in reader:
            print(row['words'])



