import json

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

""" Loads a .json file with multiple json objects on different lines
    filename: filename of the .json file
    outputs (temp, U2B, B2U)
    temp is list of json objects
    U2B is a dictionary (string, set) of users ids to businesses they review
    B2U is a dictionary (string, set) of business ids to users who have reviewed them """
def populate_dict(filename):
	U2B = dict()
	B2U = dict()
	temp = list()
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
			temp.append(curr_review)
	return temp, U2B, B2U




if __name__ == "__main__":
	#Minimum reviews
	user_reviews = 35
	busi_reviews = 100
	
	#file information
	data_path = "data/"
	filename = 'yelp_academic_dataset_review.json'

	print("Reading in file and populating dict...")
	reviews_json, UserToBusiness, BusinessToUser = populate_dict(filename)
	del BusinessToUser