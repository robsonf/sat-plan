# -*- coding: UTF-8 -*-
from action import Action
class Problem:
    def __init__(self, actions, initial, goal):
        self.actions = actions
        self.initial = initial
        self.goal = goal

        predicate_fluents = set()
        for action in actions:
            for f in action.prec + action.eff:
                predicate_fluents.add(f.replace('~',''))
        self.predicate_fluents = predicate_fluents
        self.action_fluents = set([a.name for a in actions]) 

    def read_strips(file_name):
        file = open(file_name)
        strips_file = file.read().split('\n\n')
        actions_file = strips_file[0].split()
        iter_actions_file = iter(actions_file)
        init_goal_file = strips_file[1].split()
        # verica se entrada segue padrão correto 
        assert len(actions_file) % 3 == 0, "Número de ações não é múltiplo de 3."
        assert len(init_goal_file) == 2, "Número de linhas para Objetivo e Estado não está igual a 2."

        # cada ação guarda tem um nome, lista de precondições e efeitos
        actions = []
        for action_name in iter_actions_file:
             prec = iter_actions_file.next().split(';')
             eff = iter_actions_file.next().split(';')
             actions.append(Action(action_name, prec, eff))

        # conjunto de fluentes de predicado e ações
        initial = init_goal_file[0].split(';')
        goal = init_goal_file[1].split(';')
        return Problem(actions, initial, goal)
        
        
    def __str__(self):
        return "problem: " + str(self.initial) +" "+ str(self.goal)
    read_strips = staticmethod(read_strips)
