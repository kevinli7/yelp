import json, re, string

""" Takes a filename with  a set of words separated by new lines 
    and returns a set of thsoe words """
def create_wordset(filename):
	l = list()
	with open(filename, 'r') as f:
		l = f.read().split('\n')
	return set(l)

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

""" Returns the user form a json """
def get_user(review_json):
	return review_json['user_id']

""" Returns the text of a review """
def get_text(review_json):
	return review_json['text']

""" Returns a json object from string """
def get_json(json_string):
    return byteify(json.loads(json_string))

""" counts the words from a selected word file that appear
    in user reviews """
def count_words(review_file, wordset):
	word_count = dict()
	p = re.compile('[%s]' % re.escape(string.punctuation))
	with open(review_file, 'r') as reviews:
		for review in reviews:
			review_json = get_json(review)
			user = get_user(review_json)
			text = p.sub('', get_text(review_json)).split()
			if user not in word_count:
				word_count[user] = dict()
			for word in text:
				user_dict = word_count[user]
				if word in wordset:
					if word not in user_dict:
						user_dict[word] = 0
					user_dict[word] = user_dict[word] + 1
	return word_count

if __name__ == "__main__":
	filename = "data/yelp_filtered_reviews.json"
	wordset = create_wordset("words.txt")
	word_count = count_words(filename, wordset)
	output = list()
	for user in word_count:
		output.append(user)
		count = 0
		for word in word_count[user]:
			count += word_count[user][word]
			output.append("{0} - {1}".format(word, word_count[user][word]))
		output.append("Total: {0}".format(count))
	output_file = "data/test_count.txt"
	with open(output_file, 'w') as f:
		f.write('\n'.join(output))


