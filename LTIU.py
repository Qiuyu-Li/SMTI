import time
import random
import sys
# Needed to hide warnings in the matplotlib sections
import warnings
import argparse

# -*- coding: utf-8 -*-
"""LTIU-knuth.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1wd7Yc6wMJm5OQ7VymISiu7nF6lIxEj4G
"""

# -*- coding: utf-8 -*-
"""
This file contains the implementation of Local search model for MAX-SMTI problem,
based on the paper "Local Search Approaches in Stable Matching Problems" by Mirco Gelain , Maria Silvia Pini , Francesca Rossi , K. Brent Venable  and Toby Walsh.
Last modified: 04.12.2020 - İlayda Begüm İzci
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline


warnings.filterwarnings("ignore")


def match(men_size, women_size):
    if men_size > women_size:
        n = women_size
    else:
        n = men_size
    men = random.sample(list(range(1, men_size + 1)), n)
    women = random.sample(list(range(1, women_size + 1)), n)
    return list(zip(men, women))


def find_index(a_list, s):
    # if s is -1 return the length so that to find blocking pairs all the pref_list will be scanned in findblockingpairs function
    if s == -1:
        return len(a_list)
    if s in a_list:
        return a_list.index(s)
    else:
        for el in a_list:
            if isinstance(el, tuple):
                if s in el:
                    return a_list.index(el)
    return -1


def findBlockingPairs(matching, men_pref, women_pref):
    blocking_pairs = [(-1, -1)]
    match_dict = dict(matching)
    reverse_bpairs = {}
    for man in men_pref.keys():
        if match_dict.get(man) != None:
            index = find_index(men_pref[man], match_dict.get(man))
            if index == -1:  # unacceptable pair, should break them
                index = len(men_pref[man])
                matching.remove((man, match_dict.get(man)))
        else:
            index = len(men_pref[man])

        for ind in range(index):
            woman = men_pref[man][ind]
            if isinstance(woman, tuple):  # if there is a tie
                for wom in woman:
                    my_rank = find_index(women_pref[wom], man)
                    if wom in list(match_dict.values()):  # if she is not single
                        currentP = list(match_dict.keys())[list(match_dict.values()).index(wom)]
                        currentP_rank = find_index(women_pref[wom], currentP)
                    else:
                        currentP_rank = -1
                    other_couple = [p for p in blocking_pairs if p[1] == wom]
                    if currentP_rank == -1 or currentP_rank > my_rank:
                        if len(other_couple) == 0:
                            blocking_pairs.append((man, wom))
                            break
                        elif find_index(women_pref[wom], other_couple[0][0]) > my_rank:
                            blocking_pairs.append((man, wom))
                            blocking_pairs.remove(other_couple[0])
                            break
                    if blocking_pairs[-1][0] == man:
                        break
                if blocking_pairs[-1][0] == man:
                    break
            else:
                my_rank = find_index(women_pref[woman], man)
                if woman in list(match_dict.values()):  # if she is not single
                    currentP = list(match_dict.keys())[list(match_dict.values()).index(woman)]
                    currentP_rank = find_index(women_pref[woman], currentP)
                else:
                    currentP_rank = -1
                other_couple = [p for p in blocking_pairs if p[1] == woman]
                if currentP_rank == -1 or currentP_rank > my_rank:
                    if len(other_couple) == 0:
                        blocking_pairs.append((man, woman))
                        break
                    elif find_index(women_pref[woman], other_couple[0][0]) > my_rank:
                        blocking_pairs.append((man, woman))
                        blocking_pairs.remove(other_couple[0])
                        break
    return blocking_pairs[1:]


# being matched with -1=being single
# add blocking pair and make their partners single
def newStategenerator(stateM, blockingpair):
    matching = stateM.copy()
    couple1 = [c for c in matching if c[0] == blockingpair[0]]
    couple2 = [c for c in matching if c[1] == blockingpair[1]]
    matching.append(blockingpair)
    if len(couple1) != 0:
        matching.remove(couple1[0])
    if len(couple2) != 0:
        matching.remove(couple2[0])
    return matching


class Problem(object):

    def __init__(self, initial=None, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):        raise NotImplementedError

    def result(self, state, action): raise NotImplementedError

    def is_goal(self, state):        return state == self.goal

    def action_cost(self, s, a, s1): return 1

    def h(self, node):               return 0  # value of the state: calculated with the help of heuristic function

    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)


class SMTI(Problem):
    def __init__(self, initial, women_pref, men_pref, msize, wsize):
        Problem.__init__(self, initial)
        self.women_pref = women_pref
        self.men_pref = men_pref
        self.msize = msize
        self.wsize = wsize

    def actions(self, state):
        return findBlockingPairs(state, self.men_pref, self.women_pref)

    def result(self, state, action):
        new_state = newStategenerator(state, action)
        blockingPairs = findBlockingPairs(new_state, self.men_pref, self.women_pref)
        return new_state, blockingPairs

    def value(self, blp, state):  # number of undominated bp+number of singles
        ns = self.msize - len(state)
        ns += self.wsize - len(state)
        return len(blp) + ns


class Node:

    def __init__(self, state, bp, parent=None):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.bp = bp  # number of undominated bp

    def __repr__(self):
        return "<Node {}>".format(self.state)

    """def __lt__(self, node):
      return self.state < node.state"""

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state, next_bp = problem.result(self.state, action)
        next_node = Node(next_state, next_bp, self)
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


def hill_climbing(problem):
    iterations = 50000  # kaç yapmak istersek
    TOTAL_TIME = 0
    current = Node(problem.initial, findBlockingPairs(problem.initial, problem.men_pref, problem.women_pref))
    best_stable_node_so_far = None
    best_node_so_far = current
    val = 50000
    fail_to_update = 0
    while TOTAL_TIME < 1990 and iterations:
        # print("------------------------------")
        # print("iteration number: ",iterations)
        START_TIME = time.time()
        old_val = val
        val = problem.value(current.bp, current.state)
        if val == 0:
            return current, 50000 - iterations
        if val == old_val:
            fail_to_update += 1
        if fail_to_update >= 10:
            return current, 50000 - iterations
        if val < problem.value(best_node_so_far.bp, best_node_so_far.state):  # update best node so far
            best_node_so_far = current
        neighbors = current.expand(problem)
        if not neighbors:  # we already now it is not perfect but if no neighbors then ramdom restart to find perfect matching
            if best_stable_node_so_far == None or val < problem.value(best_stable_node_so_far.bp,
                                                                      best_stable_node_so_far.state):
                best_stable_node_so_far = current
            current = Node(match(problem.msize, problem.wsize),
                           findBlockingPairs(problem.initial, problem.men_pref, problem.women_pref))
        else:
            values = [problem.value(node.bp, node.state) for node in neighbors]
            # print("values of neighbor: ",values)
            minimum = min(values)
            indices = [i for i, v in enumerate(values) if v == minimum]
            neighbor = neighbors[random.choice(indices)]
            # print("chosen neighbor: ",neighbor,"its value is: ",problem.value(neighbor.bp,neighbor.state))
            if random.random() < 0.8:
                current = neighbor
            else:
                current = neighbors[random.randrange(0, len(neighbors))]
            iterations -= 1
        LOOP_TIME = time.time()
        TOTAL_TIME += LOOP_TIME - START_TIME
    if best_stable_node_so_far != None:
        return best_stable_node_so_far, 50000 - iterations  # if couldnt find a perfect match after iterations return best stable so far
    else:
        print("printed best so far", "left iterations", iterations)
        return best_node_so_far, 50000 - iterations


def LTIU():
    inputF = "test_instance.txt"

    with open(inputF) as fp:
        lines = fp.readlines()

    mensize = int(lines[1])
    womensize = int(lines[2])
    menprefDict = {key: [] for key in range(1, int(mensize) + 1)}
    womenprefDict = {key: [] for key in range(1, int(womensize) + 1)}
    for line in lines[3:int(mensize) + 3]:
        preferencesM = line.split()
        tupl = []
        for p in range(1, len(preferencesM)):
            if '(' in preferencesM[p] and ')' in preferencesM[p]:
                menprefDict[int(preferencesM[0])].append(int(preferencesM[p][1:-1]))
            elif ')' in preferencesM[p]:
                tupl.append(int(preferencesM[p][:-1]))
                menprefDict[int(preferencesM[0])].append(tuple(tupl))
                tupl = []
            else:
                if '(' in preferencesM[p]:
                    tupl.append(int(preferencesM[p][1:]))
                else:
                    tupl.append(int(preferencesM[p]))

    for line in lines[int(mensize) + 3:]:
        preferencesW = line.split()
        tupl = []
        for p in range(1, len(preferencesW)):
            if '(' in preferencesW[p] and ')' in preferencesW[p]:
                womenprefDict[int(preferencesW[0])].append(int(preferencesW[p][1:-1]))
            elif ')' in preferencesW[p]:
                tupl.append(int(preferencesW[p][:-1]))
                womenprefDict[int(preferencesW[0])].append(tuple(tupl))
                tupl = []
            else:
                if '(' in preferencesW[p]:
                    tupl.append(int(preferencesW[p][1:]))
                else:
                    tupl.append(int(preferencesW[p]))

    smti = SMTI(match(mensize, womensize), womenprefDict, menprefDict, mensize, womensize)
    # print("initial state is",smti.initial)
    # print("men preferences are",menprefDict)
    # print("women preferences are",womenprefDict)
    sTime = time.time()
    node, numIterations = hill_climbing(smti)
    eTime = time.time()
    timePassed = eTime - sTime

    return timePassed
    #print("%s" % ("Run time: " + str(timePassed)))
    
    '''
    print("Number of steps: " + str(numIterations))
    print("%s" % ("Number of blocking pairs: " + str(len(node.bp))))
    print("%s" % ("Number of singles: " + str(smti.msize + smti.wsize - (2 * len(node.state)))))

    print("\nSolution:")
    for pair in node.state:
        print("%s" % str(pair))
    '''