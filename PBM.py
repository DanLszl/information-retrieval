from pprint import pprint
from collections import defaultdict
from tqdm import tqdm
import numpy as np
from numpy.random import binomial

from data_parser import parse_log_data


class PositionBasedModel:
	def __init__(self, session_data, clicks_per_session, fixed_alpha = 1e-2):
		self.alphas, self.gammas = self.estimate_parameters(session_data, clicks_per_session)
		self.fixed_alpha = fixed_alpha

	def estimate_alphas(self, alphas, gammas, session_data, clicks_per_session):
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


	def estimate_gammas(self, alphas, gammas, session_data, clicks_per_session):
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


	def estimate_parameters(self, session_data, clicks_per_session, num_iterations = 50):
		'''
		EM algorithm
		'''
		alphas = defaultdict(lambda:np.random.uniform(0.25, 0.75))
		gammas = defaultdict(lambda:np.random.uniform(0.25, 0.75))

		print('Training PBM Model')
		for iteration in tqdm(range(num_iterations)):	
			new_alphas = self.estimate_alphas(alphas, gammas, session_data, clicks_per_session)
			new_gammas = self.estimate_gammas(alphas, gammas, session_data, clicks_per_session)		
			
			alphas = new_alphas
			gammas = new_gammas

		return alphas, gammas


	def simulate_clicks(self, interleaved_results, *args):
		p_click = self.click_probability(interleaved_results, args[0])
		clicks = np.array([binomial(1, prob) for prob in p_click])
		
		return np.where(clicks)[0]


	def click_probability(self, interleaved_results, *args):
		p_gammas = np.array([val for val in self.gammas.values()])
		p_gammas = p_gammas[:len(interleaved_results)]
		relevance = args[0]		
		p_alphas = np.array([self.fixed_alpha 
							if relevance[idx] == 0
							else 1 - self.fixed_alpha
							for idx in range(len(interleaved_results))])

		return p_gammas * p_alphas

 
if __name__ == "__main__":
	interleaved_results = [2, 0, 3, 1, 4]
	relevance = [1, 0, 0, 1, 0]
	log_file = "YandexRelPredChallenge.txt"
	session_data, clicks_per_session = parse_log_data(log_file)
	pmb_model = PositionBasedModel(session_data, clicks_per_session)
	pmb_model.simulate_clicks(interleaved_results, relevance)


