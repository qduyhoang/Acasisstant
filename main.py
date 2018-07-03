import xml.etree.ElementTree as ET
import json
import re
import urllib.request
import io
import gzip
import sys
import shutil
import os
import subprocess
from tqdm import tqdm


def retrieveData(baseURL = "https://dumps.wikimedia.org/enwiki/latest/"):
	file_path = 'data/'
	chunk_size = 4096
	#Get html content
	html_page = urllib.request.urlopen(baseURL)
	#Convert html content to string and read
	page = html_page.read().decode('utf-8') 
	#Get history files'name
	pattern = re.compile('enwiki-latest-abstract11.xml.gz')  #Replace this small file for testing purpose
	result = pattern.findall(page)											  #enwiki-latest-abstract11.xml.gz  
	#Filter overlapping results												  #original: 'enwiki-latest-stub-meta-history[0-9]{0,3}.xml.gz'
	file_names = set(result)
	for file_name in file_names:
		if file_name == 'enwiki-latest-abstract11.xml.gz':
			out_file_path = file_name[:-3]
			with gzip.open(file_path+file_name, 'wb') as compressed_file:
				#Download gzip file
				response = urllib.request.urlopen(baseURL + file_name)
				#Save file
				shutil.copyfileobj(response, compressed_file)
				print("Downloading %s" % file_name)
				bytes_so_far = 0
				file_size = response.info().get_all('Content-Length')[0]
				while True:
					chunk = response.read(chunk_size)
					bytes_so_far += len(chunk)
					#progress bar
					done = int(50 * bytes_so_far / int(file_size))
					sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
					sys.stdout.flush()
					if not chunk:
						sys.stdout.write("==========Decompressing===========")    
						sys.stdout.flush()
						break
			#Decompress file and save
			with gzip.open(file_path+file_name) as compressed_file:
				file_content = gzip.decompress(compressed_file.read())
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

