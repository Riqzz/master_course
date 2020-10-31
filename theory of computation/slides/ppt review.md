#### 6-2 Turing Machine

* Recognizable language

  | Automata                                  | Recognizable language            |
  | ----------------------------------------- | -------------------------------- |
  | Deterministic finite automata (DFA)       | regular languages                |
  | Nondeterministic finite automata (NFA)    | regular languages                |
  | Regular languages Pushdown automata (PDA) | context-free languages           |
  | Linear bounded automata (LBA)             | context-sensitive language       |
  | Turing machines (TM)                      | recursively enumerable languages |

* Call a language **Turing Recognizable**, if some TM recognizes it.

  *other name: Turing Acceptable, Recursively Enumerable*

* Standard TM simulates Stay-Option TM: 

  * the stay option

  ```mermaid
  graph LR;  
  　　A((Q1)) -- a->b,S --> B((Q2))
  ```

  * simulation: x is any possible symbol

  ```mermaid
  graph LR;  
  　　A((Q1)) -- a->b,L --> C((Qt)) -- x->x,R --> B((Q2))
  ```

* Nondeterministic TM key points:

  - configurations form a tree, each children nodes are yielded by their parent configuration
  - so, every configuration can be encode an address uniquely
  - use breadth first search (there may exist infinite path)

