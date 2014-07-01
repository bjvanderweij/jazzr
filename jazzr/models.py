from pymuco.models import Model, FrequentistModel
from jazzr.representations import Symbol

class MetricalPerformanceModel(Model):

    def __init__(self, tolerance=0.01):
        self.tolerance = tolerance

    def input_probability(self, S, performance, v=False):

        metrical_onsets = S.metrical_onsets()

        # Disallow symbols that only contain rests
        if len(metrical_onsets) == 0 and len(S.flatten()) > 1:
            return 0.0

        # We need more than one ioi to know anything
        if len(performance) <= 2:
            return 1.0

        position = 0.0
        onset_pointer = 0
        metrical_iois = [b-a for (a,b) in zip(metrical_onsets[:-1], metrical_onsets[1:])]
        performance_iois = [b-a for (a,b) in zip(performance[:-1], performance[1:])]

        if v:
            print S.flatten()
            print metrical_onsets
            print performance

        previous_crotchet = None

        for m, p in zip(metrical_iois, performance_iois):
            crotchet = p / float(4.0 * m)
            if previous_crotchet:
                if abs(crotchet - previous_crotchet) > self.tolerance * previous_crotchet:
                    return 0.0
            previous_crotchet = crotchet


        return 1.0

class RatioPerformanceModel(Model):

    def __init__(self):
        pass

    def performance_observations(self, onsets):
        if len(onsets) <= 2: return []

        iois = [b-a for (a,b) in zip(onsets[:-1], onsets[1:])]
        ratios = [b/a for (a,b) in zip(iois[:-1], iois[1:])]
        return ratios

    def observation_categories(self, S):
        # Extract all observed ratios in sets of two iois

        metrical_onsets = S.metrical_onsets()
        if len(metrical_onsets) <= 2: return []

        metrical_iois = [b-a for (a,b) in zip(metrical_onsets[:-1], metrical_onsets[1:])]
        ratios = [b/a for (a,b) in zip(metrical_iois[:-1], metrical_iois[1:])]

        if self.v:
            print S.flatten()
            print metrical_onsets
            print performance

        return ratios

    def probability(category, performance):
        log_diff = log(category) - log(performace)
        mean, std = self.parameters[category]

    def input_probability(self, S, onsets):
        p_obs = self.performance_observations(onsets)
        s_obs = self.observation_categories(S)
        for category, performance in zip(s_obs, p_obs):
            self.probability(category, performance)

class OneBarModel(Model):
    """
    This model assumes that a whole unit (1) corresponds to one bar
    """

    def input_probability(self, S, performance, threshold=0.01):
        metrical_onsets = S.metrical_onsets()
        print metrical_onsets, performance
        print [abs(onset - metrical_onset) < threshold for onset, metrical_onset in zip(performance, metrical_onsets)]
        return 1.0 if all([abs(onset - metrical_onset) < threshold for onset, metrical_onset in zip(performance, metrical_onsets)]) else 0.0

class PCFG(FrequentistModel):

    def observations(self, input):
        observations = []
        if not input.symbol in Symbol.TERMINALS:
            if not input.symbol[0] == 'm':
                observations += [(input.symbol, tuple([c.symbol for c in input.children]))] 
            from operator import add
            observations += reduce(add, [self.observations(c) for c in input.children])
        return observations

