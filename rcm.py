
from data_parser import parse_log_data
from pprint import pprint
import numpy as np
from numpy.random import binomial


class RandomClickModel:
    def __init__(self, session_data, clicks_per_session):
        self.rho = self.estimate_parameters(session_data, clicks_per_session)

    def estimate_parameters(self, session_data, clicks_per_session):
        ndocs = 0
        nclicks = 0
        for id, docs in session_data.items():
            ndocs += len(docs['doc_ids'])
            nclicks += len(clicks_per_session[id])
        return nclicks / ndocs

    def simulate_clicks(self, interleaved_results, *args):
        '''
        Returns idx of clicked document on the interleaved_results list
        '''
        p_click = self.click_probability(interleaved_results)
        clicks = np.array([binomial(1, prob) for prob in p_click])
        return np.where(clicks)[0]
        
    def click_probability(self, interleaved_results):
        click_probabilities = [self.rho for _ in range(len(interleaved_results))]
        return click_probabilities


def get_session_data_and_clicks_per_session():
    log_file = "YandexRelPredChallenge.txt"
    session_data, clicks_per_session = parse_log_data(log_file)
    return session_data, clicks_per_session


if __name__ == "__main__":
    log_file = "YandexRelPredChallenge.txt"
    session_data, clicks_per_session = parse_log_data(log_file)
    model = RandomClickModel(session_data, clicks_per_session)
    pprint("Rho: %0.3f" % model.rho)
    pprint(model.simulate_clicks([1, 2, 3, 4, 5, 6]))
