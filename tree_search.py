# Modulo: tree_search
# 
# Fornece um conjunto de classes para suporte a resolucao de 
# problemas por pesquisa em arvore:
#    SearchDomain  - dominios de problemas
#    SearchProblem - problemas concretos a resolver 
#    SearchNode    - nos da arvore de pesquisa
#    SearchTree    - arvore de pesquisa, com metodos para 
#                    a respectiva construcao
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2018,
#  Inteligência Artificial, 2014-2018

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):
    """ Dominios de pesquisa permitem calcular as accoes possiveis em cada estado, etc"""

    @abstractmethod
    def __init__(self):
        """construtor"""
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        """lista de accoes possiveis num estado"""
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        """resultado de uma accao num estado, ou seja, o estado seguinte"""
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        """custo de uma accao num estado"""
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal_state):
        """custo estimado de chegar de um estado a outro"""
        pass

    # comparacao de estados (devolve True se estados foram equivalentes)
    @abstractmethod
    def equivalent(self, state1, state2):
        """comparacao de estados (devolve True se estados foram equivalentes)"""
        pass

    # devolve True se goal satisfeito no state
    @abstractmethod
    def satisfies(self, state, goal):
        """devolve True se goal satisfeito no state"""
        pass

class SearchProblem:
    """ Problemas concretos a resolver dentro de um determinado dominio"""
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)
        

class SearchNode:
    """Nos de uma arvore de pesquisa"""
    def __init__(self,state,parent,arg3=None,arg4=None,arg5=None):
        self.state = state
        self.parent = parent
        self.arg3 = arg3
        self.arg4 = arg4
        self.arg5 = arg5
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + "," + str(self.arg4) + ")"
    def __repr__(self):
        return str(self)

class SearchTree:
    """Arvores de pesquisa"""
    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.strategy = strategy


    def get_path(self,node):
        """Obter o caminho (sequencia de estados) da raiz ate um no"""
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self):
        """Procurar solução"""
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                return self.get_path(node)
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                lnewnodes += [SearchNode(newstate,node)]
            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        """Juntar novos nos a lista de nos abertos de acordo com a estrategia"""
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.uniform_add_to_open(lnewnodes)
        elif self.strategy == 'astar':
            self.astar_add_to_open(lnewnodes)

