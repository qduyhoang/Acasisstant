
import re
from smart_open import smart_open
import json
from nltk.tokenize import sent_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from pprint import pprint

tfidf = TfidfVectorizer()


def expand(tokenized_sents, position):
	doc_len = 0
	for sent in tokenized_sents:
		doc_len += len(sent)

	if position == doc_len:
		sentence = tokenized_sents[-1]
		sent_index = len(tokenized_sents) - 1
		all_word_index = [i for i in range(doc_len - len(sentence.split()), doc_len)]
		return (sentence, all_word_index, sent_index)

	cur_pos = 0
	for sent_num, sentence in enumerate(tokenized_sents):
		begin = cur_pos
		words = sentence
		for word in words:
			if cur_pos == position:
				sent_index = sent_num
				all_word_index = [i for i in range(begin, begin + len(words))]
				return (sentence, all_word_index, sent_index)
			else:
				cur_pos += 1


def findSentence(first_revision, second_revision, deleted, added):
	pairs = []
	PROCESSED_ORIGINAL_ADDED = []
	PROCESSED_DELETED = []
	PROCESSED_ADDED = []
	PROCESSED_OVERLAPPED = []


	# for order, position in enumerate(deleted):
	# 	if position not in PROCESSED_DELETED:
	# 		result = expand(first_revision, position)
	# 		sentence_deleted = True
	# 		sentence, processed, _ = result
	# 		for index in processed:
	# 			if index not in deleted:
	# 				sentence_deleted = False
	# 		PROCESSED_DELETED.extend(processed)
	# 		#Check if the whole sentence is deleted
	# 		if not sentence_deleted:
	# 			revised_pos = position - order
	# 			for insertion in added:
	# 				if revised_pos > insertion:
	# 					revised_pos += 1
	# 			input_sent = sentence
	# 			result = expand(second_revision, revised_pos)
	# 			if (input_sent and result):
	# 				output_sent, _, _ = result
	# 				yield((input_sent, output_sent))


	# for order, position in enumerate(added):
	# 	if position not in PROCESSED_ADDED:
	# 		sentence_added = True
	# 		result = expand(second_revision, position)
	# 		sentence, processed, sent_index = result
	# 		for index in processed:
	# 			if index not in added:
	# 				sentence_added = False
	# 		PROCESSED_ADDED.extend(processed)
	# 		if not sentence_added:
	# 			revised_pos = position - order
	# 			for deletion in deleted:
	# 				if position > deletion:
	# 					revised_pos += 1
	# 			output_sent = sentence
	# 			result = expand(first_revision, revised_pos)
	# 			if (output_sent and result):
	# 				input_sent, _, _ = result
	# 				yield((input_sent, output_sent))

	for position in deleted:
		if position not in PROCESSED_DELETED:
			result = expand(first_revision, position)
			sentence_deleted = True
			sentence, processed, _ = result
			for index in processed:
				if index not in deleted:
					sentence_deleted = False
			PROCESSED_DELETED.extend(processed)
			#Check if the whole sentence is deleted
			if not sentence_deleted:
				yield(('deleted', sentence))

	for position in added:
		if position not in PROCESSED_ADDED:
			result = expand(second_revision, position)
			sentence_added= True
			sentence, processed, _ = result
			for index in processed:
				if index not in added:
					sentence_added = False
			PROCESSED_ADDED.extend(processed)
			#Check if the whole sentence is deleted
			if not sentence_added:
				yield(('added', sentence))




def findSimilarity(sentence, sentences):
	sentence = [sentence]
	sentence_tfidf = tfidf.fit(sentences).transform(sentence)
	sentences_tfidf = tfidf.fit_transform(sentences)

	cosine_similarities = linear_kernel(sentence_tfidf, sentences_tfidf).flatten()
	related_product_indices = cosine_similarities.argsort()
	result_index = list(related_product_indices).pop()
	return sentences[result_index]

with smart_open('data/processed/input', 'a') as outputfile:
	for line in smart_open('data/processed/processed_outputfile'):
		added_index = []
		first_doc_dict = json.loads(line)

		deleted = first_doc_dict['deleted']
		added = first_doc_dict['added']

		first_doc_words = first_doc_dict['original']
		second_doc_words = first_doc_dict['original'][::]


		for pos in deleted[::-1]:
			second_doc_words.pop(pos)
		for pos, content in added:
			second_doc_words.insert(pos, content)
			added_index.append(pos)


		first_doc_sentences = sent_tokenize(" ".join(first_doc_words))
		second_doc_sentences = sent_tokenize(" ".join(second_doc_words))


		for result in findSentence(first_doc_sentences, second_doc_sentences, deleted, added_index):
			# if result is not None:
			# 	input_sent = result[0]
			# 	output_sent = result[1]
			# 	if input_sent != output_sent:
			# 	outputfile.write('input. '+input_sent.text)
			# 	outputfile.write('\n')
			# 	outputfile.write('output. '+output_sent.text)
			# 	outputfile.write('\n')
			label = result[0]
			if label == 'deleted':
				input_sent = result[1]
				output_sent = findSimilarity(input_sent, second_doc_sentences)
			elif label == 'added':
				output_sent = result[1]
				input_sent = findSimilarity(output_sent, first_doc_sentences)
			if input_sent != output_sent:
				outputfile.write('Input '+input_sent)
				outputfile.write('\n')
				outputfile.write('Output ' +output_sent)
				outputfile.write('\n')

			

