import re
from smart_open import smart_open
import json
from nltk.tokenize import sent_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from utils import iter_files
import os

from nltk import sent_tokenize

from diff_match_patch import diff_match_patch, patch_obj


class SentencePairer:
	"""
	file_path: path of the directory containing revisions
	"""
	def __init__(self, file_path):
		self.filepath = file_path
		self.tfidf = TfidfVectorizer()
		self.diff = diff_match_patch()


	def findSimilarSentence(self, sentence, sentences):
		sentence = [sentence]
		sentence_tfidf = self.tfidf.fit(sentences).transform(sentence)
		sentences_tfidf = self.tfidf.fit_transform(sentences)

		cosine_similarities = linear_kernel(sentence_tfidf, sentences_tfidf).flatten()
		related_product_indices = cosine_similarities.argsort()
		result_index = list(related_product_indices).pop()
		return sentences[result_index]




	def getSentencePairs(self):
		""" Tokenize each revision into sentences. Find pairs of sentences. """
		with smart_open(self.filepath, 'r') as f:
			revision = f.readline().strip()
			rev_num = 1
			while revision:
				if rev_num == 1:
					input_sentences = sent_tokenize(revision)
				else:
					target_sentences = sent_tokenize(revision)
					for input_sent in input_sentences:
						yield [input_sent, self.findSimilarSentence(input_sent, target_sentences)]
					input_sentences = target_sentences
				revision = f.readline().strip()
				rev_num += 1


	def classifyPairs(self):
		label = ""
		for input_sent, target_sent in self.getSentencePairs():
			ignore = False
			diffs = self.diff.diff_main(input_sent, target_sent)
			edit_distance = self.diff.diff_levenshtein(diffs)
			if edit_distance == 0 or edit_distance > 100:
				ignore = True
			elif edit_distance <= 4:
				label = "fluency"
			elif edit_distance > 4: # edit_distance > 100 || edit_distance = 0 => ignore
				label = "factual"
			if not ignore:
				yield [label, input_sent, target_sent]

				


	def savePairsToDir(self, directory):
		if not os.path.exists(directory+"/fluency"):
			os.makedirs(directory+"/fluency")
		if not os.path.exists(directory+"/factual"):
			os.makedirs(directory+"/factual")

		fluency_file_num = 0
		factual_file_num = 0 
		fluency_line_ctr = 0
		factual_line_ctr = 0

		fluency_f = open("%s/fluency/pairs_%d" %(directory, fluency_file_num), "a")
		factual_f = open("%s/factual/pairs_%d" %(directory, factual_file_num), "a")

		for label, input_sent, target_sent in self.classifyPairs():
			content = input_sent + "\t" + target_sent + "\n"
			if label == "fluency":
				print(content)
				fluency_f.write(content)
				fluency_line_ctr += 1
			elif label == "factual":
				factual_f.write(content)
				factual_line_ctr += 1

			if (fluency_line_ctr % 100 == 0):  #Write to a new file after every 100 line
				fluency_f.close()
				fluency_file_num += 1
				fluency_f = open("%s/fluency/pairs_%d" %(directory, fluency_file_num), "a")
			elif (factual_line_ctr % 100 == 0):
				factual_f.close()
				factual_file_num += 1
				factual_f = open("%s/factual/pairs_%d" %(directory, factual_file_num), "a")

		fluency_f.close()
		factual_f.close()

if __name__ == "__main__":
	pairer = SentencePairer("data/wiki_01")
	pairer.savePairsToDir("data/raw_sent_pair")

				




	