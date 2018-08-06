import nltk
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
import gensim
from gensim.models.doc2vec import TaggedDocument
from collections import namedtuple
from smart_open import smart_open
import json
import logging
import os
from random import shuffle
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
SentimentDocument = namedtuple('SentimentDocument', 'word categories')

file_directory = 'data/unprocessed'

nltk.download('stopwords')
tokenizer = RegexpTokenizer(r"\w+")
stopword_set = set(stopwords.words("english"))


class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list

    def __iter__(self):
        for idx, file_name in enumerate(self.doc_list):
        	with smart_open(os.path.join(file_directory, file_name)) as file:
        		for revision_num, doc in enumerate(file):
        			doc = nlp_clean(json.loads(doc)['text'])
        			yield gensim.models.doc2vec.LabeledSentence(doc,    
						[self.labels_list[idx] + '_%s' % revision_num]) 

    def to_array(self):
    	self.documents = []
    	for idx, file_name in enumerate(self.doc_list):
    		with smart_open(os.path.join(file_directory, file_name)) as file:
    			for revision_num, doc in enumerate(file):
    				doc = nlp_clean(json.loads(doc)['text'])
    				self.documents.append(gensim.models.doc2vec.LabeledSentence(doc, [self.labels_list[idx] + '_%s' % revision_num]))
    	return self.documents

    def sentences_perm(self):
        shuffle(self.documents)
        return self.documents


def nlp_clean(data):
	new_data = tokenizer.tokenize(data.lower())
	new_data = list(set(new_data).difference(stopword_set))
	return new_data


doc_list = ['input']
label_list = ['first_doc']
if not os.path.isfile('./myfirstmodel.d2v'):
	sentences = LabeledLineSentence(doc_list, label_list)
	model = gensim.models.Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=8)
	model.build_vocab(sentences.to_array())
	for epoch in range(10):
		model.train(sentences.sentences_perm(), total_examples=model.corpus_count, epochs = model.epochs)
		model.save('./myfirstmodel.d2v')
else:
	model = gensim.models.Doc2Vec.load('./myfirstmodel.d2v')
	tokens = "natural language processing is super cool".split()
	new_vector = model.infer_vector(tokens)
	sims = model.docvecs.most_similar([new_vector])
	print(model['first_doc_353'])

# with smart_open('data/unprocessed/input', 'rb', encoding='utf-8') as alldata:
# 	for line_no, line in enumerate(alldata):
# 		if line_no == 353:
# 			line = json.loads(line)
# 			tokens = gensim.utils.to_unicode(line['text'])
# 			print(nlp_clean(tokens))

