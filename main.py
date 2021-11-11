#!/usr/bin/env python
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
from argparse import FileType
from sys import stdin
from sys import stdout
from sys import stderr

from satinstance import SATInstance
from solvers.watchlist import setup_watchlist
from solvers import recursive_sat
from solvers import iterative_sat

__author__ = 'Sahand Saba'


def generate_assignmnets(instance, solver, verbose=False):
    """
    Returns a generator that generates all the satisfying assignments for a
    given SAT instance, using algorithm given by alg.
    """
    n = len(instance.variables)
    watchlist = setup_watchlist(instance)
    print("\n WATCHLIST: {}".format(watchlist))

    if not watchlist:
        return ()
    
    assignment = [None] * n
    return solver.solve(instance, watchlist, assignment, 0, verbose)


# def run_solver(input_file, solution_type):
def run_solver():
    """
    Run the given solver for the given file-like input object and write the
    output to the given output file-like object.
    """
       
    input_file = ""
    instance = SATInstance.get_rules_and_game(input_file)
    
    assignments = generate_assignmnets(instance, solver=recursive_sat, verbose=True)
    count = 0
    for assignment in assignments:
        count += 1
        
        print('Found satisfying assignment #{}:'.format(count),
                  file=stderr)
        assignment_str = instance.assignment_to_string(
                assignment,
                brief=brief,
                starting_with=starting_with
        )
        output_file.write(assignment_str + '\n')
        if not output_all:
            break

    if count == 0:
        print('No satisfying assignment exists.', file=stderr)


def main():
    """
    args = parse_args()
    with args.input:
        print(args)
        run_solver(args.input, args.solutiontype) 
    """
    run_solver()

def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-S',
                        '--solutiontype',
                        help='method number',
                        type=int)
    parser.add_argument('-i',
                        '--input',
                        help='read from given file',
                        type=FileType('r')
                        )
    return parser.parse_args()


if __name__ == '__main__':
    main()
