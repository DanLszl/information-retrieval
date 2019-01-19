from pprint import pprint

from collections import namedtuple
from itertools import permutations
from collections import defaultdict

from offline import create_positive_pairs, create_buckets, allocate_pairs_to_buckets

RankingPair = namedtuple('RankingPair', ['E', 'P', 'rel_E', 'rel_P'])


class RankingPairs:
    def __init__(self, k):
        '''k: cutoff'''
        self.ranking1 = tuple(range(k))
        all_ids = list(range(2*k))
        self.rankings2 = list(permutations(all_ids, k))
        self.k = k
        self.masks = []

    def filter(self, ranking1, ranking2, relevances1, relevances2):
        mask = []
        for doc1, rel1 in zip(ranking1, relevances1):
            for doc2, rel2 in zip(ranking2, relevances2):
                if doc1 == doc2 and rel1 != rel2:
                    return False
                elif doc1 == doc2:
                    mask.append(doc1)
                else:
                    mask.append(-1)

        if mask in self.masks:
            return False
        else:
            self.masks.append(mask)
            return True

    def generate_valid_rankings(self, relevance_pair):
        self.masks = []
        rel_B, rel_A = relevance_pair

        if len(rel_A) != self.k or len(rel_B) != self.k:
            raise ValueError(
                'The relevance lists should have a length of {}'.format(self.k))
        else:
            ranking1 = self.ranking1
            valid = [RankingPair(ranking2, ranking1, rel_B, rel_A)
                     for ranking2 in self.rankings2
                     if self.filter(ranking1, ranking2, rel_A, rel_B)]
            return valid


def convert_pairs_of_relevances_to_possible_rankings(pairs):
    k = len(pairs[0][0])
    ranking_pairs = RankingPairs(k)
    result = {tuple(pair): {'rankings': ranking_pairs.generate_valid_rankings(
        pair), 'd_ERR': d_ERR} for *pair, d_ERR in pairs}
    return result


def allocate_to_buckets(relevances, buckets):
    for bucket in buckets.values():
        bucket['relevances'] = {}

    for rel_pair, data in relevances.items():
        delta_err = data['d_ERR']
        for bucket in buckets.values():
            interval = bucket['range']
            if interval[0] <= delta_err < interval[1]:
                bucket['relevances'][rel_pair] = data
                break

    return buckets


if __name__ == '__main__':
    pairs = create_positive_pairs()
    rankings = convert_pairs_of_relevances_to_possible_rankings(pairs)
    buckets = create_buckets()
    # allocate_pairs_to_buckets(pairs, buckets)
    allocate_to_buckets(rankings, buckets)
    pprint(buckets)
