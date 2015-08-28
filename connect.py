import json, re, string
from datetime import datetime

filename = 'yelp_academic_dataset_review.json'
# p = re.compile('[%s]' % re.escape(string.punctuation))

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

# Loads a .json file with multiple json objects on different lines
def populate_dict(filename):
	U2B = dict()
	B2U = dict()
	with open(filename, 'r') as reviews:
		for review in reviews:
			curr_review = byteify(json.loads(review))
			user = curr_review['user_id']
			business = curr_review['business_id']
			if user not in U2B:
				U2B[user] = list()
			if business not in B2U:
				B2U[business] = list()
			U2B[user].append(business)
			B2U[business].append(user)
	return U2B, B2U

#UserToBusiness, BusinessToUser = populate_dict(filename)

def count_overlap(U2B, B2U, threshold=5):
	User_Overlap = dict()
	for user in U2B:
		temp = dict()
		count = 0
		for business in U2B[user]:
			for u in B2U[business]:
				if u == user: continue
				if u not in temp:
					temp[u] = 0
				temp[u] = temp[u] + 1
		for key in temp:
			if temp[key] >= threshold:
				count += 1
		User_Overlap[user] = count
	return User_Overlap

#User_Overlap = count_overlap_shiori(UserToBusiness, BusinessToUser)

def populate_dict_shiori(file_name):
	U2B = dict()
	B2U = dict()
	f = open(filename, 'r')
	for line in f:
		review = json.loads(line)
		user = review['user_id']
		business = review['business_id']
		if user not in U2B:
			U2B[user] = set()
		if business not in B2U:
			B2U[business]=set()
		B2U[business].add(user)
		U2B[user].add(business)
	return U2B, B2U

def count_overlap_shiori(U2B, B2U, threshold=5):
	User_Overlap = dict()
	for user in U2B:
		business = U2B[user]
		otherUsers = set()
		for b in business:
			otherUsers =  otherUsers.union(B2U[b])
		otherUsers.remove(user)
		overlaps = map(lambda user: len(business.intersection(U2B[user])), otherUsers)
		over_thresh = map(lambda overlap: overlap>=threshold, overlaps)
		User_Overlap[user]=sum(over_thresh)
	return User_Overlap



# with open("user_relations.txt", 'w') as f:
# 	f.write(output)

