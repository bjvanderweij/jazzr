from jazzr.representations import Symbol

# A lambda abstracted symbol with unbound children
S = lambda symbol: lambda children: Symbol(symbol, children=children)

# A lambda abstracted symbol with unbound children to which a rest will be added on the left hand side
RS = lambda symbol, child_symbol: lambda children: Symbol(symbol, children=[Symbol(child_symbol, children=[Symbol(('rest',))] )] + children)

# Single onset triplet, possibility 1: * o * (rest onset rest)
SOT1 = lambda symbol, child_symbol: lambda children:\
    Symbol(symbol, children=\
        [Symbol(child_symbol, children=[Symbol(('rest',))] )] + \
        children + \
        [Symbol(child_symbol, children=[Symbol(('rest',))] )]
    )

# Single onset triplet, possibility 2: * * o (rest rest onset)
SOT2 = lambda symbol, child_symbol: lambda children: Symbol(symbol, children=2 * [Symbol(child_symbol, children=[Symbol(('rest',))])] + children)

# Dual onset triplet, possibility 1: o * o (onset rest onset)
DOT1 = lambda symbol, child_symbol: lambda children:\
    Symbol(symbol, children=[
        children[0],
        Symbol(child_symbol, children=[Symbol(('rest',))]),
        children[1]
    ])
# Dual onset triplet, possibility 2: o o * (onset onset rest)
DOT2 = lambda symbol, child_symbol: lambda children:\
    Symbol(symbol, children=children + [Symbol(child_symbol, children=[Symbol(('rest',))])])
# Dual onset triplet, possibility 3: * o o (rest onset onset)
DOT3 = lambda symbol, child_symbol: lambda children:\
    Symbol(symbol, children=[Symbol(child_symbol, children=[Symbol(('rest',))])] + children)

# A lambda abstracted symbol where the resulting symbol will contain a concatenation of the input symbol's children
from operator import add
MS = lambda symbol: lambda children: Symbol(symbol, children=reduce(add, [c.children for c in children]))

def apply_rule(input, grammar):
    symbols = tuple([i.symbol for i in input])
    if symbols in grammar:
        return [s(input) for s in grammar[symbols]]
    else:
        print symbols

fourfour_single = {
        ((4, 4), ):     [S(('m', 4, 4))],
        ((2, 4), ):     [RS((4, 4), (2, 4)), SOT1((4, 4), (2, 4)), SOT2((4, 4), (2, 4))],
        ((1, 4), ):     [RS((2, 4), (1, 4)), SOT1((2, 4), (1, 4)), SOT2((2, 4), (1, 4))],
        ((1, 8), ):     [RS((1, 4), (1, 8)), SOT1((1, 4), (1, 8)), SOT2((1, 4), (1, 8))],
        ((1, 16), ):    [RS((1, 8), (1, 16)), SOT1((1, 8), (1, 16)), SOT2((1, 8), (1, 16))],
        (('on', ), ):   [S(s) for s in [(4, 4), (2, 4), (1, 4), (1, 8), (1, 16)]],
        (('rest', ), ): [S(s) for s in [(4, 4), (2, 4), (1, 4), (1, 8), (1, 16)]],
        ((1, 16), (1, 16))     :[S((1,8)), DOT1((1, 8), (1, 16)), DOT2((1, 8), (1, 16)), DOT3((1, 8), (1, 16))],
        ((1, 8), (1, 8))     :[S((1,4)), DOT1((1, 4), (1, 8)), DOT2((1, 4), (1, 8)), DOT3((1, 4), (1, 8))],
        ((1, 4), (1, 4))     :[S((1,2)), DOT1((1, 2), (1, 4)), DOT2((1, 2), (1, 4)), DOT3((1, 2), (1, 4))],
        ((2, 4), (2, 4))        :[S((4,4))],
        ((1, 16), (1, 16), (1, 16))     :[S((1,8))],
        ((1, 8), (1, 8), (1, 8))     :[S((1,4))],
        ((1, 4), (1, 4), (1, 4))     :[S((2,4))],
}
fourfour = {
        ((4, 4), ): [S(('m', 4, 4))],
        (('m', 4, 4), ('m', 4, 4), ): [MS(('m', 4, 4))],
        ((2, 4), ): [RS((4, 4), (2, 4))],
        ((1, 4), ): [RS((2, 4), (1, 4))],
        ((1, 8), ): [RS((1, 4), (1, 8))],
        ((1, 16), ): [RS((1, 8), (1, 16))],
        (('on', ), ): [S(s) for s in [(4, 4), (2, 4), (1, 4), (1, 8), (1, 16)]],
        (('rest', ), ): [S(s) for s in [(4, 4), (2, 4), (1, 4), (1, 8), (1, 16)]],
        ((1, 16), (1, 16))      :[S(s) for s in [(1,8)]],
        ((1, 8), (1, 8))        :[S(s) for s in [(1,4)]],
        ((1, 4), (1, 4))        :[S(s) for s in [(2,4)]],
        ((2, 4), (2, 4))        :[S(s) for s in [(4,4)]],
}
threefour = {
        ((3, 4), ): [S(('m', 3, 4))],
        (('m', 3, 4), ('m', 3, 4), ): [MS(('m', 3, 4))],
        ((1, 4), ): [RS((2, 4), (1, 4))],
        ((1, 8), ): [RS((1, 4), (1, 8))],
        ((1, 16), ): [RS((1, 8), (1, 16))],
        (('on', ), ): [S(s) for s in [(3, 4), (2, 4), (1, 4), (1, 8), (1, 16)]],
        (('rest', ), ): [S(s) for s in [(3, 4), (2, 4), (1, 4), (1, 8), (1, 16)]],
        ((1, 16), (1, 16))      :[S(s) for s in [(1,8)]],
        ((1, 8), (1, 8))        :[S(s) for s in [(1,4)]],
        ((1, 4), (1, 4), (1, 4)):[S(s) for s in [(3,4)]],
}
sixeight = {
        ((4, 4), ): [S(('m', 4, 4))],
        (('m', 4, 4), ('m', 4, 4), ): [MS(('m', 4, 4))],
        ((2, 4), ): [RS((4, 4), (2, 4))],
        ((1, 4), ): [RS((2, 4), (1, 4))],
        ((1, 8), ): [RS((1, 4), (1, 8))],
        ((1, 16), ): [RS((1, 8), (1, 16))],
        (('on', ), ): [S(s) for s in [(4, 4), (2, 4), (1, 4), (1, 8), (1, 16)]],
        (('rest', ), ): [S(s) for s in [(4, 4), (2, 4), (1, 4), (1, 8), (1, 16)]],
        ((1, 16), (1, 16))      :[S(s) for s in [(1,8)]],
        ((1, 8), (1, 8))        :[S(s) for s in [(1,4)]],
        ((1, 4), (1, 4), (1, 4)):[S(s) for s in [(3,4)]],
}
full = {
        # Rules for concatenating measures
        ((4, 4), ): [S(('m', 4, 4))],
        ((3, 4), ): [S(('m', 3, 4))],
        ((6, 8), ): [S(('m', 6, 8))],
        (('m', 4, 4), ('m', 4, 4), ): [MS(('m', 4, 4))],
        (('m', 4, 4), ('m', 3, 4), ): [MS(('m', 3, 4))],
        (('m', 4, 4), ('m', 6, 8), ): [MS(('m', 6, 8))],
        (('m', 3, 4), ('m', 4, 4), ): [MS(('m', 4, 4))],
        (('m', 3, 4), ('m', 3, 4), ): [MS(('m', 3, 4))],
        (('m', 3, 4), ('m', 6, 8), ): [MS(('m', 6, 8))],
        (('m', 6, 8), ('m', 4, 4), ): [MS(('m', 4, 4))],
        (('m', 6, 8), ('m', 3, 4), ): [MS(('m', 3, 4))],
        (('m', 6, 8), ('m', 6, 8), ): [MS(('m', 6, 8))],
        # Tie/Rest adding rules
        ((2, 4), ): [RS((4, 4), (2, 4))],
        ((1, 4), ): [RS((2, 4), (1, 4))],
        ((1, 8), ): [RS((1, 4), (1, 8))],
        ((1, 16), ): [RS((1, 8), (1, 16))],
        # Terminals
        (('on', ), ): [S(s) for s in [(4, 4), (3, 4), (2, 4), (1, 4), (6, 8), (3, 8), (1, 8), (1, 16)]],
        (('rest', ), ): [S(s) for s in [(4, 4), (3, 4), (2, 4), (1, 4), (6, 8), (3, 8), (1, 8), (1, 16)]],
        # 4/4
        ((1, 16), (1, 16))      :[S(s) for s in [(1,8)]],
        ((1, 8), (1, 8))        :[S(s) for s in [(1,4)]],
        ((1, 4), (1, 4))        :[S(s) for s in [(2,4)]],
        ((2, 4), (2, 4))        :[S(s) for s in [(4,4)]],
        # 3/4
        ((1, 4), (1, 4), (1, 4)):[S(s) for s in [(3,4)]],
        # 6/8
        ((1, 8), (1, 8), (1, 8)):[S(s) for s in [(3,8)]],
        ((3, 8), (3, 8))        :[S(s) for s in [(6,8)]],
}
