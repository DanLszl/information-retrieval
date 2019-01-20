import numpy as np
from scipy.stats import norm
from math import sqrt, ceil

from pprint import pprint

from collections import defaultdict

from click_experiments import run_click_experiments

# TODO: should ties be removed? - currently they have been removed
# TODO: interleave should be capped @3

def get_sample_size(p_1, p_0=0.5, alpha=0.05, beta=0.1):
    '''
        we set p0 = 0.5 to reflect that each system wins 50% of times.
        p1 is the proportion of times E wins over P out of k simulations.
        α and β specify the level of significance.
            We set α = 0.05 and β = 0.1.
        δ is |p1 − p0|
        z is the standard normal distribution

        Finally, using the continuity correction the minimum sample
        size is determined as:

        Source:
        @inproceedings{azarbonyad2016power,
          title={Power Analysis for Interleaving Experiments by means of Offline Evaluation},
          author={Azarbonyad, Hosein and Kanoulas, Evangelos},
          booktitle={Proceedings of the 2016 ACM International Conference on the Theory of Information Retrieval},
          pages={87--90},
          year={2016},
          organization={ACM}
        }

        See also:
        https://en.wikipedia.org/wiki/Notation_in_probability_and_statistics#Critical_values
    '''

    delta = abs(p_1 - p_0)
    z_alpha = norm.ppf(1-alpha)
    z_beta = norm.ppf(1-beta)
    
    N = (z_alpha * sqrt(p_0*(1-p_0)) + z_beta * sqrt(p_1*(1-p_1)))

    if N == 0.0 or (p_1 - p_0) == 0.0:
        return 0

    N = N / delta
    N = N**2
    N = N + 1/delta
    return N


def nested_defaultdict(depth, inner_factory=list):
    if depth <= 1:
        return defaultdict(list)
    else:
        return defaultdict(lambda: nested_defaultdict(depth-1))


def determine_sample_sizes(n, k):
    table = nested_defaultdict(4)
    for i in range(n):
        print('iteration:', i)
        results = run_click_experiments(k)
        # pprint(results) #debug

        for interleaving, clicks in results.items():
            for click_model, bucket in clicks.items():
                for b_id, wins in bucket.items():
                    if (wins['E'] + wins['P']) > 0:
                        p_1 = wins['E'] / (wins['E'] + wins['P'])     # proportion of wins
                    else:
                        p_1 = wins['E'] / k
                    N = get_sample_size(p_1)
                    table[interleaving][click_model][b_id]['p_1'].append(p_1)
                    table[interleaving][click_model][b_id]['N'].append(ceil(N))

    return table


def get_final_table(sample_sizes):
    final_table = nested_defaultdict(4)
    for interleaving, clicks in sample_sizes.items():
        for click_model, data in clicks.items():
            for b_id, bucket in data.items():
                final_table[interleaving][click_model][b_id]['min N'] = np.min(
                    bucket['N'])
                final_table[interleaving][click_model][b_id]['median N'] = np.median(
                    bucket['N'])
                final_table[interleaving][click_model][b_id]['max N'] = np.max(
                    bucket['N'])
    return final_table


def print_final_table(final_table):
    for interleaving in final_table.keys():
        for click_model in final_table[interleaving].keys():
            print('\n')
            print('Interleaving Method: {} - Click Model: {}'.format(interleaving, click_model))
            print('----------| Min |---| Median |---| Max |')
            for b_id, bucket in final_table[interleaving][click_model].items():
                print('bucket{}---| {} |---| {} |---| {} |'.format(b_id+1, bucket['min N'],
                        bucket['median N'], bucket['max N']))
                print('-'*44)


if __name__ == '__main__':
    sample_sizes = determine_sample_sizes(n=20, k=100)
    final_table = get_final_table(sample_sizes)
    print_final_table(final_table)


if __name__ == '__test__':
    win_proportions = np.arange(0, 1, 0.1)
    for win_proportion in win_proportions:
        N = get_sample_size(win_proportion)
        print('proportion = {} \t N = {}'.format(win_proportion, N))
