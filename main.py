import xml.etree.ElementTree as ET
import json
import re
import requests
import io
import gzip
import sys
import shutil
import os
import subprocess
from tqdm import tqdm
import math
from bs4 import BeautifulSoup
import exec_time
from collections import defaultdict
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
console = logging.StreamHandler()
console.setFormatter(fmt)
logger.addHandler(console)

def iter_files(path):
    """Walk through all files located under a root path."""
    if os.path.isfile(path):
        yield path
    elif os.path.isdir(path):
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                yield os.path.join(dirpath, f)
    else:
        raise RuntimeError('Path %s is invalid' % path)


def getTotalFileSize(file_path):
	sizecounter = 0
	for f in iter_files(file_path):
		sizecounter += os.path.getsize(f)
	return sizecounter

def retrieveData(file_name_pattern, file_path = 'data/compressed/', baseURL = "https://dumps.wikimedia.org/enwiki/latest/"):
	#Get html content and convert to string
	html_page = requests.get(baseURL).text
	result = file_name_pattern.findall(html_page)											 
	#Filter overlapping results												 
	file_names = set(result)
	for file_name in file_names:
		if file_name == 'enwiki-latest-abstract11.xml.gz':
			#Download gzip file
			response = requests.get(baseURL + file_name, stream = True)
			with gzip.open(file_path+file_name, 'wb') as compressed_file:
				# Total size in bytes.
				file_size = int(response.headers.get('content-length', 0));
				block_size = 1024
				#Write gzip response to a new file and show progress bar
				for data in tqdm(response.iter_content(block_size), total=math.ceil(file_size//block_size) , unit='KB', unit_scale=True):
					compressed_file.write(data)

def uncompressData(input_path = 'data/compressed/', output_path = 'data/unprocessed/'):
	# Preprocess the total files sizes
	sizecounter = getTotalFileSize(input_path)

	count = 0
	# Show progress using file size
	with tqdm(total = sizecounter, unit = 'B', unit_scale = True, unit_divisor = 1024) as progressBar:
		#Search compressed files
		for file in iter_files(input_path):
			if file.endswith('.gz'):
				out_file_name = file[:-3]
				with gzip.open(file, 'rb') as compressed_file:
					with open(out_file_name, 'wb') as uncompressed_file:
						buf = 1
						while buf:
							#Decompress file and save
							buf = gzip.decompress(compressed_file.read())
							uncompressed_file.write(buf)
						if buf:
							progressBar.set_postfix(file=filepath[-10:], refresh=False)
							progressBar.update(len(buf))
				#Delete comesseprd file after uncompressing
				os.remove(file)
				logger.info('%s uncompressed' %file)
				count += 1
		logger.info('%d files uncompressed' %count)


#Retrieve content from xml files
def processData(file_path = 'data/unprocessed/', remove_formatting = False):
	#global dictionary of documents + revision numbers vs categories
	category_files = defaultdict(dict)
	#Store all existing category file names 
	for cur_path, directories, files in os.walk('data/categories/'):
		for file_name in files:
			category_files[file_name] = 1
	#local dict to store all revisions of category of each document
	local_dict = defaultdict(dict)

	#regex to get all content inside category tags
	category_content_pattern = re.compile('\[\[Category:(.*?)\]\]')
	#Search uncompressed files
	for cur_path, _, files in os.walk(file_path):
		for file_name in files:
			logger.info('Processing %s' %file_name)
			tree = ET.parse(cur_path+file_name)
			#Get root tag <page>
			root = tree.getroot()[1]
			file_start = '{http://www.mediawiki.org/xml/export-0.10/}'

			#Get text content and revision number
			revision_count = 1
			data = {}
			for revision in root.iter(file_start+'revision'):
				text = revision.find(file_start+'text').text
				if text != None:
					#category of each revision
					categories = category_content_pattern.findall(text)
					if len(categories):  #if there is any categories
						for cat in categories:  #for each category
							if cat not in local_dict:  #if category hasn't existed
							# 	local_dict[cat] = []	#create an array to store revision numbers
							# else:						#uncomment this to have array of all revision numbers
							# 	local_dict[cat].append(i)
								local_dict[cat] = revision_count

					if remove_formatting:	
						text, refs = stripFormatting(text)
					data[i] = tokenization(text), categories, refs
				revision_count += 1

			for category, revision_number in local_dict.items():
				if category in category_files:  #if a category file has existed
					with open('data/categories/'+category+".txt", "a") as category_file:  #append to the file
						#store document's name and revision number
						category_file.write(file_name + ' ' + str(revision_number) + '\n')
						# for num in revision_number:	#uncomment this to have array of all revision numbers
						# 	category_file.write(' '+ str(num))
				else:
					with open('data/categories/'+category+".txt", "w") as category_file:  #create a new file
						category_file.write(file_name + ' ' + str(revision_number) + '\n')
						# for num in revision_number:
						# 	category_file.write(' '+ str(num))

				#Write a new file with filtered data as json format
				json_file_name = file_name[:-3] + 'json'
				with open(file_path+json_file_name, 'w') as data_file:
					json.dump(data, data_file, indent = 2)
				#Delete uncompressed after finish processing
				os.remove(cur_path+file_name)
				print(file_name, ' processed')

def filter_special_chars(word):
	to_filter = ["", "#", "/", ":%"]
	if word in to_filter:
		return False
	return True

def tokenization(text):
	#return a list of filtered tokens
	return list(filter(filter_special_chars, re.split("([\w]+)", text)))

def stripFormatting(text):
	refs = [] #Store references
	#Use HTML parser to remove html tags and content inside them
	soup = BeautifulSoup(text, 'html.parser')
	for html in soup.find_all():
		#retrieve references from <ref> tags
		if html.name == 'ref':
			if len(html.contents) != 0:    #if reference is not empty
				for ref in html.contents:
					refs.append(ref)
		html.decompose()
	text = soup.text

	#Remove infoboxes: Removing all content of nested {{ }} 
	n = 1  # run at least once
	while n:
		text, n = re.subn(r'\{\{[^{}]*\}\}', '', text)  # remove non-nested/flat balanced parts

	#Remove categories, images tags and their content
	text = re.sub(r'\[\[\s*Category:.*?\]\]|\[\[\s*Image:.*?\]\]','',text, flags=re.DOTALL)
	#Remove all links in single square brackets
	# text =re.sub(r'(?<!\[)\[[^\[\]]+\]', '', text, flags = re.DOTALL)
	#Remove everything after External links/Links sections
	text =re.sub('==External [L|l]inks==.*|====[L|l]inks====.*', '', text, flags = re.DOTALL)

	#Remove double square brackets
	text = re.sub(r'(\[\[)(.+?)(\]\])', r'\2', text)
	#Remove new line characters
	text = text.replace('\n', ' ')
	#Remove apostrophe when they are not used to show possession
	text = re.sub("(?<!s)'(?!(?:t|ll|e?m)\b)", '', text)

	return text, refs


if __name__ == '__main__':
	# what we need: 'enwiki-latest-stub-meta-history[0-9]{0,3}.xml.gz'
	compressed_file_pattern = re.compile('enwiki-latest-abstract11.xml.gz')
	
	retrieveData(compressed_file_pattern)
	uncompressData()
	# processData(unprocessed_file_pattern, remove_formatting = True)
	# call php script
	result = subprocess.run(
	    ['php', 'compare/compare.php'],    # program and arguments
	    check=True               # raise exception if program fails
	)
