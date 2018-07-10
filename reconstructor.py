import os
original = "Drexel University is an institution of higher learning located in Philadelphia, Pennsylvania.  The school was founded in 1891 by Anthony J. Drexel, a noted financier and philanthropist.  The university has ten colleges and schools: *Arts and Sciences  *Bennett S. LeBow College of Business  *Engineering  *Evening & Professional Studies  *Information Science and Technology  *Media Arts and Design  *School of Biomedical Engineering, Science and Health Systems  *School of Education *School of Environmental Science, Engineering and Policy (SESEP -- now defunct) *Hospitality Management  The schools sports teams are called the Dragons.  They participate in the NCAAs Divison I-AA and the Colonial Athletic Association.  Every year, more than one percent of all graduating engineers in the US graduate from Drexel University.  When people think they are getting a bad deal from the University, the often refer to it as getting the Drexel Shaft.  Drexel University borders The University of Pennsylvania.  Links: *[http:\/\/www.drexel.edu Drexel University]"
deleted =  [
        44,
        45,
        46,
        47,
        54,
        56,
        58,
        64,
        65,
        66,
        67,
        68,
        69,
        70,
        71,
        72,
        73,
        74,
        75,
        76,
        77
    ]
added = [
        [
            45,
            "*Medicine"
        ],
        [
            46,
            "*Nursing"
        ],
        [
            47,
            "and"
        ],
        [
            48,
            "Health"
        ],
        [
            49,
            "Professions"
        ],
        [
            56,
            "&"
        ],
        [
            58,
            "*Richard"
        ],
        [
            59,
            "C."
        ],
        [
            60,
            "Goodwin"
        ],
        [
            61,
            "College"
        ],
        [
            63,
            "Evening"
        ],
        [
            64,
            "and"
        ],
        [
            65,
            "*Professional"
        ],
        [
            66,
            "Studies"
        ],
        [
            67,
            "====Schools===="
        ],
        [
            68,
            "*Biomedical"
        ],
        [
            74,
            "*Education"
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