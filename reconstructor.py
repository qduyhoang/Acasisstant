import os
original = "William Shakespeare (1564-1616) was a poet, playwright, and actor in England.  He predominantly wrote between 1585 and 1610. Considering how well respected he is today, remarkably little is actually known of his life.  This fact accounts for the many theories on who, other than the actor William Shakespeare, may have written the works. Shakespeares reputation--as a poet and dramaturgist--has ebbed and flowed over the past five centuries.   His dramatic work is traditionally categorized in the following divisions: :Shakespearean tragedies :: Romeo and Juliet :: Macbeth :: King Lear :: Hamlet :: Othello :Shakespearean comedies :: Alls Well That Ends Well--Text|Alls Well That Ends Well :: As You Like It--Text|As You Like It :: A Midsummer Nights Dream|A Midsummer Nights Dream :: Much Ado About Nothing :: Measure for Measure :: The Tempest :Shakespearean histories ::Julius Caeser ::Antony and Cleopatra ::Richard III ::Richard II ::Henry V ::Henry I  His other literary works include: :Shakespearean Sonnets (See Sonnet) :Shakespearean Long Poetry  Some famous \/quotations See also his contemporaries Christopher Marlowe and Elizabeth I|Queen Elizabeth I. ---- \/How to upload Shakespeare to Wikipedia--a good cause  \/Talk"
deleted =  [
         167,
        168,
        172
    ]
added = [
        [
            167,
            "Marlowe,"
        ],
        [
            171,
            "I,"
        ],
        [
            172,
            "and"
        ],
        [
            173,
            "Edward"
        ],
        [
            174,
            "de"
        ],
        [
            175,
            "Vere."
        ]
    ]
#Search uncompressed files
# for cur_path, directories, files in os.walk('data/processed/'):
# 	for file_name in files:
# 		if file_name.endswith('json'):
# 			print(file_name)
# 			with open(cur_path+file_name, 'r') as processed_file:
# 				print(processed_file.read())

words = original.split()
for i in deleted[::-1]:
    words.pop(i)
for item in added:
	index = item[0]
	word = item[1]
	words.insert(index, word)
print(' '.join(words))