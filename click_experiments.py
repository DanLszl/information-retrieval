from collections import defaultdict
from pprint import pprint

from offline_documents_to_online import get_buckets
from online import ProbabilisticInterleaving, TeamDraftInterleaving

from rcm import RandomClickModel, get_session_data_and_clicks_per_session
from PBM import PositionBasedModel


DEBUG = False

session_data, clicks_per_session = get_session_data_and_clicks_per_session()
rcm = RandomClickModel(session_data, clicks_per_session)
pbm = PositionBasedModel(session_data, clicks_per_session)

click_models = {'random': rcm,
                'position-based': pbm}

interleavings = {'probabilistic': ProbabilisticInterleaving,
                 'team-draft': TeamDraftInterleaving}


def iterate_bucket(bucket):
    while True:
        relevances = bucket['relevances']
        if not relevances:
            return
        for rel_pair, data in relevances.items():
            for ranking in data['rankings']:
                yield ranking


def simulate_interleaving_experiment(buckets, interleaving_factory, click_model, k):
    '''
        Simulates click experiments and stores win results in buckets[id][wins]
    '''
    for bucket in buckets.values():
        wins = {'P': 0, 'E': 0}
        bucket['wins'] = wins
        # sample from the bucket k times
        gen = iterate_bucket(bucket)
        for i, ranking in zip(range(k), gen):
            prod_ranking, exp_ranking = ranking.P, ranking.E
            interleaved, prod_docs, exp_docs = interleaving_factory(
                prod_ranking, exp_ranking).run()

            relevances = []
            for doc in interleaved:
                if doc in prod_docs:
                    docs = prod_docs
                    rel = ranking.rel_P
                else:
                    docs = exp_docs
                    rel = ranking.rel_E

                i = docs.index(doc)
                relevances.append(rel[i])

            clicks = click_model.simulate_clicks(interleaved, relevances)

            if DEBUG:
                print('relevances:', relevances)
                print(ranking)
                print('Rankings:', prod_ranking, exp_ranking)
                print('interleaved:', interleaved)
                print('prod_docs', prod_docs)
                print('exp_docs', exp_docs)
                print('clicks', [interleaved[c] for c in clicks])

            winner = assign_winner(clicks, exp_docs, prod_docs, interleaved)
            if winner == 'E':
                wins['E'] += 1
            elif winner == 'P':
                wins['P'] += 1


def assign_winner(clicks, exp_docs, prod_docs, interleaved):
    click_count_E = 0
    click_count_P = 0

    for click_idx in clicks:
        clicked_doc = interleaved[click_idx]
        if clicked_doc in exp_docs:
            click_count_E += 1
        elif clicked_doc in prod_docs:
            click_count_P += 1

    if click_count_E > click_count_P:
        return 'E'
    elif click_count_P > click_count_E:
        return 'P'
    else:
        return 'T'


def run_click_experiments(k):
    results = defaultdict(dict)
    for click_model_name, click_model in click_models.items():
        for interleaving_name, interleaving_factory in interleavings.items():
            buckets = get_buckets()
            simulate_interleaving_experiment(
                buckets, interleaving_factory, click_model, k=k)

            results[interleaving_name][click_model_name] = \
                {b_id: bucket['wins'] for b_id, bucket in buckets.items()}

    return results


if __name__ == '__main__':
    results = run_click_experiments(100)
    pprint(results)


if __name__ == '__test__':
    session_data, clicks_per_session = get_session_data_and_clicks_per_session()
    interleaving_name = 'team-draft'
    interleaving_factory = interleavings[interleaving_name]

    click_model_name = 'random'
    click_model = click_models[click_model_name](
        session_data, clicks_per_session)

    buckets = get_buckets()
    simulate_interleaving_experiment(
        buckets, interleaving_factory, click_model, k=10)

    pprint(buckets)
