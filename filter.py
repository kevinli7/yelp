import json
import os
import datetime
	
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def getJson(json_string):
  return byteify(json.loads(json_string))

def getDate(review_json):
	date_str = review_json['date']
	y,m,d = map(lambda x: int(x), date_str.replace('-', ' ').split())
	date = datetime.date(y,m,d)
	return date

def getUser(review_json):
	return review_json['user_id']

def getBusiness(review_json):
	return review_json['business_id']

def getText(review_json):
	return review_json['text']

def getRate(review_json):
	return review_json['stars']

def filter_reviews(review_file, min_user_reviews, min_busi_reviews, data_path="data"):
	reviews = open(review_file, 'r')
	u2b = dict()
	b2u = dict()
	ub2d = dict()
	eliminate = set()
	print("Reading in file and populating dict...")  	
	for r in reviews:
		review_json = getJson(r)
		user = getUser(review_json)
		business = getBusiness(review_json)
		date = getDate(review_json)
		if (user,business) in ub2d:
			if ub2d[(user,business)]>date:
				eliminate.add((user,business,date))
			else:
				eliminate.add((user,business,ub2d[(user,business)]))
				ub2d[(user,business)]=date
		else:
			ub2d[(user,business)]=date
			if user not in u2b:
				u2b[user]=set()
			u2b[user].add(business)
			if business not in b2u:
				b2u[business]=set()
			b2u[business].add(user)
	reviews.close()
	print("Finding users with over {0} reviews...".format(min_user_reviews))
	qualified_users = set([u for (u,b) in u2b.items() if len(b)>=min_user_reviews])
	print("Removing reviews from users without 35 reviews and populating new dict...")
	b2u = {b:(u.intersection(qualified_users)) for (b,u) in b2u.items()}
	print("Selecting businesses with over {0} reviews...".format(min_busi_reviews)) 
	qualified_business = set([b for (b,u) in b2u.items() if len(u)>=min_busi_reviews])
	reviews = open(review_file, 'r')
	new_reviews = open(os.path.join(data_path, 'yelp_filtered_reviews.json'), 'w')
	print("Writing new data file...") 
	for r in reviews:
		review_json = getJson(r)
		user = getUser(review_json)
		business = getBusiness(review_json)
		date = getDate(review_json)
		if (user,business,date) not in eliminate and user in qualified_users and business in qualified_business:
			new_reviews.write(r)
	new_reviews.close()
	reviews.close()
	print("Done") 
	
if __name__ == "__main__":	
	#Minimum reviews
	user_reviews = 35
	busi_reviews = 100
	#file information
	data_path = "data/"
	file_path = 'data/yelp_academic_dataset_review.json'
	filter_reviews(file_path, user_reviews, busi_reviews, data_path="data")
