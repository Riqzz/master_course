import copy

class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class PairSet:
    def __init__(self, pair_list=None):
        self.data = list()
        if pair_list:
            for p in pair_list:
                self._add(p)
            
    def _add(self, pair):
#         print('debug', self._is_in(pair))
        if not self._is_in(pair):
            self.data.append(pair)
    def _equal(self, p1, p2):
        if p1.left == p2.left and len(p1.right) == len(p2.right):
            rlen = len(p1.right)
            flag = True
            for i in range(0, rlen):
                if p1.right[i] != p2.right[i]:
                    return False
            if flag:
                return True
        return False
            
    def _is_in(self, pair):
        for p in self.data:
            if p.left == pair.left and len(p.right) == len(pair.right):
                rlen = len(p.right)
                flag = True
                for i in range(0, rlen):
                    if p.right[i] != pair.right[i]:
                        flag = False
                        break
#                 print('flg', flag)
                if flag: # same left and right
                    return True
        return False
    
    def _del(self, pair):
        for p in self.data:
            if self._equal(p, pair):
                self.data.remove(p)
                break
            
    @classmethod
    def is_equal(cls, pair1, pair2):
        return self._equal(pair1, pair2)
    
    def add(self, pair):
        self._add(pair)
    
    def delete(self, pair):
        self._del(pair)
    
    def is_in_set(self, pair):
        return self._is_in(pair)
        
    def print_all(self):
        for d in self.data:
            print(d.left, '->',d.right)
                    

cfg = '''

S -> ASA | aB
A -> B | S
B -> b | ε 

'''

print('-'*27 + "context free grammar" + '-'*27, cfg)

terminals = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']

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
                cfg.append(Pair(left, list(right.strip())) )
for d in dlt:
    for pr in cfg:
        if d in pr.right:
            pr.right.remove(d)
#             pr.right = pr.right.replace(d, '')

tmpcfg = list()
for pr in cfg:
    if len(pr.right) != 0:
        tmpcfg.append(pr)
        
cfg = PairSet(tmpcfg)

# step 1: add S0 -> S
cfg.add(Pair('S0', ['S']))

print('-'*30 + "Step 1 finish" + '-'*30)
cfg.print_all()

# step 2: delete X -> ε

def is_right_empty(pair):
    if len(pair.right) == 1 and pair.right[0] == 'ε':
        return True
    return False

def not_any_empty(cfg):
    for rule in cfg.data:
        if is_right_empty(rule):
            return rule
    return None

def generate_makeup(rule, empty):
    empty = empty # 'X' # X -> ε
    tmp_cfg = PairSet([ rule ])
    tmp_cfg_len = 0

    while tmp_cfg_len != len(tmp_cfg.data):
        tmp_cfg_len = len(tmp_cfg.data)
        tmp = PairSet()
        for rule in tmp_cfg.data:
            main_right = rule.right

            pos = list()
            for i in range(len(main_right) ):
                if main_right[i] == empty:
                    pos.append(i)


            for i in pos:
                sub_right = copy.deepcopy(main_right)
                sub_right[i] = 'ε'
                tmp.add(Pair(rule.left, sub_right))
        for rule in tmp.data:
            tmp_cfg.add(rule)

    return tmp_cfg

def remove_empty(rule):
    while 'ε' in rule.right:
        rule.right.remove('ε')
    return rule


del_rule = not_any_empty(cfg)

while del_rule:
    others = list()
    contains = list()
    for rule in cfg.data:
        if rule.left == del_rule.left and not is_right_empty(rule):
            others.append(rule.right)
        if del_rule.left in rule.right:
            contains.append(rule)

#     print(len(others), len(contains))
#     del_rule = None
    for rule in contains:
        tmp_cfg = generate_makeup(rule, del_rule.left)
        for tmp_rule in tmp_cfg.data:
            cfg.add(tmp_rule)

    cfg.delete(del_rule)
    for rule in cfg.data:
        rule = remove_empty(rule)
        if len(rule.right) == 0:
            rule.right = ['ε']

    del_rule = not_any_empty(cfg)
#     print(not_any_empty(cfg).left)

print('-'*30 + "Step 2 finish" + '-'*30)
cfg.print_all()

# step 3: delete A -> B
del_cfg = PairSet()

cfg_len = 0

while cfg_len != len(cfg.data):
    cfg_len = len(cfg.data)
    for rule in cfg.data:
        generates = list()
        if len(rule.right) == 1 and rule.right[0] not in terminals: # single variable
            for tmp_rule in cfg.data:
                if tmp_rule.left == rule.right[0]: # right equals left
                    new_pair = Pair(rule.left, tmp_rule.right) # generate new rule
                    if not del_cfg.is_in_set(new_pair): # add only if have not been delated
                        generates.append(new_pair)

            for new_pair in generates:
                cfg.add(new_pair)
            cfg.delete(rule)


print('-'*30 + "Step 3 finish" + '-'*30)
cfg.print_all()

# step 4: split right part whose length is longer than 2
split = list()
u_cnt = 0
new_variable = 'U'

def get_rule_longer_than_two(cfg):
    for rule in cfg.data:
        if len(rule.right) >= 3:
            return rule
    return None

# more than 2 -> 2
longer = get_rule_longer_than_two(cfg)
while longer:
    tmp1_left = longer.left
    tmp1_right = [longer.right[0], new_variable+str(u_cnt)]
    tmp2_left = new_variable+str(u_cnt)
    tmp2_right = longer.right[1:]
    cfg.add(Pair(tmp1_left, tmp1_right))
    cfg.add(Pair(tmp2_left, tmp2_right))
    u_cnt += 1
    
    
    cfg.delete(longer)
    longer = get_rule_longer_than_two(cfg)

# terminal -> variable
cfg_len = 0

while cfg_len != len(cfg.data):
    cfg_len = len(cfg.data)
    
    for rule in cfg.data:
        if len(rule.right) == 2:
            
            if rule.right[0] not in terminals and rule.right[1] not in terminals:
                continue
                
            if rule.right[0] in terminals and rule.right[1] in terminals:
                tmp1_left = rule.left
                tmp1_right = [new_variable+str(u_cnt), new_variable+str(u_cnt+1)]
                tmp2_left = new_variable+str(u_cnt)
                tmp2_right = [rule.right[0]]
                tmp3_left = new_variable+str(u_cnt+1)
                tmp3_right = [rule.right[1]]
                cfg.add(Pair(tmp1_left, tmp1_right))
                cfg.add(Pair(tmp2_left, tmp2_right))
                cfg.add(Pair(tmp3_left, tmp3_right))
                u_cnt += 1
            elif rule.right[0] in terminals and rule.right[1] not in terminals:
                tmp1_left = rule.left
                tmp1_right = [new_variable+str(u_cnt), rule.right[1]]
                tmp2_left = new_variable+str(u_cnt)
                tmp2_right = [rule.right[0]]
                cfg.add(Pair(tmp1_left, tmp1_right))
                cfg.add(Pair(tmp2_left, tmp2_right))
                
            elif rule.right[0] not in terminals and rule.right[1] in terminals:
                tmp1_left = rule.left
                tmp1_right = [rule.right[0], new_variable+str(u_cnt)]
                tmp2_left = new_variable+str(u_cnt)
                tmp2_right = [rule.right[1]]
                cfg.add(Pair(tmp1_left, tmp1_right))
                cfg.add(Pair(tmp2_left, tmp2_right))

            u_cnt += 1
            cfg.delete(rule)

print('-'*30 + "Step 4 finish" + '-'*30)
cfg.print_all()

