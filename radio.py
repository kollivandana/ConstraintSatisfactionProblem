# Radio program
# B551 Fall 2015
# Name    : VANDANA KOLLI
# User ID : kolliv
# Description of the Problem ans solution:
# All the states should be assigned a frequency with a constraint that no two states get the same frequency
# Solution:
# I have implemented BACKTRACKING with forward checking
# The backtrack algorithm was used along with the 3 heuristics and forward checking.
# Backtrack algorithm:
#
# If all assignments are complete then return Assignment
# X --> select a variable not in Assignment  (Use Most constraining variable and most constrained variable to pick a variable)
# D --> select an ordering on the domain of X ( Use Least constraining value heuristic to pick the best value)
# For each value v in D do
#  If X = v is consistent with A    -  checks if assigning a value to the current state is consistence with values assigned to other neighbours
#    Add (X<--v) to A then          -  Also remove the assigned value from neighbours (forward checking)
#    result <-- CSP-BACKTRACKING(A) -  recursive call  for backtracking
#    If result not failure then return result - check for result, if not failure then return result
#    Remove (X<--v) from A                    - delete the assignment if false is returned
# Return failure                   - If the entire domain is completed and no value was consistent then return false
#
# Heuristics used :
# Most constrained variable  : chooses the variable with the fewest “legal” frequencies
# Most constraining variable :among the variables with the smallest remaining domains (ties with respect to the most constrained variable heuristic),
#                             select the one that appears in the largest number of constraints on variables not in the current assignment
#
# Least constraining Value   : chooses the variable that rules out the fewest values in the remaining variables
#
# problems faced : Deciding on an algorithm consumed lot of time. There was backtacking with heuristics and filtering (ARC and Forward checking)
#                  also the heuristics testing took time and effort
#
# assumptions made : None
#
# The program executes backtracking and assigns the frequency to all states. No backtracking occurs for any of the contraint file.
#

import random
import sys
import os
from collections import defaultdict

# adjStatesDict      : Static dictionary with neighbours
# assignedStatesDict : Dynamic dictionary for assigned states
# csp                : Dynamic The list of states and corresponding domains
# static csp

assignedStatesDict = {} # for all the assignment variable -> value pairs
csp = {}      # Each state with all the domain values assigned
cspStatic = {}
countBacktracks = 0

def fetch_state(assignment,csp):
    #minimum remaining values state
    new_dict = defaultdict(list)
    new_dict = csp.copy()
    #print(len(new_dict))
    for i in csp.keys():
        if i in assignment.keys():
            del new_dict[i]
    var = min(new_dict.keys(), key=lambda k: len(new_dict[k]))

    same_len_domains = []
    for j in new_dict.keys():
        if len(new_dict[var]) == len(new_dict[j]):
            same_len_domains.append(j)
    max_count = 0
    max_neigh = ''
    for k in adjStatesDict.keys():
        for m in same_len_domains:
            if k == m and max_count <= len(adjStatesDict[k]):
                max_neigh = m
                max_count = len(adjStatesDict[k])
    return max_neigh

    ''' minValuesList = []
    for key in new_dict.keys():
        if(len(new_dict[key]) == len(new_dict[var])):
            minValuesList.append(key)

    if(len(minValuesList) > 1):
        minVarAdjDict = {}
        for minVar in minValuesList:
            minVarAdjDict[minVar] = len(adjStatesDict[minVar])

        finalVar = max(minVarAdjDict.keys(), key=lambda k: minVarAdjDict[k])
        return finalVar'''

    #return var

def first_unassigned_variable(assignment, adjStatesDict):

    "The default variable order."
    for var in adjStatesDict:
        found =0
        if(len(assignment) == 0):
            return var
        else:
            #for assignedValues in assignment:
            for keyState in assignment.keys():
                if (var == keyState):
                    found = 1;
                    break

            if found == 0:
                    return var;

def valueConsistent(var,val):
    for neighbour in adjStatesDict[var]:
        if(len(csp[neighbour]) == 1):
            if(csp[neighbour] == val):
                return False
    return True

#Backtracking algorithm
def CSP_Backtracking(assigned):

    #1. If assignment A is complete then return A
    #print("assigned len:", len(assigned), " adjDict length:", len(adjStatesDict))
    if len(assigned) == len(adjStatesDict):
            return assigned

    #2. X ? select a variable not in A
    #var = first_unassigned_variable(assigned, adjStatesDict)
    var = fetch_state(assigned, csp)

    #3. D ? select an ordering on the domain of X
    if(var != ''):
        domainVals = csp[var]

    #4. For each value v in D do
    for val in domainVals:
        #If X = v is consistent with A
        if valueConsistent(var,val):
            #Add (X?v) to A then
            assigned[var] = val;
            #print(var," : ", val)
            #print(len(assigned))
            #print(assigned)
            #remove from csp
            csp[var] = val
            tempVal = val

            listNeigh = []
            for state in adjStatesDict.keys():
                if state == var:
                    listNeigh = list(adjStatesDict[state])
                    break

            for neighbour in listNeigh:
                if val in csp[neighbour]:
                    csp[neighbour].remove(val)

            #result ? CSP-BACKTRACKING(A)
            result = CSP_Backtracking(assigned)
            #If result != failure then return result
            if(result != False):
                return result
            #Remove (X?v) from A

            del assigned[var]
            domainList = []
            domainList = list(cspStatic[var])
            domainList.remove(val)
            csp[var] = domainList
            cspStatic[var] = domainList

            for neighbour in listNeigh:
                if(val not in csp[neighbour]):
                    list(csp[neighbour]).append(tempVal)

            countBacktracks = countBacktracks + 1

    return False

if __name__ == "__main__":

    # Getting input arguments for legacy constraints file
    if len(sys.argv) == 2:
        legacyConstraintFile= sys.argv[1]
    else:
        print("\n ERROR : Missing the input argument\n\n************ USABILITY ************")
        print("python radio.py [legacy_constraint_file]")
        sys.exit();

    print("\n****** INPUT ARGUMENTS *********\n\n Legacy Constraint FileName: ", legacyConstraintFile)

    adjStatesDict = {}
    states = []
    constraintsDict = {}

    with open(legacyConstraintFile, 'r') as constraintFile:
        for constraintLine in constraintFile:
            adjArray = []
            cons = constraintLine.split()
            if(len(cons) > 0):
                constraintsDict[cons[0]] = cons[1]

    with open("adjacent-states", 'r') as file:
        for line in file:
            adjArray = []
            states = line.split()
            for i in range(1,len(states)):
                adjArray.append(states[i])
            adjStatesDict[states[0]] = adjArray
            if states[0] in constraintsDict.keys():
                csp[states[0]] = constraintsDict[states[0]]
                cspStatic[states[0]] = constraintsDict[states[0]]
            else:
                csp[states[0]] = ['A','B','C','D']
                cspStatic[states[0]] = ['A','B','C','D']
            #csp[states[0]] = ['A','B','C','D']


    #print("\n adjStatesDict dictionary count:\n", len(adjStatesDict))

    result = CSP_Backtracking(assignedStatesDict)
    #print(len(result))
    with open('results.txt', 'w') as resultFile:
        for state in result.keys():
            resultFile.write(state)
            resultFile.write(' ')
            resultFile.write(result[state])
            resultFile.write('\n')
    resultFile.close()

    #print(result)
    print("\nNumber of Backtracks:", countBacktracks)



