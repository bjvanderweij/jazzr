from pymuco.representations import Representation

class Symbol(Representation):

    REST = ('rest', )
    ONSET = ('on', )
    TERMINALS = [REST, ONSET]
    BAR_SYMBOLS = [(4, 4), (3, 4), (6, 8)]

    def __init__(self, symbol, children=[]):
        self.children = children
        self.symbol = symbol

    def __str__(self):
        return '%s (%s)' % (self.symbol, ', '.join([str(s) for s in self.children]))


    def metrical_onsets(self):
        units = self.flatten()
        metrical_onsets = []
        position = 0.0
        for (type, (nom, denom)) in units:
            if type == self.ONSET:
                metrical_onsets.append(position)
            position += nom / float(denom)
        return metrical_onsets

    def _metrical_onsets(self, position=0, duration=None):
        """
        Do a depth first tree traversal and convert the tree to a flat list of metrical onset times (units=whole notes).
        """
        if self.symbol in self.TERMINALS:
            if self.symbol == self.ONSET:
                return [position]
            else: 
                return []

        if self.symbol[0] != 'm':
            num, denom = self.symbol
            if duration == None:
                duration = num / float(denom)

            onsets = []
            child_duration = duration / float(len(self.children))
            for i, child in enumerate(self.children):
                onsets += child.metrical_onsets(position=position+i*child_duration, duration=child_duration)
            return onsets

        else:
            onsets = []
            for i, child in enumerate(self.children):
                c_nom, c_denum = self.children[i].symbol
                child_duration = c_nom / float(c_denum)
                onsets += child.metrical_onsets(position=position, duration=child_duration)
                position += child_duration
            return onsets

    
    def flatten(self, parent=None):
        """
        Do a depth first tree traversal and convert the tree to a flat list of metrical units.
        """
        if self.symbol in self.TERMINALS:
            if parent:
                return [(self.symbol, parent.symbol)]

        l = []
        for child in self.children:
            l += child.flatten(self)
        return l

    def music21(self, root=False):
        if root:
            stream = Stream()
            # Add key signature
            # Add time signature
            # Add bars
            stream += [child.music21 for child in self.children]
            return stream
        elif not self.symbol in TERMINALS:
            stream = []
            if self.symbol in BAR_SYMBOLS:
                stream = Bar()
            for child in self.children:
                stream += child.music21
            return stream
        elif self.symbol == REST:
            return Rest(duration=self.symbol[1] / self.symbol[2])


REST_SYMBOL = Symbol(('rest', ))
ONSET_SYMBOL = Symbol(('on', ))
METRICAL_REST_SYMBOL = lambda unit: Symbol(unit, children=[Symbol(('rest', ))]) 
METRICAL_ONSET_SYMBOL = lambda unit: Symbol(unit, children=[Symbol(('on', ))]) 

