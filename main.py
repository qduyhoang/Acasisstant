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


def retrieveData(baseURL = "https://dumps.wikimedia.org/enwiki/latest/"):
	file_path = 'data/'
	#Get html content and convert to string
	html_page = requests.get(baseURL).text
	#Get history files'name
	pattern = re.compile('enwiki-latest-abstract11.xml.gz')  #Replace this small file for testing purpose
	result = pattern.findall(html_page)											  #enwiki-latest-abstract11.xml.gz  
	#Filter overlapping results												  #original: 'enwiki-latest-stub-meta-history[0-9]{0,3}.xml.gz'
	file_names = set(result)
	for file_name in file_names:
		if file_name == 'enwiki-latest-abstract11.xml.gz':
			#Download gzip file
			response = requests.get(baseURL + file_name, stream = True)
			with gzip.open(file_path+file_name, 'wb') as compressed_file:
				# Total size in bytes.
				file_size = int(response.headers.get('content-length', 0));
				block_size = 4096
				bytes_so_far = 0
				#Write gzip response to a new file and show progress bar
				for data in tqdm(response.iter_content(block_size), total=math.ceil(file_size//block_size) , unit='KB', unit_scale=True):
					bytes_so_far += len(data)
					compressed_file.write(data)

			#Decompress file and save
			with gzip.open(file_path+file_name) as compressed_file:
				file_content = gzip.decompress(compressed_file.read())
				out_file_path = file_name[:-3]
				with open(file_path+out_file_path, 'wb') as out_file:
					out_file.write(file_content)
			#Delete compressed file after done
			os.remove(file_path+file_name)

def processData(file_name):
	file_path = 'data/'
	tree = ET.parse(file_path+file_name)
	#Get root tag <page>
	root = tree.getroot()[1]	
	file_start = '{http://www.mediawiki.org/xml/export-0.10/}'
	data = {}

	#Get text content of all revision and store revision number
	i = 1
	for revision in root.iter(file_start+'revision'):
		text = revision.find(file_start+'text').text
		if text != None:
			data[i] = text
			i += 1
	#Write a new file with filtered data as json format
	with open(file_path+'data.json', 'w') as data_file:
		json.dump(data, data_file, indent = 4)
	os.remove(file_path+file_name)

if __name__ == '__main__':
	retrieveData()
	processData('enwiki-latest-abstract11.xml')
	# call php script

	result = subprocess.run(
	    ['php', 'compare/compare.php'],    # program and arguments
	    check=True               # raise exception if program fails
	)

