from diff_match_patch import diff_match_patch, patch_obj
import pprint

INPUT_SENTS_DIR = 'data/raw_sent_pair/in_sent/in'
OUTPUT_SENTS_DIR = 'data/raw_sent_pair/out_sent/out'

pp = pprint.PrettyPrinter(indent=4)

Diff = diff_match_patch()


with open(INPUT_SENTS_DIR, 'r') as in_file, open(OUTPUT_SENTS_DIR, 'r') as out_file:
	in_sent = in_file.readline().strip()
	out_sent = out_file.readline().strip()
	pair_ctr = 1
	while pair_ctr == 1:
		diffs = Diff.diff_main("\"This article is about the city of Philadelphia, Pennsylvania; see also other cities called Philadelphia\" Philadelphia is a large city in Pennsylvania, USA."
			, "\"This article is about the city of Philadelphia, Pennsylvania; see also other cities called Philadelphia\" Philadelphia is a large city in Pennsylvania, USA.")

		edit_distance = Diff.diff_levenshtein(diffs)
		if edit_distance > 0 and edit_distance <= 4:
			pprint.pprint(diffs)
			pprint.pprint(edit_distance)

		
		#Proceed to the next pair
		in_sent = in_file.readline().strip()
		out_sent = out_file.readline().strip()
		pair_ctr += 1


