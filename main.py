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


def retrieveData(file_path = 'data/', baseURL = "https://dumps.wikimedia.org/enwiki/latest/"):
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
				block_size = 1024
				#Write gzip response to a new file and show progress bar
				for data in tqdm(response.iter_content(block_size), total=math.ceil(file_size//block_size) , unit='KB', unit_scale=True):
					compressed_file.write(data)
	return file_names

def uncompressData(file_path, compressed_file_list):
	# Preprocess the total files sizes
	sizecounter = 0
	for cur_path, directories, files in tqdm(os.walk(file_path), unit="files"):
		for file in files:
			if file in compressed_file_list:	
				sizecounter += os.path.getsize(cur_path)

	# Load tqdm with size counter instead of file counter
	with tqdm(total = sizecounter, unit = 'B', unit_scale = True, unit_divisor = 1024) as progressBar:
		compressed_file_exist = False
		#Search compressed files
		for cur_path, directories, files in tqdm(os.walk(file_path), unit="files"):
			for file in files:
				if file in compressed_file_list:	
					compressed_file_exist = True
					out_file_name = file[:-3]
					with gzip.open(cur_path+file, 'rb') as compressed_file:
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
					os.remove(cur_path+file)
		if compressed_file_exist:
			print('Files uncompressed')
		else:
			print('Nothing to uncompress')


def processData(file_name):
	file_path = 'data'
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
	compressed_file_list = retrieveData()
	# processData('enwiki-latest-abstract11.xml')
	# call php script
	uncompressData('data/', ['enwiki-latest-abstract11.xml.gz'])
	# result = subprocess.run(
	#     ['php', 'compare/compare.php'],    # program and arguments
	#     check=True               # raise exception if program fails
	# )

