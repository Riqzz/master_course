## Project 1

#### Experiment 1

* **Goal**

  Write a program to match IP address with regular expression. It is required to match the legitimate IP address format correctly.

* **Design**

  It is known that there are $4$ segments in an IP address, and the range of each segment is from $0$ to $255$, but the first segment can not involve $0$.

  We can summarize the form of each IP address segment in regular expression as following:

  * $2[0-4][0-9]$ represents the range $200$ ~ $249$
  * $25[0-5]$ represents the range $250$ ~ $255$
  * $1[0-9][0-9]$ represents the range $100$ ~ $199$.
  * $[1-9][0-9]$ represents the range $10$ ~ $99$
  * $[0-9]$represents the range $0$ ~ $9$

  So, let $s_1$, $s_2$ be the first and three back segments, and then, the IP address could be written as $s_1.s_2.s_2.s_2$.we can use the re package to recognize every segment as following:

  ```python
  s1 = '(25[0-5]|(1\d|2[0-4]|[1-9]{1})\d|[1-9])' 		# 1~255
  s2 = '(25[0-5]|(1\d|2[0-4]|[1-9]{0,1})\d)' 			# 0~255
  ```

  Add separation character before each $s_2$ , we can get a tuple by repeating:

  ```python
  s2_tuple = '((\.(25[0-5]|(1\d|2[0-4]|[1-9]{0,1})\d)){3})'	# .255.255.255
  ```

  To recognize the form of IP address, the regular expression pattern could be defined as following:

  ```python
  ip_str = "^{}{}$".format(s1,s2_tuple)
  ip_pattern = re.compile(ip_str)
  ```

  Then we can define a function to match an  IP address:

  ```python
  def match(ip):
      s1 = '(25[0-5]|(1\d|2[0-4]|[1-9]{1})\d|[1-9])'
      s2_tuple = '((\.(25[0-5]|(1\d|2[0-4]|[1-9]{0,1})\d)){3})'
      ip_str = "^{}{}$".format(s1,s2_tuple)
  	ip_pattern = re.compile(ip_str)
      result = re.search(ip_pattern, ip)
      if result is not None:
          print("successful: ", result.group())
      else
      	print("faild")
  ```

* **Result**

  ```python
  >>> match('127.0.0.1')
  successful:  127.0.0.1
  >>> match('0.0.0.0')
  faild
  >>> match('127.0.0.256')
  faild
  ```
#### Experiment 2

* **Goal**

  Write a program to realize the conversion from regular expression to non-deterministic finite automata (NFA), and design data structure to represent in computer.
  
* **Design**

  - **Regular Expression (RE): **

    Say that $R$ is a regular expression if $R$ is:

    1. $a$ for some $a$ in alphabet $\Sigma$,
    2. $\varepsilon$,
    3. $\phi$,
    4. $(R_1 \cup R_2)$, where $R_1$ and $R_2$ are regular expressions,
    5. $(R_1 \circ R_2)$, where $R_1$ and $R_2$ are regular expressions,
    6. $(R_1^*)$, where $R_1$ regular expressions.

    Other typical abbreviated signal, for example  $(R_1^+)$ , could be generated by combining these basic regular expression defined above like$(R_1 \circ R_1^*)$.

  - **Non-deterministic Finite Automaton (NFA): **

    A non-deterministic finite automata is a 5-tuple $(Q,\Sigma,\delta,q_0,F)$, where:

    1. $Q$ is a finite set of states,
    2. $\Sigma$ is a finite alphabet,
    3. $\delta:Q \times\Sigma_\varepsilon \to \mathcal{P}(Q)$ is the transition function,
    4. $q_0 \in Q$ is the start state,
    5. $F \subseteq Q$ is the set of accept states.

    The data structure of state $q \in Q$ is implement as following:

    ```python
    class State:
        cnt = 0
        def __init__(self, enter, to1 = None):
            self.enter = enter
            self.to1 = to1
    
            self.no = State.cnt
            State.cnt += 1
    ```

    `cnt` is a static value of the class `State` used to count the amount of states and number states. `enter` is the input value, and  `to1` points to next state. The successful completion of state transition is based on both of them.`no` is the number of the state.

  - **Thompson Algorithm**

    Thompson algorithm can complete the conversion from regular expressions to non-deterministic finite automata with $\varepsilon$ ($\varepsilon $-NFA). First construct the $\varepsilon $-NFA that recognizes the sub-expression, and then merge the $\varepsilon $-NFA through a few simple rules, and finally get the $\varepsilon $-NFA that recognizes the complete regular expression. 

    There are three cases to construct NFA from RE through Thompson algorithm: 
    - The state machine must have **only one **initial state node and one end state node.

    - In any state, there are **at most two** transition edges going out.

    - Each state node has **at most three** possible edges: 

      1. One edge with the value $a$ ;

         ```mermaid
         graph LR
           BEGIN(( )) -->|a| END((  ))
         ```

      2. One edge with the value $\varepsilon$ ;

         ```mermaid
         graph LR
           BEGIN(( )) -->|ε| END((  ))
         ```

      3. Two edges with both the value $\varepsilon$ .

         ```mermaid
         graph LR
           BEGIN(( )) -->|ε| END1((  ))
           BEGIN(( )) -->|ε| END2((  ))
         ```

    So, it is necessary to design a new data structure to represent the last structure of case three, which requires two pointers for two directions.  Let it be named as `Split`, and its implement is as following:

    ```python
    class Split(State):
        def __init__(self, to1, to2):
            super(Split, self).__init__(SPLIT, to1)
            self.to2 = to2
    ```

    `split` inherits from class `State` and sets the attribute `enter` and `to1` by calling the super construction function, and meanwhile, sets the another pointer `to2` to another next state.

    **Induction** method is used in order to read regular expressions correctly, so it requires to make sub states as one segment. So we introduce a new data structure `Fragment` representing the  segment of several sub states. The implement is as following:

    ```python
    class Fragment:
        def __init__(self, begin, end = None):
            self.begin = begin
            self.end = begin
            if end:
                self.end = end
    ```

    `begin` means the input state of the segment `Fragment`, and relatively, `end` means the output. It is constructed by recursion, and the constructing rules are as following. Note that every circle represent a state, directed edges represent inputs, and rectangles are the `Fragment`.The dotted lines in a fragment means there may exits other fragments.

    - Basic Rule

      1. expression $a$
      
      ```mermaid
      graph LR
        subgraph f [ ]
        BEGIN(( begin)) -->|a| END(( end ))
        end
        pre((pre))-.->BEGIN
        END-->|ε|next((next))
      ```
      
      2. expression $\varepsilon$
      
      ```mermaid
      graph LR
        subgraph f [ ]
        BEGIN(( begin)) -->|ε| END((end ))
        end
        pre((pre))-.->BEGIN
        END-->|ε|next((next))
      ```
      
    - Induction Rule

      1. expression $st$ schematic diagram and its implement

         ```mermaid
         graph LR
             subgraph s [s]
             s1(( begin))-.->s2((end ))
             end
             subgraph t [t]
             t1(( begin))-.->t2(( end))
             end
             s2-->|ε|t1
             
             pre((pre))-.->s1
             t2-->|ε|next((next))
         ```

    ```python
    def joint(self, frag1, frag2):
         if frag2 is None:
             return frag1
         else:
             frag1.end.to1 = frag2.begin
             return Fragment(frag1.begin, frag2.end)
    ```

      2. expression $s|t$ schematic diagram and its implement

         ```mermaid
         graph LR
             subgraph s [s]
             s1(( begin))-.->s2(( end))
             end
             subgraph t [t]
             t1(( begin))-.->t2(( end))
             end
             
             split(( split))
             merge(( merge))
             pre(( pre))
             next(( next))
             split-->|ε|s1
             split-->|ε|t1
             
             s2-->|ε|merge
             t2-->|ε|merge
             
             pre-.->split
             merge-->|ε|next
         ```

    ```python
    def union(self, frag1, frag2):
        split = Split(frag1.begin, frag2.begin)
        merge = State(MERGE)
      	frag1.end.to1 = merge
       	frag2.end.to1 = merge
        return Fragment(split, merge)
    ```

      3. expression $s^*$ schematic diagram and its implement

         ```mermaid
         graph LR
             subgraph s [s]
             s1((begin))-.->s2(( end ))
             end
             
             split((split))
             pre(( pre))
             next(( next))
             split-->|a|s1
             s2-->|ε|split
             pre-.->split
             split-->|ε|next
             
         ```

    ```python
    def star(self, frag1):
       	split = Split(frag1.end.to1, frag1.begin)
        frag1.end.to1 = split
        return Fragment(split)
    ```

      4. expression $s^+$ schematic diagram and its implement

         ```mermaid
         graph LR
             subgraph s [s]
             s1((begin))-.->s2(( end ))
             end
             
             split((split))
             pre(( pre))
             next(( next))
             split-->|ε|s1
             s2-->|a|split
             pre-.->s1
             split-->|ε|next
         ```

    ```python
    def plus(self, frag1):
      	split = Split(frag1.end.to1, frag1.begin)
      	frag1.end.to1 = split
      	return Fragment(frag1.begin, split)
    ```
    - The core code of NFA building function is implemented as following:
    
    ```python
    def build(...)
    	# omit some code here
        if alpha == '$' :
            return self.joint(frag, pre)
        elif alpha in self.ALPHABET :
            return self.build(pattern, self.letter(alpha), self.joint(frag, pre))
        elif alpha == '|' :
            return self.union(self.joint(frag, pre), self.build(pattern, None, 			self.begin()))
        elif alpha == '*' :
            return self.build(pattern, self.star(pre), frag)
        elif alpha == '+' :
            return self.build(pattern, self.plus(pre), frag)
        elif alpha == '(' :
            return self.build(pattern, self.build(pattern, None, self.begin()), 		self.joint(frag, pre))
        elif alpha == ')' :
            return self.joint(frag, pre)
    ```
    

    `alpha` is a iterator signal in regular expression, and the building function calls different functions of construction rules defined above according to different signal values.

* **Result**

  * Test case 1
  
    - Input:
  
    ```pyth
    regular expression = "abcd$"
    language = "abcd"
    ```
  
    - Output:
  
    ```python
    the NFA diagram:
    state 0 (^) ---> state 1
    state 1 (a) ---> state 2
    state 2 (b) ---> state 3
    state 3 (c) ---> state 4
    state 4 (d) ---> state 5
    state 5 ($) ---> output
    
    language length:  4 , matched length:  4
    
    median state [0, 1, 2, 3, 4, 5]
    ```
  
  * Test Case 2
  
    - Input
  
    ```python
    regular expression = "(a|b)(c|d)$"
    language = "ad"
    ```
  
    - Output
  
    ```python
    the NFA diagram:
    state 0 (^) ---> state 5
    state 5 (SPLIT) ---> state 1
    state 1 (^) ---> state 2
    state 2 (a) ---> state 6
    state 6 (MERGE) ---> state 11
    state 11 (SPLIT) ---> state 7
    state 7 (^) ---> state 8
    state 8 (c) ---> state 12
    state 12 (MERGE) ---> state 13
    state 13 ($) ---> output
    state 11 (SPLIT) ---> state 9
    state 9 (^) ---> state 10
    state 10 (d) ---> state 12
    state 5 (SPLIT) ---> state 3
    state 3 (^) ---> state 4
    state 4 (b) ---> state 6
    
    language length:  2 , matched length:  2
    
    median state [0, 5, 3, 4, 1, 2, 6, 11, 9, 7, 10, 8, 12, 13]
    ```
  
  * Test Case 3
  
    - Input
  
    ```python
    regular expression = "a*(bc)*d*$"
    language = "aaaaaaabcbc"
    ```

    - Output
    
    ```python
    the NFA diagram:
    state 0 (^) ---> state 2
    state 2 (SPLIT) ---> state 6
    state 6 (SPLIT) ---> state 8
    state 8 (SPLIT) ---> state 9
    state 9 ($) ---> output
    state 8 (SPLIT) ---> state 7
    state 7 (d) ---> state 8
    state 6 (SPLIT) ---> state 3
    state 3 (^) ---> state 4
    state 4 (b) ---> state 5
    state 5 (c) ---> state 6
    state 2 (SPLIT) ---> state 1
    state 1 (a) ---> state 2
    
    language length:  11 , matched length:  11
            
    median state [0, 2, 6, 1, 8, 3, 7, 9, 4, 2, 6, 1, 8, 9, 3, 7, 4, 2, 6, 1, 8, 9, 3, 7, 4, 2, 6, 1, 8, 9, 3, 7, 4, 2, 6, 1, 8, 9, 3, 7, 4, 2, 6, 1, 8, 9, 3, 7, 4, 2, 6, 1, 8, 9, 3, 7, 4, 2, 6, 1, 8, 9, 3, 7, 4, 5, 6, 8, 3, 4, 9, 7, 5, 6, 8, 3, 4, 9, 7]
    ```
    
  * Test Case 4
  
    - Input
  
    ```python
    regular expression = "a+b+(cd)+$"
    language = "aaabbbbbcd"
    ```
    - Output
  
    ```python
    the NFA diagram:
    state 0 (^) ---> state 1
    state 1 (a) ---> state 2
    state 2 (SPLIT) ---> state 3
    state 3 (b) ---> state 4
    state 4 (SPLIT) ---> state 5
    state 5 (^) ---> state 6
    state 6 (c) ---> state 7
    state 7 (d) ---> state 8
    state 8 (SPLIT) ---> state 9
    state 9 ($) ---> output
    state 8 (SPLIT) ---> state 5
    state 4 (SPLIT) ---> state 3
    state 2 (SPLIT) ---> state 1
    
    language length:  10 , matched length:  10
            
    median state [0, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 4, 5, 3, 6, 4, 5, 3, 6, 4, 5, 3, 6, 4, 5, 3, 6, 4, 5, 3, 6, 7, 8, 5, 9, 6]
    ```
  * Test Case 5
  
    - Input
  
    ```python
    regular expression = "(a|b)*c*(de)+$"
    language = "ababbadede"
    ```
    - Output
    
    ```python
    the NFA diagram:
    state 0 (^) ---> state 7
    state 7 (SPLIT) ---> state 9
    state 9 (SPLIT) ---> state 10
    state 10 (^) ---> state 11
    state 11 (d) ---> state 12
    state 12 (e) ---> state 13
    state 13 (SPLIT) ---> state 14
    state 14 ($) ---> output
    state 13 (SPLIT) ---> state 10
    state 9 (SPLIT) ---> state 8
    state 8 (c) ---> state 9
    state 7 (SPLIT) ---> state 5
    state 5 (SPLIT) ---> state 1
    state 1 (^) ---> state 2
    state 2 (a) ---> state 6
    state 6 (MERGE) ---> state 7
    state 5 (SPLIT) ---> state 3
    state 3 (^) ---> state 4
    state 4 (b) ---> state 6
    
    language length:  10 , matched length:  10
            
    median state [0, 7, 9, 5, 10, 8, 3, 11, 1, 4, 2, 6, 7, 9, 5, 10, 8, 3, 11, 1, 4, 2, 6, 7, 9, 5, 10, 8, 3, 11, 1, 4, 2, 6, 7, 9, 5, 10, 8, 3, 11, 1, 4, 2, 6, 7, 9, 5, 10, 8, 3, 11, 1, 4, 2, 6, 7, 9, 5, 10, 8, 3, 11, 1, 4, 2, 6, 7, 9, 5, 10, 8, 3, 11, 1, 4, 2, 12, 13, 10, 14, 11, 12, 13, 10, 14, 11]
    ```
  
  

