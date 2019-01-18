from offline import create_positive_pairs, create_buckets, allocate_pairs_to_buckets
from pprint import pprint
import string

from itertools import permutations


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
        flag = True
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
        rel_A, rel_B = relevance_pair

        if len(rel_A) != self.k or len(rel_B) != self.k:
            raise ValueError('The relevance lists should have a length of {}'.format(self.k))
        else:
            ranking1 = self.ranking1
            valid = [(ranking1, ranking2)
                     for ranking2 in self.rankings2
                     if self.filter(ranking1, ranking2, rel_A, rel_B)]
            return valid


def convert_pairs_of_relevances_to_possible_rankings(pairs):
    # pprint(pairs)
    k = len(pairs[0][0])
    ranking_pairs = RankingPairs(k)
    for *pair, _ in pairs:
        print(pair)
    result = [ranking_pairs.generate_valid_rankings(pair) for *pair, _ in pairs]
    # print('result:')
    # pprint(result)
    return result


if __name__ == '__main__':
    pairs = create_positive_pairs()
    rankings = convert_pairs_of_relevances_to_possible_rankings(pairs)
    #pprint(rankings)

    for pair, ranking in zip(pairs, rankings):
        pprint((pair, ranking))

    # print(len(pairs))
    # print(len(rankings))

    buckets = create_buckets()

    # pprint(allocate_pairs_to_buckets(pairs, buckets))
