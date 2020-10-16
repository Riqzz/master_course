import copy

cfg = '''

S -> ASA | aB
A -> B | S
B -> b | ε 

'''

terminals = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
variables = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']

class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

# step 0: pre-process cfg string
spls = cfg.split('\n')
cfg = list()
dlt = list()
for spl in spls:
    if len(spl) != 0:
        brk = spl.split('->')
        if len(brk) == 2:
            left = brk[0].strip()
            rights = brk[1].split('|')

            # the judgement here is used to remove productions that only generate empty terminal
            if len(rights) == 1 and rights[0].strip() == 'ε':
                dlt.append(left)
                # print('debug ', left)
                continue

            for right in rights:
                cfg.append(Pair(left, right.strip()))
for d in dlt:
    for pr in cfg:
        if d in pr.right:
            pr.right = pr.right.replace(d, '')

tmpcfg = list()
for pr in cfg:
    if len(pr.right) != 0:
        tmpcfg.append(pr)
cfg = tmpcfg

# step 1
cfg.append(Pair('S0', 'S'))

# step 2
def is_right_empty(pair):
    if pair.right == 'ε':
        return True
    else:
        return False

def not_any_empty(cfg):
    for p in len(cfg):
        if is_right_empty(cfg[p]):
            return p
    return -1

pos = not_any_empty(cfg)
while pos != -1:
    # same left, other right(maybe no use)
    others = list()
    # whose right contains the left, need to make up
    contains = list()

    for pr in cfg:
        if pr.left == cfg[pos].left and pr.right != 'ε':
            others.append(pr.right)
        if cfg[pos].left in pr.right:
            contains.append(pr)
    
    for con in contains:
        l = cfg[pos].left
        r = cfg[pos].right
        for i in len(r):
            if l == r[i]:
                


    


for x in cfg:
    print(x.left, x.right)

