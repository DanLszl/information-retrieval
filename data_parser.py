import pprint as pp
from collections import defaultdict

# SessionID TimePassed TypeOfAction QueryID RegionID ListOfURLs
# SessionID TimePassed TypeOfAction URLID

def get_document_query_pairs(log_file):
	with open(log_file, 'r') as in_file:
		pairs = defaultdict(list)
		for line in in_file:
			line = line.split()
			if line[2] == "Q":
				ranked_docs = line[5:]
				for doc in ranked_docs:
					pairs[line[3]].append(doc)
			
	return pairs


def initialise_query_data(pairs):
	query_data = dict()
	for query_id, docs in pairs.items():
		for doc in docs:
			query_data[(query_id, doc)] = {'session_ids': [],
												'rankings': []}

	return query_data


def get_clicks_per_session(log_file):
	clicks_per_session = defaultdict(list)
	with open(log_file, 'r') as in_file:
		for line in in_file:
			line = line.split()
			if line[2] == "C":
				clicks_per_session[line[0]].append(line[3])

	return clicks_per_session


def parse_query_data(log_file, query_data):
	with open(log_file, 'r') as in_file:
		for line in in_file:
			line = line.split()
			if line[2] == "Q":
				query_id = line[3]
				ranked_docs = line[5:]
				rank_count = 0 #rank starts at 0
				for doc in ranked_docs:
					query_data[(query_id, doc)]['session_ids'].append(line[0])
					query_data[(query_id, doc)]['rankings'].append(rank_count)
					rank_count += 1

	return query_data


def parse_log_data(log_file):
	pairs = get_document_query_pairs(log_file)
	query_data = initialise_query_data(pairs)
	data_per_query_doc = parse_query_data(log_file, query_data)
	clicks_per_session = get_clicks_per_session(log_file)

	return data_per_query_doc, clicks_per_session


if __name__ == "__main__":
	log_file = "YandexRelPredChallenge.txt"

	pairs = get_document_query_pairs(log_file)
	query_data = initialise_query_data(pairs)
	query_data = parse_query_data(log_file, query_data)
	# pp.pprint(query_data)
	# pp.pprint(get_clicks_per_session(log_file))

	






