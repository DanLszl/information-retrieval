
from data_parser import parse_log_data
from pprint import pprint
import numpy as np
from numpy.random import binomial


class RandomClickModel:
    def __init__(self, session_data, clicks_per_session):
        self.rho = self.estimate_rho(session_data, clicks_per_session)

    def estimate_rho(self, session_data, clicks_per_session):
        ndocs = 0
        nclicks = 0
        for id, docs in session_data.items():
            ndocs += len(docs['doc_ids'])
            nclicks += len(clicks_per_session[id])
        return nclicks / ndocs

    def simulate_clicks(self, interleaved_results, *args):
        clicked_or_not_clicked = binomial(
            1, self.rho, len(interleaved_results))
        return np.where(clicked_or_not_clicked)[0]


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
