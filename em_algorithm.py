from data_parser2 import parse_log_data
import pprint as pp
from collections import defaultdict


def estimate_attention(alphas, gammas, session_data, clicks_per_session):
	_alphas = defaultdict(lambda: defaultdict(list))

	for session, _ in session_data.items():
		query_id = session_data[session]['query_id'][0]
		for doc_rank, doc in enumerate(session_data[session]['doc_ids']):
			if doc in clicks_per_session[session]:
				weight = 1
			else:
				weight = (1 - gammas[doc_rank])*alphas[(query_id, doc)] / (1 - gammas[doc_rank]*alphas[(query_id, doc)])

			_alphas[(query_id, doc)]['weigth'].append(weight)
			_alphas[(query_id, doc)]['count'].append(1)

	for pair in _alphas.keys():
		sum_weights = sum(_alphas[pair]['weigth'])
		sum_count = sum(_alphas[pair]['count'])
		alphas[pair] = sum_weights / sum_count

	return alphas


def estimate_gammas(alphas, gammas, session_data, clicks_per_session):
	_gammas = defaultdict(lambda: defaultdict(list))

	for session, _ in session_data.items():
		query_id = session_data[session]['query_id'][0]
		for doc_rank, doc in enumerate(session_data[session]['doc_ids']):
			if doc in clicks_per_session[session]:
				weight = 1
			else:
				weight = gammas[doc_rank]*(1 - alphas[(query_id, doc)]) / (1 - gammas[doc_rank]*alphas[(query_id, doc)])
			# print('doc', doc, "query", query_id, 'rank', doc_rank)

			_gammas[doc_rank]['weigth'].append(weight)
			_gammas[doc_rank]['count'].append(1)

	for rank in _gammas.keys():
		sum_weights = sum(_gammas[rank]['weigth'])
		sum_count = sum(_gammas[rank]['count'])
		gammas[rank] = sum_weights / sum_count

	return gammas


def em_algorithm(session_data, clicks_per_session, num_iterations = 10):
	alphas = defaultdict(lambda:0.5)
	gammas = defaultdict(lambda:0.5)

	for iteration in range(num_iterations):
		print('running iteration {}'.format(iteration))

		alphas = estimate_attention(alphas, gammas, session_data, clicks_per_session)
		gammas = estimate_gammas(alphas, gammas, session_data, clicks_per_session)

		# pp.pprint(gammas)
	return alphas, gammas



if __name__ == "__main__":
	# YandexRelPredChallenge

	log_file = "test.txt"
	session_data, clicks_per_session = parse_log_data(log_file)
	alphas, gammas = em_algorithm(session_data, clicks_per_session, num_iterations = 50)
	# pp.pprint(gammas)




