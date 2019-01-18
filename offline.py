import pprint as pp

def calculate_prob_relevance(grade, max_grade=1):
    return (2 ** grade - 1) / (2 ** max_grade)


def calculate_err(ranking_list):
    err = 0
    for r_index, rank in enumerate(ranking_list):
        i_prod = 1
        for i_index in range(r_index):
            i_prod *= (1 - calculate_prob_relevance(ranking_list[i_index]))
        err += 1 / (r_index + 1) * i_prod * calculate_prob_relevance(rank)

    return err


def calculate_delta_err(pair):
    return calculate_err(pair[0]) - calculate_err(pair[1])


def create_positive_pairs(num_labels=2):
    labels = [label for label in range(num_labels)]
    ranks = [[x, y, z] for x in labels for y in labels for z in labels]

    return [(e, p, calculate_delta_err((e, p)))
            for e in ranks
            for p in ranks
            if calculate_delta_err((e, p)) > 0]


def create_buckets(n_buckets=10, offset=0.05):
    buckets = dict()
    for bucket_id in range(n_buckets):
        buckets[bucket_id] = dict()
        buckets[bucket_id]['range'] = [round(1/10*bucket_id, 2), round(1/n_buckets*(bucket_id + 1), 2)]
        buckets[bucket_id]['ranked_lists'] = []

    # offset first and last bucket
    buckets[0]['range'][0] = offset
    buckets[n_buckets - 1]['range'][1] -= offset

    return buckets


def allocate_pairs_to_buckets(pairs, buckets):
    for pair in pairs:
        delta_err = pair[2]
        for bucket_id in buckets.keys():
            min_range, max_range = buckets[bucket_id]['range']
            if delta_err >= min_range and delta_err < max_range:
                buckets[bucket_id]['ranked_lists'].append(pair)
                break

    return buckets


if __name__ == "__main__":
    pairs = create_positive_pairs()
    buckets = create_buckets()
    pp.pprint(allocate_pairs_to_buckets(pairs, buckets))













