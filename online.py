import numpy as np
import random
import string


def randbit():
    return random.random() > 0.5


class TeamDraftInterleaving:
    def __init__(self, production_ranking, experimental_ranking):
        self.prod_ranking = list(production_ranking)
        self.exp_ranking = list(experimental_ranking)

    @staticmethod
    def choose_from_A_and_delete_from_both(A, B, ranking_name):
        '''choose_from_A_and_delete_from_both'''
        doc = A.pop(0)
        try:
            i = B.index(doc)
            del B[i]
        except ValueError:
            pass
            # print('{} : doc {} is not in the other ranking'.format(ranking_name, doc))
        return doc

    def choose_from_prod(self):
        return self.choose_from_A_and_delete_from_both(self.prod_ranking, self.exp_ranking, 'Prod')

    def choose_from_exp(self):
        return self.choose_from_A_and_delete_from_both(self.exp_ranking, self.prod_ranking, 'Exp')

    def run(self):
        '''
            production_ranking = [a_1, a_2, ..., a_n]
            experimental_ranking = [b_1, b_2, ..., b_n]
            where a_i and b_i are document ids
            It is assumed that both rankings contain unique documents
        '''

        interleaved = []  # Interleaved ranking
        TeamA = []
        TeamB = []

        for interleaved_idx in range(len(self.prod_ranking) + len(self.exp_ranking)):
            if len(self.prod_ranking) == 0 and len(self.exp_ranking) == 0:
                break

            if len(self.exp_ranking) == 0:
                doc = self.choose_from_prod()
                winning_team = TeamA
            elif len(self.prod_ranking) == 0:
                doc = self.choose_from_exp()
                winning_team = TeamB
            elif len(TeamA) < len(TeamB):
                # Chosing from production ranking
                doc = self.choose_from_prod()
                winning_team = TeamA
            elif len(TeamB) < len(TeamA):
                doc = self.choose_from_exp()
                winning_team = TeamB
            else:
                if randbit():
                    doc = self.choose_from_prod()
                    winning_team = TeamA
                else:
                    doc = self.choose_from_exp()
                    winning_team = TeamB

            interleaved.append(doc)
            winning_team.append(doc)

        return interleaved, TeamA, TeamB


def generate_docs():
    letters = list(string.ascii_lowercase)
    docs = letters[:6]
    prod_ranking = random.sample(docs, len(docs))
    exp_ranking = random.sample(docs, len(docs))
    print('Ranking P:', prod_ranking)
    print('Ranking E:', exp_ranking)
    return prod_ranking, exp_ranking


def test_team_draft_interleaving(docs=None):
    docs = generate_docs() if docs is None else docs
    prod_ranking, exp_ranking = docs
    team_draft = TeamDraftInterleaving(prod_ranking, exp_ranking)
    interleaved_ranking, prod_docs, exp_docs = team_draft.run()
    print('Rankings Interleaved:', interleaved_ranking)
    print('Docs of P:', prod_docs)
    print('Docs of E:', exp_docs)


def softmax(x):
    e_x = np.exp(x)
    return e_x / np.sum(e_x)


class ProbabilisticInterleaving:
    def __init__(self, prod_ranking, exp_ranking, tau=3):
        self.prod_ranking = list(prod_ranking)
        self.prod_ranks = list(range(1, len(prod_ranking)+1))

        self.exp_ranking = list(exp_ranking)
        self.exp_ranks = list(range(1, len(exp_ranking)+1))
        self.tau = tau

        self.update_dists()

        self.interleaved = []

    def update_dists(self):
        self.prod_dist = self.probability_dist_over_ranks(self.prod_ranks)
        self.exp_dist = self.probability_dist_over_ranks(self.exp_ranks)

    def probability_dist_over_ranks(self, ranks):
        '''
        Parameters
        ----------
        ranking : list
            A list of documents.
        tau : int
            The second parameter.

        Returns
        -------
        numpy.ndarray
            probability distribution over the given ranking
        '''
        tau = self.tau
        ranks = np.array(ranks)
        inverse_ranks = (1 / ranks) ** tau
        p_dist = softmax(inverse_ranks)
        return p_dist

    def choose_from_A(self, A, p_A, ranks_A, B, p_B, ranks_B, A_name):
        doc = np.random.choice(A, p=p_A)
        i = A.index(doc)
        del A[i]
        del ranks_A[i]

        try:
            i = B.index(doc)
            del B[i]
            del ranks_B[i]
        except ValueError:
            pass
            # print('Doc {} was not in the {} ranking'.format(doc, A_name))

        self.update_dists()
        return doc

    def choose_from_prod(self):
        doc = self.choose_from_A(self.prod_ranking, self.prod_dist, self.prod_ranks,
                           self.exp_ranking, self.exp_dist, self.exp_ranks, 'Prod')
        return doc

    def choose_from_exp(self):
        doc = self.choose_from_A(self.exp_ranking, self.exp_dist, self.exp_ranks,
                           self.prod_ranking, self.prod_dist, self.prod_ranks, 'Exp')
        return doc

    def run(self):
        '''
            production_ranking = [a_1, a_2, ..., a_n]
            experimental_ranking = [b_1, b_2, ..., b_n]
            where a_i and b_i are document ids
            It is assumed that both rankings contain unique documents
        '''

        interleaved = []  # Interleaved ranking
        TeamA = []
        TeamB = []

        for interleaved_idx in range(len(self.prod_ranking)+len(self.exp_ranking)):
            if len(self.prod_ranking) == 0 and len(self.exp_ranking) == 0:
                break

            if len(self.exp_ranking) == 0:
                doc = self.choose_from_prod()
                winning_team = TeamA
            elif len(self.prod_ranking) == 0:
                doc = self.choose_from_exp()
                winning_team = TeamB
            elif randbit():
                doc = self.choose_from_prod()
                winning_team = TeamA
            else:
                doc = self.choose_from_exp()
                winning_team = TeamB

            interleaved.append(doc)
            winning_team.append(doc)

        return interleaved, TeamA, TeamB


def test_probabilistic():
    prod_ranking, exp_ranking = generate_docs()
    interleaving = ProbabilisticInterleaving(prod_ranking, exp_ranking)

    interleaved, prod_docs, exp_docs = interleaving.run()

    print('Rankings Interleaved:', interleaved)
    print('Docs of P:', prod_docs)
    print('Docs of E:', exp_docs)


if __name__ == '__main__':
    test_team_draft_interleaving()
    test_probabilistic()
