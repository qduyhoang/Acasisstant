
import re
from smart_open import smart_open
import json
from nltk.tokenize import sent_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from pprint import pprint
import os

from nltk import sent_tokenize


tfidf = TfidfVectorizer()


def findSimilarSentence(sentence, sentences):
	sentence = [sentence]
	sentence_tfidf = tfidf.fit(sentences).transform(sentence)
	sentences_tfidf = tfidf.fit_transform(sentences)

	cosine_similarities = linear_kernel(sentence_tfidf, sentences_tfidf).flatten()
	related_product_indices = cosine_similarities.argsort()
	result_index = list(related_product_indices).pop()
	return sentences[result_index]


def iter_files(path):
	"""Walk through all files located under a root path."""
	for dirpath, _, filenames in os.walk(path):
		for f in filenames:
			if f != '.DS_Store':
				yield os.path.join(dirpath, f)

def getSentencePairs(filepath):
	""" Tokenize each revision into sentences. Find pairs of sentences. """
	with smart_open(filepath, 'r') as f:
		revision = f.readline().strip()
		rev_num = 1
		while rev_num < 10:
			if rev_num == 1:
				pre_sentences = sent_tokenize(revision)
			else:
				post_sentences = sent_tokenize(revision)
				for orig_sent in pre_sentences:
					yield [orig_sent, findSimilarSentence(orig_sent, post_sentences)]
				pre_sentences = post_sentences
			revision = f.readline().strip()
			rev_num += 1



with smart_open('data/raw_sent_pair/in_sent/in', 'a') as orig_file, smart_open('data/raw_sent_pair/out_sent/out', 'a') as mod_file :
	for orig_sent, mod_sent in getSentencePairs('data/wiki_01'):
		orig_file.write(orig_sent+'\n')
		mod_file.write(mod_sent+'\n')

