import random

def getRandom():
	return random.random()

def splitReviews(reviewFile, splitPoints=[0.64, 0.80], splits=['training', 'validation', 'test']):
	prefix = "data/"
	suffix = "_set.json"
	files = list()
	for split in splits:
		files.append(open(prefix + split + suffix, 'w'))
	reviews = open(reviewFile, 'r')
	for review in reviews:
		r = getRandom()
		if r < splitPoints[0]:
			files[0].write(review)
		elif r > splitPoints[1]:
			files[2].write(review)
		else:
			files[1].write(review)
	reviews.close()
	for f in files:
		f.close()
	return 1

if __name__ == "__main__":
	filename = 'data/yelp_filtered_reviews.json'
	splitReviews(filename)
	print("yay")

