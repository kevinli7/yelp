import json, re, string
from nltk.corpus import stopwords

filename = 'yelp_academic_dataset_business.json'

# Courtesy of Mark Amery from stackoverflow
# Changes json dictionary from unicode to strings
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

wordcount = dict()
with open(filename, 'r') as businesses:
	for business in businesses:
		curr_business = byteify(json.loads(business))
		categories = curr_business['categories']
		for cat in categories:
			cat = cat.lower()
			if cat not in wordcount:
				wordcount[cat] = 0
			wordcount[cat] = wordcount[cat] + 1

sorted_words = sorted(wordcount.items(), key=lambda x:-1*x[1])

output = ""
for word in sorted_words:
	output += '{0} {1}\n'.format(word[0], word[1])

with open("categories.txt", 'w') as f:
	f.write(output)

