import json, re, string
from nltk.corpus import stopwords

""" Courtesy of Mark Amery from stackoverflow
    Changes json dictionary from unicode to strings """
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

""" Updates dictionary with words from text
    Filters out any words in the set 'filt' """
def count_words(dictionary, words, filt=set()):
	for word in words:
		word = word.lower()
		if word in filt:
			continue
		if word not in dictionary:
			dictionary[word] = 0
		dictionary[word] += 1
	return dictionary

""" Counts the words from filename and returns them in a dictionary
    This assumes that the filename is a text filename that has
    multiple JSON objects separated by line and each JSON object
    has 'field' """
def count_file(filename, field):
	# Empty Dictionary that will be returned
	word_count = dict()
	# Pattern that matches punctuation
	p = re.compile('[%s]' % re.escape(string.punctuation))
	# Set of stopwords from the nltk package
	filter_set = set(stopwords.words())
	with open(filename, 'r') as f:
		for json_string in f:
			curr_json = byteify(json.loads(json_string))
			text = p.sub('', curr_json[field])
			words = text.split()
			word_count = count_words(word_count, words, filter_set)
	return word_count

""" Writes 'text' to the file 'filename' """
def write_file(filename, text):
	with open(filename, 'w') as f:
		f.write(text)

if __name__ == "__main__":
	filename = 'yelp_filtered_reviews.json'
	output_name = 'filtered_word_count.txt'
	data_path = "data/"
	field = 'text'
	print("Counting words...")
	word_count = count_file(data_path + filename, field)
	sorted_words = sorted(word_count.items(), key=lambda x:-1*x[1])
	print("Writing file...")
	write_file(data_path + output_name, '\n'.join("%s %s" % word for word in sorted_words))
	print("Done!")
