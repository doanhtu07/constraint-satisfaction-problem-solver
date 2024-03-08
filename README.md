# Constraint Satisfaction Problem Solver

- Use most constrained variable heuristic to prioritize variable, most constraining variable heuristic to break ties, and alphabetical order to break ties in extreme cases

- Use least constraining value heuristic to prioritize value and numerical order to break ties

## How to use

Use python3 with main.py.

Accept input as follows: Variable file path -> Constraint file path -> Procedure (none / fc)

Procedure "fc" stands for forward checking.

You can check out the results with example files.

## Example

### Variable file

```
A: 1 2 3 4 5
B: 1 2 3 4 5
C: 1 2 3 4 5
D: 1 2 3 4 5
E: 1 2 3
F: 1 2 
```

### Constraint file

```
A > B
B > F
A > C
C > E
A > D
D = E
```

### Result

- Using procedure "none"

```
1. F=1, E=1, A=5, B=1  failure
2. F=1, E=1, A=5, B=2, C=1  failure
3. F=1, E=1, A=5, B=2, C=2, D=1  solution
```

- Using procedure "fc"

```
1. F=1, E=1, D=1, A=5, B=2, C=2  solution
```

### Example call

```
python3 main.py ./example_files/ex1.var ./example_files/ex1.con none
```
