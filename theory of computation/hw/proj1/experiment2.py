# from graphviz import Digraph

SPLIT = 'SPLIT'
MERGE = 'MERGE'
BEGIN = '^'
END = '$'
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

class State:
    cnt = 0
    def __init__(self, enter, to1 = None):
        self.enter = enter
        self.to1 = to1

        self.no = State.cnt
        State.cnt += 1


class Split(State):
    def __init__(self, to1, to2):
        super(Split, self).__init__(SPLIT, to1)
        self.to2 = to2

class Fragment:
    def __init__(self, begin, end = None):
        self.begin = begin
        self.end = begin
        if end:
            self.end = end
    # def debug(self):
    #     print("fragment {} ---> {}".format(self.begin.no, self.end.no))


class NFA:

    def __init__(self, alphabet = None):
        self.ALPHABET = alphabet if alphabet else ALPHABET
    def begin(self):
        return Fragment(State(BEGIN))
    def end(self):
        return Fragment(State(END))
    def letter(self, alpha):
        return Fragment(State(alpha))
    def joint(self, frag1, frag2):
        if frag2 is None:
            return frag1
        else:
            frag1.end.to1 = frag2.begin
            return Fragment(frag1.begin, frag2.end)
    def union(self, frag1, frag2):
        split = Split(frag1.begin, frag2.begin)
        merge = State(MERGE)
        frag1.end.to1 = merge
        frag2.end.to1 = merge
        return Fragment(split, merge)
    def star(self, frag1):
        split = Split(frag1.end.to1, frag1.begin)
        frag1.end.to1 = split
        return Fragment(split)
    def plus(self, frag1):
        # split = Split(frag1.end.to1, frag1.begin)
        # frag1.end.to1 = split
        # return Fragment(State(frag1.begin, split.to1))
        split = Split(frag1.end.to1, frag1.begin)
        frag1.end.to1 = split
        return Fragment(frag1.begin, split)
    def build(self, pattern, pre, frag):
        
        alpha = next(pattern)
        # print('nfa debug:', alpha)

        if alpha == '$' :
            return self.joint(frag, pre)
        # elif alpha == '^' :
        #     return self.joint(frag, pre)
        elif alpha in self.ALPHABET :
            return self.build(pattern, self.letter(alpha), self.joint(frag, pre))
        elif alpha == '|' :
            return self.union(self.joint(frag, pre), self.build(pattern, None, self.begin()))
        elif alpha == '*' :
            return self.build(pattern, self.star(pre), frag)
        elif alpha == '+' :
            return self.build(pattern, self.plus(pre), frag)
        elif alpha == '(' :
            return self.build(pattern, self.build(pattern, None, self.begin()), 
             self.joint(frag, pre))
        elif alpha == ')' :
            return self.joint(frag, pre)
        else :
            raise ValueError("Symbol {} cannot be recognized.".format(alpha))
    
    def create(self, pattern):
        return self.joint(self.build(pattern, None, self.begin()), self.end())



def print_nfa(state):

    read = set()
    nodes = list()
    edges = list()
    def report(state):
        if state.no in read:
            return
        
        read.add(state.no)

        print("state {} ({}) ---> {}".format(state.no, state.enter, "state "+str(state.to1.no) if state.to1 else "output"))
        if state.to1:
            edges.append([str(state.no), str(state.to1.no), state.enter])
            report(state.to1)
        else:
            nodes.append(str(state.no))

        if state.enter == 'SPLIT':
            print("state {} ({}) ---> {}".format(state.no, state.enter, "state "+str(state.to2.no) if state.to2 else "output"))
            if state.to2:
                edges.append([str(state.no), str(state.to2.no), state.enter])
                report(state.to2)
            else:
                nodes.append(str(state.no))
    
    report(state)
    return nodes, edges

# need graphviz package, run "pip install graphviz" ot get support
# def draw(nodes, edges):

#     f = Digraph(name='NFA')
#     f.attr('node', shape='doublecircle')
#     for node in nodes:
#         f.node(node)
#     f.attr('node', shape='circle')
#     for edge in edges:
#         f.edge(edge[0], edge[1], label=edge[2])

#     return f


def process(nfa, lang):

    curr = set()
    curr.add(nfa.begin)

    match = list()
    states = list()

    i = 0
    while i < len(lang):
        matched_letter = set()
        while curr:
            start = curr.pop()
            states.append(start.no)
            if start.enter == BEGIN or start.enter == MERGE:
                curr.add(start.to1)
            elif start.enter == SPLIT:
                curr.add(start.to1)
                curr.add(start.to2)
            elif start.enter == END:
                match.append(i)
            elif start.enter == lang[i]:
                matched_letter.add(start)
            else:
                continue
        if matched_letter:
            curr = set(x.to1 for x in matched_letter)
            i+=1
        else:
            break
    
    return match, states

# import os
# print(os.getcwd())
# set the regular expression here
with open("re.i") as file_object:
    pattern = file_object.read()
# pattern = '(a|cd)*b+a$'
pattern = iter(pattern)

nfa = NFA()
nfa = nfa.create(pattern)

# set the sentence to recognize here
with open("lang.i") as file_object:
    lang = file_object.read()
lang = lang + '\0'

# show the nfa diagram
print("the NFA diagram:")
nodes, edges = print_nfa(nfa.begin)

# show the process of language matching
match, states = process(nfa, lang)
print("language length: ", len(lang)-1, ", matched length: ", match[-1])
print("median state", states)

print(lang)

# img = draw(nodes, edges)
# print(img.source)
# img.view()