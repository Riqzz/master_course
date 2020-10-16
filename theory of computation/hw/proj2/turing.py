ACCEPT = 0
REJECT = -1

L = -1
R = 1

class State:
    def __init__(self, no, trans):
        self.no = no
        self.trans = trans
    # def to(self, entry):
    #     return self.trans[entry]

class TuringMachine:
    def __init__(self, string):
        self.acc = State(ACCEPT, None)
        self.rej = State(REJECT, None)

        self.s1 = State(1, {'a':['#', R, 2], 'b':['b', R, REJECT], 'x':['x', R, REJECT], '#':['#', R, REJECT]})
        self.s2 = State(2, {'a':['a', R, 2], 'b':['x', R, 3], 'x':['x', R, 2], '#':['#', L, 5]})
        self.s3 = State(3, {'a':['x', L, 4], 'b':['b', R, 3], 'x':['x', R, 3], '#':['#', R, REJECT]})
        self.s4 = State(4, {'a':['a', R, 2], 'b':['b', L, 4], 'x':['x', L, 4], '#':['#', R, 2]})
        self.s5 = State(5, {'a':['a', L, 5], 'b':['b', R, REJECT], 'x':['x', L, 5], '#':['#', R, 6]})
        self.s5 = State(5, {'a':['a', L, 5], 'b':['b', R, REJECT], 'x':['x', L, 6], '#':['#', R, REJECT]})
        self.s6 = State(6, {'a':['x', R, 7], 'b':['b', R, REJECT], 'x':['x', L, 6], '#':['#', R, 8]})
        self.s7 = State(7, {'a':['x', L, 6], 'b':['b', R, REJECT], 'x':['x', R, 7], '#':['#', R, REJECT]})
        self.s8 = State(8, {'a':['x', R, 9], 'b':['b', R, REJECT], 'x':['x', R, 8], '#':['#', R, REJECT]})
        self.s9 = State(9, {'a':['a', R, REJECT], 'b':['b', R, REJECT], 'x':['x', R, REJECT], '#':['#', R, ACCEPT]})

        self.states = [self.acc, self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9, self.rej]
        self.string = list(string)
        # for i in range(0, len(string)):
        #     self.string.append('#')
        self.string.append('#')

    def to(self, state, entry):
        # print(state.no, entry)
        # print(state.trans[entry])
        return state.trans[entry]

    def check(self, string, qno, pos):
        flag = False
        for i in range(0, len(string)):
            if pos == i:
                flag = True
                if qno == 0:
                    print('ACC', end=' ')
                elif qno == -1:
                    print('REJ', end=' ')
                else:
                    print('q'+str(qno), end=' ')
            print(string[i], end=' ')
        if not flag:
            if qno == 0:
                print('AC', end=' ')
            elif qno == -1:
                print('RJ', end=' ')
        print('')

    def process(self):
        state = self.s1
        string = self.string
        tmp = list()
        tmp.append(state.no)
        slot = 0
        self.check(string, state.no, slot)
        while state.no != ACCEPT and state.no != REJECT:
            [rewrite, shift, nextstate] = self.to(state, string[slot])
            # print('debug', state.no, [rewrite, shift, nextstate], slot + shift)
            state = self.states[nextstate]
            string[slot] = rewrite
            # print(string)
            slot = slot + shift
            tmp.append(state.no)
            self.check(string, state.no, slot)
        # print(tmp)
        return tmp


positive = ['abaa', 'aabaaa', 'abbaaa', 'aabbaaaa', 'aaabbaaaaa', 'aaabbbaaaaaa']
negative = ['aaaa', 'aaba', 'bbaa', 'bbbb', 'ababa']
for item in negative:
    t = TuringMachine(item)
    print(t.process()[-1])


# the following code is used for draw a diagram

for q in t.states:
    if q.no == 0 or q.no == -1:
        continue

    dic = {-1:'L', 1:'R'}
    tmp = ['a', 'b', 'x', '#']
    for key in tmp:
        item = q.trans[key]
        tono = 'q' + str(item[2])
        if item[2] == 0:
            tono = 'AC'
        if item[2] == -1:
            tono = 'RJ'
        s = "{}->{}".format( key, item[0]+','+dic[item[1]] if key!=item[0] else dic[item[1]])
        # s = "{}→{}".format( key, item[0]+','+dic[item[1]] if key!=item[0] else dic[item[1]])
        print( 'q'+str(q.no), '->', tono, '[ label = "{}" ];'.format(s) )

# digraph G {
# node [shape = circle]; 
# AC q1 q2 q3 q4 q5 q6 q7 q8 q9 RJ
# q1 -> q2 [ label = "a,#,R" ];
# q1 -> RJ [ label = "b,R" ];
# q1 -> RJ [ label = "x,R" ];
# q1 -> RJ [ label = "#,R" ];
# q2 -> q2 [ label = "a,R" ];
# q2 -> q3 [ label = "b,x,R" ];
# q2 -> q2 [ label = "x,R" ];
# q2 -> q5 [ label = "#,L" ];
# q3 -> q4 [ label = "a,x,L" ];
# q3 -> q3 [ label = "b,R" ];
# q3 -> q3 [ label = "x,R" ];
# q3 -> RJ [ label = "#,R" ];
# q4 -> q2 [ label = "a,R" ];
# q4 -> q4 [ label = "b,L" ];
# q4 -> q4 [ label = "x,L" ];
# q4 -> q2 [ label = "#,R" ];
# q5 -> q5 [ label = "a,L" ];
# q5 -> RJ [ label = "b,R" ];
# q5 -> q6 [ label = "x,L" ];
# q5 -> RJ [ label = "#,R" ];
# q6 -> q7 [ label = "a,x,R" ];
# q6 -> RJ [ label = "b,R" ];
# q6 -> q6 [ label = "x,L" ];
# q6 -> q8 [ label = "#,R" ];
# q7 -> q6 [ label = "a,x,L" ];
# q7 -> RJ [ label = "b,R" ];
# q7 -> q7 [ label = "x,R" ];
# q7 -> RJ [ label = "#,R" ];
# q8 -> q9 [ label = "a,x,R" ];
# q8 -> RJ [ label = "b,R" ];
# q8 -> q8 [ label = "x,R" ];
# q8 -> RJ [ label = "#,R" ];
# q9 -> RJ [ label = "a,R" ];
# q9 -> RJ [ label = "b,R" ];
# q9 -> RJ [ label = "x,R" ];
# q9 -> AC [ label = "#,R" ];
# }