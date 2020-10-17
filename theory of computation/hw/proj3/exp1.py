L = -1
R = 1

NORMAL_STATE = list('123456789')
MID_STATE = list('ABCDEFGHI')
BASE_ASCII = ord('A') - 1

class State:
    def __init__(self, no):
        self.no = no
        
states = [State('0'), State('L'), State('S'), State('W')]
state_ac = State('AC')
state_rj = State('RJ')
alphabet = ['#']


class TuringMachine:
    def __init__(self, states, state_ac, state_rj, alphabet):
        self.states = states
        self.state_ac = state_ac
        self.state_rj = state_rj
        self.alphabet = alphabet
        self.table = dict()
        for state in states:
            self.table[state.no] = dict()
            for alpha in alphabet:
                self.table[state.no][alpha] = [state_rj.no, alpha, R]
    def make_trans(self):
        self.table['0']['#'] = ['S', '#', R]
        for i in range(1, len(self.alphabet)):
            for j in range(1, len(self.alphabet)):
                if self.alphabet[i] <= self.alphabet[j]:
                    x = self.alphabet[i]
                    y = self.alphabet[j]
                    self.table[x][y] = [y, y, R]
            
                    self.table[y][x] = [get_restate(x), y, L]
                    self.table[get_restate(x)][y] = [x, x, R]
        for i in range(1, len(self.alphabet)):
            x = self.alphabet[i]
            self.table[x]['#'] = ['W', x, L]
        for i in range(0, len(self.alphabet) ):
            x = self.alphabet[i]
            self.table['W'][x] = ['L', '#', L]
        self.table['L']['#'] = ['S', '#', R]
        self.table['S']['#'] = ['AC', '#', R]
        for i in range(1, len(self.alphabet)):
            x = self.alphabet[i]
            self.table['L'][x] = ['L', x, L]
            self.table['S'][x] = [x, x, R]
        
    def transform(self, state, entry):
        return self.table[state.no][entry]


def get_restate(x):
    if x in NORMAL_STATE:
        return chr(BASE_ASCII + int(x))
    if x in MID_STATE:
        return str(ord(x)-BASE_ASCII)
    return -1

def configuration(pos, state, tape):
    for i in range(len(tape)):
        if pos == i:
            if state.no == 'AC' or state.no == 'RJ':
                print(state.no, end=' ')
            elif state.no in NORMAL_STATE:
                print('Q{}'.format(state.no), end=' ')
            else:
                print('Q{}'.format(str.lower(state.no)), end=' ')
        print(tape[i], end=' ')
    print('')



input_str = "9 8 7 6 5 4 3 2 1"



input_str_list = input_str.strip().split(' ')
tape = ['#']
for s in input_str_list:
    tape.append(s)
    alphabet.append(s)
    states.append(State(s))
    states.append(State( get_restate(s) ))
tape.append('#')



tm = TuringMachine(states, state_ac, state_rj, alphabet)
tm.make_trans()

stt = State('0')
pos = 0
while stt.no != state_ac.no and stt.no != state_rj.no:
    configuration(pos, stt, tape)
    to, over, shift = tm.transform(stt, tape[pos])
    tape[pos] = over
    stt = State(to)
    pos += shift
configuration(pos, stt, tape)