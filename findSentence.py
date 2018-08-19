
import re
from smart_open import smart_open
import json
from nltk.tokenize import sent_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel



tfidf = TfidfVectorizer()


def expand(text, position):
	stop = ['.']
	left = position
	right = position + 1
	left_word = []
	right_word = []
	PROCESSED_WORDS = []
	while left >= 0 and text[left] not in stop:
		left_word.append(text[left])
		PROCESSED_WORDS.append(left)
		left -= 1
	while right < len(text) and text[right] not in stop:
		right_word.append(text[right])
		PROCESSED_WORDS.append(right)
		right +=1
	sentence = left_word[::-1]
	sentence.extend(right_word)
	return sentence, PROCESSED_WORDS


def findSentence(first_revision, second_revision, deleted, added):
	pairs = []
	deleted_sents = []
	added_sents = []
	sentence_removed = True

	for position in deleted:
		sentence, PROCESSED_WORDS = expand(first_revision, position)
		if position not in PROCESSED_WORDS:
			for index in PROCESSED_WORDS:
				if index not in deleted:
					sentence_removed = False
			if not sentence_removed:
				deleted_sents.append(sentence)
	for position in added:
		for deletion in deleted:
			print('pos', position)
			print('del', deletion)
			if position > deletion:
				position -= 1

		sentence, PROCESSED_WORDS = expand(second_revision, position)
		if position not in PROCESSED_WORDS:
			for index in PROCESSED_WORDS:
				if index not in deleted:
					sentence_added = False
			if not sentence_added:
				added_sents.append(sentence)
	yield deleted_sents, added_sents



def findSimilarity(sentence, sentences):
	sentence = [sentence]
	sentence_tfidf = tfidf.fit(sentences).transform(sentence)
	sentences_tfidf = tfidf.fit_transform(sentences)

	cosine_similarities = linear_kernel(sentence_tfidf, sentences_tfidf).flatten()
	related_product_indices = cosine_similarities.argsort()
	result_index = list(related_product_indices).pop()
	return sentences[result_index]

with smart_open('data/processed/processed_outputfile') as file, smart_open('data/processed/processed_outputfile_new', 'w') as outputfile:
	for num, line in enumerate(file):
		added = []
		if num == 0:
			first_document = json.loads(line)
		else:
			deleted = first_document['deleted']
			second_document = json.loads(line)

			first_doc_sentences = sent_tokenize(' '.join(first_document['original']))
			second_doc_sentences = sent_tokenize(' '.join(second_document['original']))

			for index_content_tuple in first_document['added']:
				added.append(index_content_tuple[0])

			for deleted_sents, added_sents in findSentence(first_document['original'], second_document['original'], deleted, added):
				if len(deleted_sents):
					for sentence in deleted_sents:
						input_sent = ' '.join(sentence)
						output_sent = findSimilarity(input_sent, second_doc_sentences)
						data = {'input': input_sent,
								'output': output_sent}
						outputfile.write(json.dumps(data))
						outputfile.write('\n')
				if len(added_sents):
					for sentence in added_sents:
						input_sent = ' '.join(sentence)
						output_sent = findSimilarity(input_sent, first_doc_sentences)
						data = {'input': input_sent,
								'output': output_sent}
						outputfile.write(json.dumps(data))
						outputfile.write('\n')
				
			first_document = second_document

