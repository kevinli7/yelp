import json
filename = 'yelp_academic_dataset_review.json'

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
				U2B[user] = set()
			if business not in B2U:
				B2U[business] = set()
			U2B[user].add(business)
			B2U[business].add(user)
	return U2B, B2U

UserToBusiness, BusinessToUser = populate_dict(filename)

User35 = {k:v for (k,v) in UserToBusiness.items() if len(v) >= user_reviews}



# with open(filter_list, 'r') as f:
# 	filter_set = f.read()

# filter_set = filter_set.split("\n")

# output = []

# with open(filename, 'r') as reviews:
# 	for review in reviews:
# 		curr_review = byteify(json.loads(review))
# 		business = curr_review['business_id']
# 		if business in filter_set:
# 			output.append(review)

# with open("business100.json", 'w') as f:
# 	f.write('\n'.1join(output))