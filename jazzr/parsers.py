import sys, math
from jazzr.representations import Symbol

class ChartParser(object):

    def __init__(self, grammar, expression_model=None, rhythm_model=None, beam=0.5, n=-1, verbose=False):
        self.beam = beam
        self.n = n
        self.expression_model=expression_model
        self.rhythm_model= rhythm_model
        self.corpus = False
        self.verbose=verbose
        self.grammar = grammar

    def close(self, symbols, performance):
        cell = []
        unseen = []
        while True:

            p = 1.0

            # Generate hypotheses
            inp = tuple([s.symbol for s in symbols])
            hypotheses = [s(symbols) for s in self.grammar.get(inp, [])]
            for h in hypotheses:
                #likelihood = self.expression_model.input_probability(h)
                #prior = self.rhythm_model.input_probability(h)
                #if likelihood > 0.0:
                #    # Per item likelihood
                #    if math.exp(math.log(likelihood) / float(n)) > self.beam:
                #        unseen += [h]
                likelihood = self.expression_model.input_probability(h, performance)
                if likelihood > 0.0:
                    unseen += [h]
            if unseen == []:
                break
            symbols = [unseen.pop()]
            cell += symbols
        return cell

    def parse(self, N, performance=[]):

        n = len(N)
        t = {}

        # Iterate over rows
        for j in range(1, n+1):

            # Fill diagonal cells
            t[j-1, j] = [N[j-1]] + self.close([N[j-1]], performance[j-1:j])

            # Iterate over columns
            for i in range(j-2, -1, -1):
                cell = []

                for k in range(i+1, j):
                    for B in t[i,k]:
                        for C in t[k,j]:
                            cell += self.close([B,C], performance[i:j])

                if self.n > 0 and len(cell) > self.n:
                    if self.rhythm_model:
                        # Sort by posterior probability
                        cell = [item for item in sorted(cell, key=lambda x: x.posterior, reverse=True)][:self.n]
                    else:
                        sortedcell = sorted(cell, key=lambda x: x.depth)
                        if abs(i-j) > 1:
                            newcell = []
                            firstdepth = sortedcell[0].depth
                            for c in sortedcell:
                                if c.depth - firstdepth > 0:
                                    break
                                newcell.append(c)
                            cell = newcell
                        else:
                            cell = [item for item in sortedcell][:self.n]
                t[i,j] = cell
                if self.verbose:
                    print '[%d, %d]: %d hypotheses' % (i, j, len(cell))
        return t

