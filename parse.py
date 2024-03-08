from typing import Dict, Tuple, List, Set


operators = ['=', '!', '>', '<']


# Return a map that has (key = variable name) and (value = domain set of that variable)
def parseVariables(varFile: str) -> Dict[str, Set[int]]:
    f = open(varFile, "r")
    lines = f.readlines()

    ans = dict()

    for line in lines:
        line = line.strip()
        tokens = line.split(" ")
        variable = tokens[0][0:-1]
        ans[variable] = set([int(x) for x in tokens[1:]])

    f.close()

    return ans


# Return a list of all constraints. E.g, [['A', '<', 'B'], ...]
def parseContraints(conFile: str) -> List[List[str]]:
    f = open(conFile, "r")
    lines = f.readlines()

    ans = []

    for line in lines:
        line = line.strip()
        tokens = line.split(" ")
        ans.append(tokens)

    f.close()

    return ans


# Returns a map with (key = variable name) and (value = constraints of that variable with other variables)
# E.g, 'A': [('<', 'B'), ...]
def normalizeConstraints(constraints: List[List[str]]) -> Dict[str, List[Tuple[str, str]]]:
    ans = dict()

    for con in constraints:
        v1, op, v2 = con

        if v1 not in ans:
            ans[v1] = list()
        if v2 not in ans:
            ans[v2] = list()

        ans[v1].append((op, v2))

        reverseOp = reverseOperator(op)
        ans[v2].append((reverseOp, v1))

    return ans


def reverseOperator(op: str) -> str:
    if op == '=':
        return '='
    if op == '!':
        return '!'
    if op == '>':
        return '<'
    if op == '<':
        return '>'

    # Should never reach this line if input is valid
    return "?"
