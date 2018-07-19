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


def getTotalFileSize(file_path, file_name_pattern):
	sizecounter = 0
	for cur_path, directories, files in tqdm(os.walk(file_path), unit="files"):
		for file_name in files:
			if file_name_pattern.match(file_name):
				sizecounter += os.path.getsize(cur_path)
	return sizecounter

def retrieveData(file_name_pattern, file_path = 'data/unprocessed/', baseURL = "https://dumps.wikimedia.org/enwiki/latest/"):
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

def uncompressData(file_name_pattern, file_path = 'data/unprocessed/'):
	# Preprocess the total files sizes
	sizecounter = getTotalFileSize(file_path, file_name_pattern)
	for cur_path, directories, files in tqdm(os.walk(file_path), unit="files"):
		for file_name in files:
			if file_name_pattern.match(file_name):
				sizecounter += os.path.getsize(cur_path)

	# Show progress using file size
	with tqdm(total = sizecounter, unit = 'B', unit_scale = True, unit_divisor = 1024) as progressBar:
		compressed_file_exist = False
		#Search compressed files
		for cur_path, directories, files in tqdm(os.walk(file_path), unit="files"):
			for file_name in files:
				if file_name_pattern.match(file_name):	
					compressed_file_exist = True
					out_file_name = file_name[:-3]
					with gzip.open(cur_path+file_name, 'rb') as compressed_file:
						with open(cur_path+out_file_name, 'wb') as uncompressed_file:
							buf = 1
							while buf:
								#Decompress file and save
								buf = gzip.decompress(compressed_file.read())
								uncompressed_file.write(buf)
							if buf:
								progressBar.set_postfix(file=filepath[-10:], refresh=False)
								progressBar.update(len(buf))
					#Delete compressed file after uncompressing
					os.remove(cur_path+file_name)
		if compressed_file_exist:
			print('Files uncompressed')
		else:
			print('Nothing to uncompress')


#Retrieve content from xml files
def processData(file_name_pattern, file_path = 'data/unprocessed/', remove_formatting = False):
	#Content of category
	category_content_pattern = re.compile('\[\[Category:(.*?)\]\]')
	#Search uncompressed files
	for cur_path, directories, files in os.walk(file_path):
		for file_name in files:
			if file_name_pattern.match(file_name):
				print(file_name, ' processing')
				tree = ET.parse(cur_path+file_name)
				#Get root tag <page>
				root = tree.getroot()[1]
				file_start = '{http://www.mediawiki.org/xml/export-0.10/}'

				json_file_name = file_name[:-3] + 'json'
				with open(file_path+json_file_name, 'a') as data_file:
					#Get text content of all revision and store revision number
					i = 1
					for revision in root.iter(file_start+'revision'):
						data = {}
						text = revision.find(file_start+'text').text
						if text != None:
							#Get categories of the current revision
							category = category_content_pattern.findall(text)
							if remove_formatting:
								text, refs = stripFormatting(text)
							# text = tokenization(text)
							data[i] = text, category, refs

							#Write data in json format
							json.dump(data, data_file)
							data_file.write('\n') 
							i += 1
				#Delete uncompressed after finish processing
				os.remove(cur_path+file_name)
				print(file_name, ' processed')


def tokenization(text):
	protoblocks = re.split(' ', text)
	with open("chars.txt", "r") as f:
	    chars = f.read()
	results = []
	for protoblock in protoblocks:
	    newblocks = []
	    newblocks.extend(re.findall("([^"+chars+"0-9\']+|["+chars+"0-9\']+)", protoblock))
	    for block in newblocks:
	        if not re.search("["+chars+"0-9\']+", block):
	            results.extend(block)
	        else:
	            results.append(block)
	return results
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
	#Remove backslash characters
	# text = text.replace('\\', '')
	#Remove apostrophe when they are not used to show possession
	text = re.sub("(?<!s)'(?!(?:t|ll|e?m)\b)", '', text)
	#Return stripped formatting text and references 
	return text, refs


if __name__ == '__main__':
	# what we need: 'enwiki-latest-stub-meta-history[0-9]{0,3}.xml.gz'
	compressed_file_pattern = re.compile('enwiki-latest-abstract11.xml.gz')
	unprocessed_file_pattern = re.compile('wiki.xml')

	# retrieveData(compressed_file_pattern)
	# uncompressData(compressed_file_pattern)
	processData(unprocessed_file_pattern, remove_formatting = True)
	# #call php script
	# result = subprocess.run(
	#     ['php', 'compare/compare.php'],    # program and arguments
	#     check=True               # raise exception if program fails
	# )
