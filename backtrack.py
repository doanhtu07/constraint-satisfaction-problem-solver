from typing import Dict, List, Tuple, Set
from collections import defaultdict


class Backtrack:
    def __init__(self,
                 variables: Dict[str, Set[int]],
                 constraintsMap: Dict[str, List[Tuple[str, str]]],
                 procedure: str  # none / fc
                 ) -> None:
        self.variables = variables
        self.constraintsMap = defaultdict(list, constraintsMap)
        self.procedure = procedure

    def backtrack(self):
        # Keep track of current domains of all UNASSIGNED variables
        self.domains: Dict[str, Set[int]] = self.copyDomains(self.variables)

        # A list of assignments of variables. This will be built up by backtracking. The list has tuples of (variable name, value assigned)
        self.assignments: List[Tuple[str, int]] = []

        # A dictionary of what variable has been assigned and what value it has for faster search in code
        self.assigned: Dict[str, int] = dict()

        # Line count used for printing on terminal
        self.count = 1

        # Recursive core of backtrack
        self.backtrackHelper()

    # Return true when found the solution, else return false
    def backtrackHelper(self) -> bool:
        # If assignments have all variables already, it guarantees to be the solution.
        # We know this because the algorithm will check validity before making the next backtrack recursive call.
        if len(self.assignments) == len(self.variables):
            print(f'{self.count}.', end=' ')
            self.printAssignment(self.assignments)
            print(" solution")
            return True

        # Get sorted variables based on most constrained, most constraining, then alphabetical
        variables = self.sortedVariables()
        chosenVariable = variables[0]

        # Get sorted values of chosen variable based on least constraining, then smaller value
        values = self.sortedValues(chosenVariable)

        # Remove chosen variable from domains of UNASSIGNED variables
        del self.domains[chosenVariable]

        for val in values:
            # Assign value to variable
            self.assignments.append((chosenVariable, val))
            self.assigned[chosenVariable] = val

            # Forward check if the procedure says so
            oldDomains = self.copyDomains(self.domains)
            if self.procedure == 'fc':
                self.forwardCheck(chosenVariable, val)

            # Check if new variable is valid with other assignments (AND if after forward checking, the domains is still valid)
            valid = self.checkValid(chosenVariable, val)

            if valid:
                foundSolution = self.backtrackHelper()
                if foundSolution:
                    return True
            else:
                print(f'{self.count}.', end=' ')
                self.printAssignment(self.assignments)
                print(" failure")
                self.count += 1

            # Clean up current value assignment to prepare for next value of chosen variable
            self.assignments.pop()
            del self.assigned[chosenVariable]
            self.domains = oldDomains

        return False

    def sortedVariables(self):
        remainVariables = [variable for variable in self.domains]

        # Sort based on three things
        remainVariables = sorted(
            remainVariables,
            key=lambda variable: (
                len(self.domains[variable]),  # Most constrained variable
                -self.getDegree(variable),  # Most constraining variable
                variable  # Alphabet
            )
        )

        return remainVariables

    # Count number of constraints a variable is associated with (Only count other variables if they are UNASSIGNED)
    def getDegree(self, variable: str) -> int:
        degree = 0

        for constraint in self.constraintsMap[variable]:
            operator, variable2 = constraint
            if variable2 in self.assigned:
                continue
            degree += 1

        return degree

    def sortedValues(self, variable: str) -> List[int]:
        domain = self.domains[variable]

        domain = sorted(
            domain,
            key=lambda value: (
                self.getRuleOut(variable, value),  # Least constraining value
                value  # Smaller value
            )
        )

        return domain

    # Get number of values of other variables ruled out if picking this variable with this value
    def getRuleOut(self, variable: str, value: int) -> int:
        ruleOut = 0

        # Go through all UNASSIGNED variables and their values to see if those values are invalid (thus ruled out) or not
        for variable2 in self.domains:
            for value2 in self.domains[variable2]:
                first = (variable, value)
                second = (variable2, value2)
                constraints = self.getConstraints(first[0], second[0])

                for constraint in constraints:
                    operator = constraint[0]
                    if operator == '=':
                        if first[1] != second[1]:
                            ruleOut += 1
                    elif operator == '!':
                        if first[1] == second[1]:
                            ruleOut += 1
                    elif operator == '<':
                        if first[1] >= second[1]:
                            ruleOut += 1
                    elif operator == '>':
                        if first[1] <= second[1]:
                            ruleOut += 1

        return ruleOut

    # Get all constraints involving variable v2 with respect to variable v1
    def getConstraints(self, v1: str, v2: str) -> List[Tuple[str, str]]:
        constraints = filter(
            lambda constraint: constraint[1] == v2,
            self.constraintsMap[v1]
        )
        return constraints

    def checkValid(self, variable: str, value: int) -> bool:
        # Check if (variable, value) is consistent with all previous assignments we currently have
        for variable2 in self.assigned:
            first = (variable, value)
            second = (variable2, self.assigned[variable2])
            constraints = self.getConstraints(first[0], second[0])

            for constraint in constraints:
                operator = constraint[0]
                if operator == '=':
                    if first[1] != second[1]:
                        return False
                elif operator == '!':
                    if first[1] == second[1]:
                        return False
                elif operator == '<':
                    if first[1] >= second[1]:
                        return False
                elif operator == '>':
                    if first[1] <= second[1]:
                        return False

        # If forward checking, check if the domain of any variables is empty, meaning no valid choices to be made later on
        if self.procedure == 'fc':
            for variable2 in self.domains:
                if len(self.domains[variable2]) == 0:
                    return False

        return True

    # Check all UNASSIGNED variables and filter their domains with respect to input (variable, value)
    def forwardCheck(self, variable: str, value: int) -> None:
        for variable2 in self.domains:
            for value2 in list(self.domains[variable2]):
                first = (variable, value)
                second = (variable2, value2)
                constraints = self.getConstraints(first[0], second[0])

                for constraint in constraints:
                    operator = constraint[0]
                    if operator == '=':
                        if first[1] != second[1]:
                            self.domains[second[0]].remove(second[1])
                    elif operator == '!':
                        if first[1] == second[1]:
                            self.domains[second[0]].remove(second[1])
                    elif operator == '<':
                        if first[1] >= second[1]:
                            self.domains[second[0]].remove(second[1])
                    elif operator == '>':
                        if first[1] <= second[1]:
                            self.domains[second[0]].remove(second[1])

    def copyDomains(self, domains: Dict[str, Set[int]]) -> Dict[str, Set[int]]:
        copiedDomains = dict()
        for variable in domains:
            copiedDomains[variable] = domains[variable].copy()
        return copiedDomains

    def printAssignment(self, assignments: List[Tuple[str, int]]) -> None:
        for i in range(len(assignments)):
            assign = assignments[i]
            print(
                f'{assign[0]}={assign[1]}',
                end=', ' if i != len(assignments)-1 else ' '
            )
