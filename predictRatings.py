import numpy as np
from sklearn import neighbors
import filter as f

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
			reviewJson = getJson(r)
			userID = getUser(reviewJson)
			businessID = getBusiness(reviewJson)		
			text = getText(reviewJson)
			rate = getRate(reviewJson)
			if businessId not in Business.busiID2Busi.keys():
				busiObj = Business(businessID, numNeighbors)
				self.businessCount+=1
			else:
				busiObj = Business.busiID2Busi[businessId]
			if userID not in User.userID2User.keys():
				userObj = User(userID)
				self.userCount+=1
			else:
				userObj = User.useID2User[userID]
			userObj.addReview(text)
			busiObj.addUser(userObj,rate)
			self.busiID2Busi[businessID] = businessObj
			self.userID2User[userID] = userObj
		reviews.close()
		for b in self.busiID2Busi.values():
			b.trainKNN(self.featureType)
	def predictKNN(self, userID, businessID):
		userObj = self.userID2User[userID]
		busiObj = self.busiID2Busi[businessID]
		return busiObj.predictKNN(userObj)

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
		return np.array(map(lambda user: User.calcFeature(user, featureType),listUsers))
	def trainKNN(self, featureType):
		features = self.getFeatureArray(featureType)
		self.knnClassifier.fit(features, self.listRate)
		self.featureType = featureType
	def predictKNN(self, userObj):
		assert self.featureType is not iNone
		return self.knnClassifier.predict(np.array([userObj.calcFeature(self.featureType)]))
	
