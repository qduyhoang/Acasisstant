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



if __name__ == '__main__':
	# what we need: 'enwiki-latest-pages-meta-history[0-9]{0,2}.xml.*\.bz2'
	file_pattern = re.compile('enwiki-latest-pages-meta-history1{0,3}.xml.*\.7z')
#retrieveData(file_pattern)
# uncompressData()
	#processData(remove_formatting = True)
	# call php script
	result = subprocess.run(
	   ['php', 'compare/compare.php'],    # program and arguments
	   check=True         )      # raise exception if program fails