from __future__ import division
from __future__ import print_function

__author__ = 'Sahand Saba'


class SATInstance(object):
    def parse_clause(self, clause):
        for literal in clause:
            negated = -1 if literal < 0 else 1
            
            variable = literal * negated
            
            if variable not in self.variable_table:
                self.variable_table[variable] = len(self.variables)
                self.variables.append(variable)
            
        self.clauses.append(tuple(set(clause)))

    def __init__(self):
        self.variables = []
        self.variable_table = dict()
        self.clauses = []

    @classmethod
    def get_rules_and_game(cls, file):
        instance = cls()
        with open('sudoku-rules2.txt') as rules:
            in_rules = rules.readlines() 
            cnf = list()
            cnf.append(list())

            for line in in_rules:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c", "#"):
                    for tok in tokens:
                        lit = int(tok)
                        if lit == 0:
                            cnf.append(list())
                        else:
                            cnf[-1].append(lit)

            assert len(cnf[-1]) == 0
            cnf.pop()

        with open('sudoku-example.txt') as game:
            in_game = game.readlines() 

            cnf.append(list())

            for line in in_game:
                tokens = line.split()
                
                if len(tokens) != 0 and tokens[0] not in ("p", "c", "#"):
                    for tok in tokens:
                        lit = int(tok)
                        if lit == 0:
                            cnf.append(list())
                        else:
                            cnf[-1].append(lit)
                        

            assert len(cnf[-1]) == 0
            cnf.pop()
        
        print(cnf)

        for clause in cnf:
            instance.parse_clause(clause)

        print("\nvariables: ",instance.variables)
        print("\nvariable_table: ",instance.variable_table)
        print("\nclauses: ", instance.clauses)

        return instance

    def literal_to_string(self, literal):
        s = '~' if literal & 1 else ''
        return s + self.variables[literal >> 1]

    def clause_to_string(self, clause):
        return ' '.join(self.literal_to_string(l) for l in clause)

    def assignment_to_string(self, assignment, brief=False, starting_with=''):
        literals = []
        for a, v in ((a, v) for a, v in zip(assignment, self.variables)
                     if v.startswith(starting_with)):
            if a == 0 and not brief:
                literals.append('~' + v)
            elif a:
                literals.append(v)
        return ' '.join(literals)
