import re, string
from nltk.corpus import stopwords


class User:
	# The set of words that we select as features
	wordFilename = "data/words.txt"
	wordset, wordlist = loadWordSet(wordFilename)

	# Punctuation regex and stopwords
	punctuation = re.compile('[%s]' % re.escape(string.punctuation))
	stopwords = set(stopwords.words())

	#UserID to User
	# userID2User = dict()

	#Features
	featureSet = set(["selectedPercentage", "selectedPercentile", "totalPercentage", "totalPercentile"])

	def __init__(self, userID):
		self.userID = userID
		self.wordCounts = dict()
		self.selectedWordCountDict = dict()
		self.totalWordCount = 0
		self.selectedWordCount = 0

		self.hasFeatures = False

		# User.userID2User[userId] = self

	def getID(self):
		return self.userID

	def loadWordSet(filename):
		l = list()
		with open(filename, 'r') as f:
			l = f.read().split('\n')
		return set(l), l

	""" Splits and processes the text of a review from the User
	    and updates word counts accordingly """
	def addReview(self, text):
		text = punctuation.sub('', text):
		words = text.split()
		for word in words:
			if word not in stopwords:
				if word in wordset:
					selectedWordCount += 1
					if word not in selectedWordCountDict:
						selectedWordCountDict[word] = 0
					selectedWordCountDict[word] += 1
				totalWordCount += 1
				if word not in wordCounts:
					wordCounts[word] = 0
				wordCounts[word] += 1

	""" Calcs and returns a feature array """
	def calcFeature(self, featureType="selectedPercentage"):
		if featureType not in featureSet:
			print("Not a valid feature.")
			return;
		if not self.hasFeatures:
			self.features = {
					'selectedPercentage': calcPercentage(selectedWordCountDict, selectedWordCount),
					'selectedPercentile': calcPercentile(selectedWordCountDict),
					'totalPercentage': calcPercentage(wordCounts, totalWordCount),
					'totalPercentile': calcPercentile(wordCounts)
					}
			self.hasFeatures = True:
		return self.features[featureType]

	""" Calcualtes the percentage of selected words from wordlist
	    using the wordCoutn dictionary and total passed in """
	def calcPercentage(wordCounts, total):
		features = list()
		for word in wordlist:
			if word in wordCounts:
				features.append(wordCounts[word]/total)
			else:
				features.append(0.0)
		return features

	""" Calculates the percentile of each selected word list from
	    the wordCount dictionary """
	def calcPercentile(wordCounts):
		sortedWordCounts = sorted(wordCounts.items(), key=lambda x:x[1])
		numWords = len(wordCounts)
		rank = dict()
		count = 1
		for word in sortedWordCounts:
			rank[word[0]] = count
			count += 1

		features = list()
		for word in wordlist:
			if word in rank:
				features.append(rank[word]/numWords)
			else:
				features.append(0.0)
		return features






