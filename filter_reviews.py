import json
data_path = "data/"
filename = 'yelp_academic_dataset_review.json'

#Minimum reviews
user_reviews = 35
busi_reviews = 100

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

# review_json = list()

# Loads a .json file with multiple json objects on different lines
def populate_dict(filename):
	U2B = dict()
	# B2U = dict()
	temp = list()
	with open(data_path + filename, 'r') as reviews:
		for review in reviews:
			curr_review = byteify(json.loads(review))
			user = curr_review['user_id']
			business = curr_review['business_id']
			if user not in U2B:
				U2B[user] = set()
			# if business not in B2U:
			# 	B2U[business] = set()
			U2B[user].add(business)
			# B2U[business].add(user)
			temp.append(curr_review)
	return temp, U2B #, B2U

# UserToBusiness, BusinessToUser = populate_dict(filename)
print("Reading in file and populating dict...")
reviews_json, UserToBusiness = populate_dict(filename)

# Contains the list of users that have greater than 35 reviews
print("Finding users with over 35 reviews...")
qualified_users = {k:v for (k,v) in UserToBusiness.items() if len(v) >= user_reviews}
userset = set(qualified_users.keys())

# Filters out any reviews that are not by the users in qualified_users
# Using remove is going to take a long time?
BusinessToUser = dict()
reviews_filtered = list()

# may need some attention, current implementation uses lots of memory
# Possible to drop old list from memory?
print("Removing reviews from users without 35 reviews and populating new dict...")
for review in reviews_json:
	# if review['user_id'] not in userset:
	# 	reviews_json.remove(review) #TODO: change implementation, very slow
	# else: 
	if review['user_id'] in userset:
		reviews_filtered.append(review)
		business = review['business_id']
		user = review['user_id']
		if business not in BusinessToUser: 
			BusinessToUser[business] = set()
		BusinessToUser[business].add(user)

del reviews_json

#This dictionary should have all businesses that match the criteria
print("Selecting businesses with over 100 reviews...")
qualified_business = {k:v for (k,v) in BusinessToUser.items() if len(v) >= busi_reviews}
business_set = set(qualified_business.keys())

#Last loop through the reviews to filter out anymore reviews that aren't fitting the criteria
reviews_final = list()
for review in reviews_filtered:
	if review['business_id'] in business_set:
		reviews_final.append(json.dumps(review))

del reviews_filtered

print("Writing new data file...")
with open(data_path + 'yelp_filtered_reviews.json', 'w') as f:
	f.write('\n'.join(reviews_final))

print("Done")