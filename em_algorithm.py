from pprint import pprint
from collections import defaultdict
from tqdm import tqdm
import numpy as np

from data_parser import parse_log_data


def estimate_alphas(alphas, gammas, session_data, clicks_per_session):
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
		sum_weights = sum(_alphas[pair]['weigth']) + 1
		sum_count = sum(_alphas[pair]['count']) + 2
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
				weight = (1 - alphas[(query_id, doc)]) * gammas[doc_rank] / (1 - gammas[doc_rank]*alphas[(query_id, doc)])

			_gammas[doc_rank]['weigth'].append(weight)
			_gammas[doc_rank]['count'].append(1)

	for rank in _gammas.keys():
		sum_weights = sum(_gammas[rank]['weigth']) + 1
		sum_count = sum(_gammas[rank]['count']) + 2
		gammas[rank] = sum_weights / sum_count

	return gammas


def estimate_parameters(session_data, clicks_per_session, num_iterations = 50, convergence_criteria = 10**-5):
	'''
	EM algorithm
	'''
	alphas = defaultdict(lambda:np.random.uniform(0.25, 0.75))
	gammas = defaultdict(lambda:np.random.uniform(0.25, 0.75))

	print('Training PBM Model')
	for iteration in tqdm(range(num_iterations)):	
		new_alphas = estimate_alphas(alphas, gammas, session_data, clicks_per_session)
		new_gammas = estimate_gammas(alphas, gammas, session_data, clicks_per_session)		
		
		alphas = new_alphas
		gammas = new_gammas

	return alphas, gammas


 
if __name__ == "__main__":
	log_file = "YandexRelPredChallenge.txt"
	session_data, clicks_per_session = parse_log_data(log_file)
	alphas, gammas = estimate_parameters(session_data, clicks_per_session, num_iterations = 50)
	pprint(gammas)