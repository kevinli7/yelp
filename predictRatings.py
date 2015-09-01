import numpy as np
from sklearn import neighbors



class Business:
	busiID2Busi = {}
	def __init__(self, busiID, numNeighbors):
		self.userCount = 0
		self.busiID = busiID
		self.listUsers = []
		self.listRate = []
		self.knnClassifier = neighbors.KNeighborsClassifier(numNeighbors, "uniform")
		busiID2Busi[busiID]=self
		self.featureType=None
	def addUser(self, userObj, rate):
		self.listUsers.append(userObj)
		self.listRate.append(rate)
	def getFeatureArray(self, featureType):
		return np.array(map(lambda user: User.calcFeature(user, featureType),listUsers))
	def trainKNN(self, featureType):
		features = self.getFeatureArray(featureType)
		self.knnClassifier.fit(features, self.listRate)
		self.featureType = featureType
	def predictKNN(self, userID):
		assert self.featureType is not  None
		userObj = User.userID2User[userID]
		return self.knnClassifier.predict(np.array([userObj.calcFeature(self.featureType)]))
	
