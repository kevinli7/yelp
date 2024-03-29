import re, string, math
from nltk.corpus import stopwords
import numpy as np
from sklearn import neighbors
import filter as f

class User:
	
	# @classmethod
	# def loadWordSet(filename):
	# 	l = list()
	# 	with open(filename, 'r') as f:
	# 		l = f.read().split('\n')
	# 	return set(l), l

	# The set of words that we select as features
	wordFilename = "data/words.txt"
	wordlist = list()
	with open(wordFilename, 'r') as f:
		wordlist = f.read().split('\n')
	wordset = set(wordlist)

	# Punctuation regex and stopwords
	punctuation = re.compile('[%s]' % re.escape(string.punctuation))
	stopwordSet = set(stopwords.words())

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


	""" Splits and processes the text of a review from the User
	    and updates word counts accordingly """
	def addReview(self, text):
		text = User.punctuation.sub(' ', text)
		words = text.split()
		for word in words:
			if word not in User.stopwordSet:
				if word in User.wordset:
					self.selectedWordCount += 1
					if word not in self.selectedWordCountDict:
						self.selectedWordCountDict[word] = 0
					self.selectedWordCountDict[word] += 1
				self.totalWordCount += 1
				if word not in self.wordCounts:
					self.wordCounts[word] = 0
				self.wordCounts[word] += 1

	""" Calcs and returns a feature array """
	def calcFeature(self, featureType="selectedPercentage"):
		if featureType not in User.featureSet:
			print("Not a valid feature.")
			return;
		#TODO: Has features may need to be set to false if add review is used after calc
		if not self.hasFeatures:
			self.features = {
					'selectedPercentage': User.calcPercentage(self.selectedWordCountDict, self.selectedWordCount),
					'selectedPercentile': User.calcPercentile(self.selectedWordCountDict),
					'totalPercentage': User.calcPercentage(self.wordCounts, self.totalWordCount),
					'totalPercentile': User.calcPercentile(self.wordCounts)
					}
			self.hasFeatures = True
		return self.features[featureType]

	""" Calcualtes the percentage of selected words from wordlist
	    using the wordCoutn dictionary and total passed in """
	@staticmethod
	def calcPercentage(wordCounts, total):
		features = list()
		for word in User.wordlist:
			if word in wordCounts:
				features.append(float(wordCounts[word])/float(total))
			else:
				features.append(0.0)
		return features

	""" Calculates the percentile of each selected word list from
	    the wordCount dictionary """
	@staticmethod
	def calcPercentile(wordCounts):
		sortedWordCounts = sorted(wordCounts.items(), key=lambda x:x[1])
		numWords = len(wordCounts)
		rank = dict()
		count = 1
		for word in sortedWordCounts:
			rank[word[0]] = count
			count += 1

		features = list()
		for word in User.wordlist:
			if word in rank:
				features.append(float(rank[word])/float(numWords))
			else:
				features.append(0.0)
		return features

class Yelp:
	def __init__(self, numNeighbors, reviewFilePath, featureType):			
		self.numNeighbors = numNeighbors
		self.featureType = featureType
		self.busiID2Busi = {}
		self.userID2User = {}
		self.userCount=0
		self.businessCount=0
		reviews = open(reviewFilePath, 'r')
		for r in reviews:
			reviewJson = f.getJson(r)
			userID = f.getUser(reviewJson)
			businessID = f.getBusiness(reviewJson)		
			text = f.getText(reviewJson)
			rate = f.getRate(reviewJson)
			if businessID not in self.busiID2Busi.keys():
				busiObj = Business(businessID, numNeighbors)
				self.busiID2Busi[businessID]=busiObj
				self.businessCount+=1
			else:
				busiObj = self.busiID2Busi[businessID]
			if userID not in self.userID2User.keys():
				userObj = User(userID)
				self.userCount+=1
				self.userID2User[userID]=userObj
			else:
				userObj = self.userID2User[userID]
			userObj.addReview(text)
			busiObj.addUser(userObj,rate)
		reviews.close()
		for b in self.busiID2Busi.values():
			b.trainKNN(self.featureType)
	def predictKNN(self, userID, businessID):
		# TODO: Assert that the user is not null
		if userID not in self.userID2User:
			return -1
		userObj = self.userID2User[userID]
		busiObj = self.busiID2Busi[businessID]
		return busiObj.predictKNN(userObj)

	def testReview(self, reviewJSON):
		review = f.getJson(reviewJSON)
		userID = f.getUser(review)
		businessID = f.getBusiness(review)
		rate = f.getRate(review)
		prediction = self.predictKNN(userID, businessID)
		return (userID, rate == prediction, rate, prediction)

	def testDataSet(self, testSetFileName):
		testSet = open(testSetFileName, 'r')
		total = 0
		true = 0
		score = [0,0,0,0,0]
		diff = list()
		for review in testSet:
			result = self.testReview(review)
			if result[1]: true += 1
			if result[3] != -1:
				score[int(result[3])-1] += 1
				diff.append(abs(int(result[2])-int(result[3])))
				total += 1
		testSet.close()
		average, std = self.avgAndStd(diff)
		# print(diff)
		print "total: {0}".format(total)
		print "true:  {0}".format(true)
		print "ratio: {0}".format((true + 0.0)/(total + 0.0))
		print score
		print "Average difference: {0}  StdDev: {1}".format(average, std)

	def avgAndStd(self, nums):
		variance = 0
		mean = 0
		for num in nums:
			variance += num*num
			mean += num
		variance /= (len(nums) + 0.0)
		mean /= (len(nums) + 0.0)
		variance -= mean*mean
		return mean, math.sqrt(variance)





class Business:
	def __init__(self, busiID, numNeighbors):
		self.userCount = 0
		self.busiID = busiID
		self.listUsers = []
		self.listRate = []
		self.knnClassifier = neighbors.KNeighborsClassifier(numNeighbors, "uniform")
		self.featureType=None
	def addUser(self, userObj, rate):
		self.listUsers.append(userObj)
		self.listRate.append(rate)
		self.userCount+=1
	def getFeatureArray(self, featureType):
		return np.array(map(lambda user: User.calcFeature(user, featureType), self.listUsers))
	def trainKNN(self, featureType):
		features = self.getFeatureArray(featureType)
		self.knnClassifier.fit(features, self.listRate)
		self.featureType = featureType
	def predictKNN(self, userObj):
		assert self.featureType is not None
		# print (userObj.calcFeature(self.featureType))[0]
		return self.knnClassifier.predict(np.array([userObj.calcFeature(self.featureType)]))[0]



if __name__ == "__main__":
	# main()
	training = 'test_data/training_set.json'
	validation = 'test_data/validation_set.json'
	n=15
	print "Selected percentage, neighbors: {0}".format(n)
	y = Yelp(n, training, 'selectedPercentage')
	y.testDataSet(validation)
	print "Selected percentile"
	y = Yelp(n, training, 'selectedPercentile')
	y.testDataSet(validation)
	print "total percentage"
	y = Yelp(n, training, 'totalPercentage')
	y.testDataSet(validation)
	print "total percentile"
	y = Yelp(n, training, 'totalPercentile')
	y.testDataSet(validation)
