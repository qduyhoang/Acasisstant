def iter_files(path):
	"""Walk through all files located under a root path."""
	for dirpath, _, filenames in os.walk(path):
		for f in filenames:
			if f != '.DS_Store':
				yield os.path.join(dirpath, f)