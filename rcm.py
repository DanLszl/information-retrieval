
from data_parser import parse_log_data
from pprint import pprint
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

    def simulate_clicks(self, size=3):
        rho = self.rho
        return binomial(1, rho, size)


if __name__ == "__main__":
    log_file = "YandexRelPredChallenge.txt"
    session_data, clicks_per_session = parse_log_data(log_file)
    model = RandomClickModel(session_data, clicks_per_session)
    pprint("Rho: %0.3f" % model.rho)
    pprint(model.simulate_clicks())
