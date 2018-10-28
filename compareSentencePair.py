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
	while in_sent and out_sent:
		diffs = Diff.diff_main(in_sent, out_sent)

		if (len(diffs) != 1 and len(diffs) <= len(in_sent)):
			pp.pprint(diffs)

		#Proceed to the next pair
		in_sent = in_file.readline().strip()
		out_sent = out_file.readline().strip()
		pair_ctr += 1


