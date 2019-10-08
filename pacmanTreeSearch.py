# Autor: Tiberio Baptista,   n81258
#       Francisco Aires,    n*****

from functools import reduce

from tree_search import *

from math import *



def nodeCommandPrint(node):
    if node.parent != None:
        return nodeCommandPrint(node.parent) + [node.arg4]
    return [node.arg4]


class PacDomain(SearchDomain):
    def __init__(self, map, info):
        self.map = map
        self.info = info

    def actions(self, state):
        """Acções possiveis do pacman"""
        [x, y] = state

        actlist = []
        # W
        if not self.map.is_wall((x, y - 1)):
            actlist.append([state, [x, y - 1], 'w'])
        # A
        if not self.map.is_wall((x - 1, y)):
            actlist.append([state, [x - 1, y], 'a'])
        # S
        if not self.map.is_wall((x, y + 1)):
            actlist.append([state, [x, y + 1], 's'])
        # D
        if not self.map.is_wall((x + 1, y)):
            actlist.append([state, [x + 1, y], 'd'])
        return actlist

    def result(self, state, action):
        """Resultado"""
        actionRes = list(action[0])
        if list(state) == actionRes:
            return action[1]

    def cost(self, state, action):
        """Calculo do custo"""
        x1, y1 = state
        x2, y2 = action[1]


        cost = abs(x1 - x2) + abs(y1 - y2)

        return cost

    # Heuristic is Manhattan (abs(xs - xg) + (abs(ys - yg))
    def heuristic(self, state, goal_state):
        """Heuristica Mannathan (abs(xs - xg) + (abs(ys - yg))"""
        x1, y1 = state
        x2, y2 = goal_state

        result = abs(x1 - x2) + abs(y1 - y2)
        print("\tHEURISTIC: ", state, " <-> ", goal_state, " ->" ,result)
        return result

    def satisfies(self, state, goal):
        return list(state) == list(goal)

    def equivalent(self, state1, state2):
        return list(state1) == list(state2)


class PacTree(SearchTree):

    def __init__(self, problem, strategy='astar'):
        super().__init__(problem, strategy)
        self.solution_cost = 0
        self.tree_size = 0
        self.open_nodes[0].arg3 = 0
        self.commands = []


    def astar_add_to_open(self, lnewnodes):

        sortedRest = sorted(self.open_nodes + lnewnodes[:],
                                 key=lambda n: n.arg3 + self.problem.domain.heuristic(n.state, self.problem.goal))

        print("\tRESULT OF ADD_TO_OPEN: ",sortedRest)
        self.open_nodes = sortedRest

        return

    def search2(self):
        """Pesquisa para o proximo node"""
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            print("\t-----NEXT NODE----")
            print("\tCurrent node: ", node)
            print("\tThis node's cost: ", node.arg3)
            print("\tThis node's path: ", self.get_path(node))
            print("\tThis node's commmands: ", self.commands)

            if self.problem.goal_test(node.state):
                self.solution_cost = node.arg3

                self.tree_size += 1

                print("\t\t\t\t\tRecursive hell: ", nodeCommandPrint(node)[1:])
                self.commands = nodeCommandPrint(node)[1:]

                print("\tSize of tree: ", self.tree_size)
                return self.get_path(node), self.commands

            lnewnodes = []
            a = self.problem.domain.actions(node.state)
            print("\tActions to consider : ", a)
            for a in a:
                print("\t\t--NEXT ACTION--\n\t\t", a)
                self.tree_size += 1

                newstate = self.problem.domain.result(node.state, a)
                print("\t\tnewstate: ", newstate)

                newnodecost = node.arg3 + self.problem.domain.cost(node.state, a)
                print("\t\tnewnodecost: ", newnodecost)
                newnode = SearchNode(newstate, node, arg3=newnodecost, arg4=a[-1])
                print("\t\tnewnode: ",newnode)

                if(newstate not in self.get_path(node)):
                    print("\t\t[", newstate, "] IS NOT IN ", self.get_path(node))
                    lnewnodes += [newnode]

            self.add_to_open(lnewnodes)

        return None


def formulatePacman(domain, initial, tovisit):
    return SearchProblem(domain, initial, tovisit)


def solvePacman(p, strategy):
    t = PacTree(p, strategy)
    solution = t.search2()
    return solution
