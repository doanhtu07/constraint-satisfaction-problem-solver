import sys
from backtrack import Backtrack
from parse import parseContraints, parseVariables, normalizeConstraints


def main():
    varFile = sys.argv[1]  # variables
    conFile = sys.argv[2]  # constraints
    procedure = sys.argv[3]  # procedure

    variables = parseVariables(varFile)
    constraints = parseContraints(conFile)
    constraintsMap = normalizeConstraints(constraints)

    bt = Backtrack(variables, constraintsMap, procedure)
    bt.backtrack()


main()
