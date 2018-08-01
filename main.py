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
 def retrieveData(file_name_pattern, file_path = 'data/compressed/', baseURL = "https://dumps.wikimedia.org/enwiki/latest/"):
    #Get html content and convert to string
    html_page = requests.get(baseURL).text
    result = file_name_pattern.findall(html_page)
    #Filter overlapping results
    file_names = set(result)
    for file_name in file_names:
        #Download bz2 file
        response = requests.get(baseURL + file_name, stream = True)
        with gzip.open(file_path+file_name, 'wb') as compressed_file:  	           # Total size in bytes.
            file_size = int(response.headers.get('content-length', 0));
            block_size = 1024
            #Write bz2 response to a new file and show progress bar
            for data in tqdm(response.iter_content(block_size), total=math.ceil(file_size//block_size) , unit='KB', unit_scale=True):
                compressed_file.write(data)
 
def uncompressData(input_path = 'data/compressed/', output_path = 'data/unprocessed/', remove_file = False):
	# Preprocess the total number of files
	filetotal = 0
	for file in iter_files(input_path):
		if file.endswith('.7z'):
			filetotal +=1
	count = 0
	#Search compressed files
	for file in iter_files(input_path):
		if file.endswith('.7z'):
			count += 1
			logger.info('Extracting %d/%d files...' %(count, filetotal))
			out_file_name = file[:-4]
			with gzip.open(file, 'rb') as compressed_file, open(out_file_name, 'wb') as output_file:
                for data in iter(lambda : compressed_file.read(1024), b''):
                    output_file.write(data)
        	#Delete compressed file after uncompressing
            if remove_file:
                os.remove(file)
	logger.info('Finish extracting %d files.' %filetotal)
 #Retrieve content from xml files
def processData(input_path = 'data/compressed/', output_path = 'data/unprocessed/', remove_formatting = False, remove_file = False):
	#global dictionary of documents + revision numbers vs categories
	category_files = defaultdict(dict)
	#local dict to store all revisions of category of each document
	local_dict = defaultdict(dict)
 	#Store all existing category file names 
	for cur_path, directories, files in os.walk('data/categories/'):
		for file_name in files:
			category_files[file_name] = 1
	#regex to get all content inside category tags
	category_content_pattern = re.compile('\[\[Category:(.*?)\]\]')
 	filetotal = 0
	for file in iter_files(input_path):
		if file.endswith('.xml'):
			filetotal +=1
	#Search uncompressed files
	filecounter = 0
	for file in iter_files(input_path):
		if file.endswith('.xml'):
			filecounter += 1
			file_name = os.path.basename(file)
			logger.info('Processing %d/%d files...' %(filecounter, filetotal))
			tree = ET.parse(file)
			
			#Get root tag <page>
			root = tree.getroot()[1]
			file_start = '{http://www.mediawiki.org/xml/export-0.10/}'
 				
			json_file_name = file_name[:-3] + 'json'
			with open(output_path+json_file_name, 'w') as json_file:
				revision_count = 0
				data = {}
				for revision in root.iter(file_start+'revision'):
					revision_count += 1
					text = revision.find(file_start+'text').text
					if text != None:
						#retrieve categories and references from text
						categories = category_content_pattern.findall(text)
						if len(categories): 
							for cat in categories:  
								if cat not in local_dict:  
									local_dict[cat] = revision_count
 						if remove_formatting:	
							text, refs = stripFormatting(text)
						data[revision_count] = {
							'text': text,
							'categories': categories,
							'references': refs
						}
				#Write to json file
				json.dump(data, json_file, indent = 2)
 				# for category, revision_number in local_dict.items():
				# 	if category in category_files:  #if a category file has existed
				# 		with open('data/categories/'+category+".txt", "a") as category_file:  #append to the file
				# 			#store document's name and revision number
				# 			category_file.write(file_name + ' ' + str(revision_number) + '\n')
				# 			# for num in revision_number:	#uncomment this to have array of all revision numbers
				# 			# 	category_file.write(' '+ str(num))
				# 	else:
				# 		with open('data/categories/'+category+".txt", "w") as category_file:  #create a new file
				# 			category_file.write(file_name + ' ' + str(revision_number) + '\n')
				# 			# for num in revision_number:
				# 			# 	category_file.write(' '+ str(num))
			#Delete original file
			if remove_file:
				os.remove(file)
	logger.info('Finish processing %d files.' %filetotal)
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
	# what we need: 'enwiki-latest-pages-meta-history[0-9]{0,2}.xml.*\.bz2'
	file_pattern = re.compile('enwiki-latest-pages-meta-history1{0,3}.xml.*\.7z')
#retrieveData(file_pattern)
uncompressData()
	#processData(remove_formatting = True)
	# call php script
	#result = subprocess.run(
	 #   ['php', 'compare/compare.php'],    # program and arguments
	  #  check=True               # raise exception if program fails