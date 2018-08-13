import collections

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from smart_open import smart_open
import re
from pprint import pprint
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
class MyCorpus(object):
    def __iter__(self):
        #store number of sentences of each revision
        for line in smart_open('data/unprocessed/input', 'r'):
            #assume there's one document per line, tokens separated by whitespace]
            yield json.loads(line)['text']


def split_by_sentence(text):
    text = re.split('([\W])', text.lower())
    stop = ('...', '.', '?', '!', '!!!')
    seperator = (' ', '', "'", ',')
    sentence = []
    for word in text:
        if word in stop:
            yield ' '.join(sentence)
            sentence = []
        elif word not in seperator:
            sentence.append(word)
memory_friendly_corpus = MyCorpus()

dataset = []
for revision_num, cur_revision in enumerate(memory_friendly_corpus):
	if revision_num == 0:
		first_revision = cur_revision
	elif revision_num <= 2:
		second_revision = cur_revision
		for sentence in split_by_sentence(first_revision):
			dataset.append(sentence)
		for sentence in split_by_sentence(second_revision):
			dataset.append(sentence)
		first_revision = second_revision


""" Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
vectorizer = TfidfVectorizer(stop_words='english',
                             max_df=0.5,
                             min_df=0.1)
#number of clusters
num_cluster = 3
tfidf_model = vectorizer.fit_transform(dataset)
km_model = KMeans(n_clusters=num_cluster)
#fitting the input data
km_model.fit(tfidf_model)

clustering = collections.defaultdict(list)



for idx, document in enumerate(dataset):
    pprint(str(idx) + document)
for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)
 
pprint(dict(clustering))
