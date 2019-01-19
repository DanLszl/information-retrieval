
from data_parser import parse_log_data
from pprint import pprint
from numpy.random import binomial


def estimate_rho(session_data, clicks_per_session):
    ndocs = 0
    nclicks = 0
    for id, docs in session_data.items():
        ndocs += len(docs['doc_ids'])
        nclicks += len(clicks_per_session[id])
    return nclicks / ndocs


def simulate_clicks(rho, size=3):
    return binomial(1, rho, size)


if __name__ == "__main__":
    log_file = "YandexRelPredChallenge.txt"
    session_data, clicks_per_session = parse_log_data(log_file)
    rho = estimate_rho(session_data, clicks_per_session)
    pprint("Rho: %0.3f" % rho)
    pprint(simulate_clicks(rho))
