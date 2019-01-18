import numpy as np
import random
import copy
import string


def randbit():
    return random.random() > 0.5


def choose_from_A_and_delete_from_both(A, B, ranking_name):
    doc = A.pop(0)
    try:
        i = B.index(doc)
        del B[i]
    except ValueError:
        print('{} : doc {} is not in the other ranking'.format(ranking_name, doc))
    return doc


def team_draft_interleaving(production_ranking, experimental_ranking):
    '''
        production_ranking = [a_1, a_2, ..., a_n]
        experimental_ranking = [b_1, b_2, ..., b_n]
        where a_i and b_i are document ids
        It is assumed that both rankings contain unique documents
    '''

    # Copying, so we can modify these from now on
    production_ranking = copy.copy(production_ranking)
    experimental_ranking = copy.copy(experimental_ranking)

    I = []  # Interleaved ranking

    TeamA = []
    TeamB = []

    while len(production_ranking) > 0 or len(experimental_ranking) > 0:
        if (len(TeamA) < len(TeamB)) or (len(TeamA) == len(TeamB) and randbit()):
            # Chosing from production ranking
            doc = choose_from_A_and_delete_from_both(production_ranking, experimental_ranking, 'production')
            I.append(doc)
            TeamA.append(doc)
        else:
            doc = choose_from_A_and_delete_from_both(production_ranking, experimental_ranking, 'experimental')
            I.append(doc)
            TeamB.append(doc)

    return I, TeamA, TeamB


def test_team_draft_interleaving():
    letters = list(string.ascii_lowercase)
    docs = letters[:6]
    prod_ranking = random.sample(docs, len(docs))
    exp_ranking = random.sample(docs, len(docs))
    print('Ranking P:', prod_ranking)
    print('Ranking E:', exp_ranking)
    interleaved_ranking, prod_docs, exp_docs = team_draft_interleaving(prod_ranking, exp_ranking)
    print('Rankings Interleaved:', interleaved_ranking)
    print('Docs of P:', prod_docs)
    print('Docs of E:', exp_docs)


def probabilistic_interleaving():
    raise NotImplementedError


if __name__ == '__main__':
    test_team_draft_interleaving()
