# -*- coding: UTF-8 -*-
from action import Action
import itertools
import os
from string import digits,letters

f = open('cake.strips')

file = f.read().split('\n\n')

actions_file = file[0].split()
iter_actions_file = iter(actions_file)
init_goal_file = file[1].split()

variables = []

# testes para validar entrada
def verify_input():
    assert len(actions_file) % 3 == 0, "Número de ações não é múltiplo de 3."
    assert len(init_goal_file) == 2, "Número de linhas para Objetivo e Estado não está igual a 2."
    return True

verify_input()

# cada ação contém o nome da ação e listas de precondições e efeitos.
actions = []
for action_name in iter_actions_file:
     prec = iter_actions_file.next().split(';')
     eff = iter_actions_file.next().split(';')
     actions.append(Action(action_name, prec, eff))

initial = init_goal_file[0].split(';')
goal = init_goal_file[1].split(';')

# cria conjunto de fluentes de predicado e ações
predicate_fluents = set()
action_fluents = set([a.name for a in actions]) 
for action in actions:
    for f in action.prec + action.eff:
        predicate_fluents.add(f.replace('~',''))

# recupera o valor do literal na lista "l", a partir da variavel "e"
# remove o "~" antes de consultar na lista de variaveis
def get_literal_id(l, e):
    if(e[0]=="~"):
        return "-"+str(l.index(e[1::])+1)
    return str(l.index(e)+1)
def get_literal(l, e):
    if(e<0):
        return "~"+l[-1*e-1]
    return l[e-1]

# converte elemento "e" em sua negação
def not_literal(e):
    if(e[0]=="~"):
       return "-"+e
    return "~"+e

# converter clausulas em arquivo cnf no padrão DIMACS
def export_to_cnf(clauses,variables):
    cnf_file = open('cnf','w')
    cnf_file.write(" c "+str(variables)+"\n")
    cnf_file.write('p cnf '+str(len(variables))+' '+str(len(clauses)) + '\n')
    for l in clauses:
        cnf_file.write(l + ' 0\n')

def main(t):
    # o valor do indice do elemento da lista de variaveis
    # corresponde ao literal utilizado na cnf, exemplo:
    # 1 haveCake0
    # 2 eatenCake0
    variables = []

    # recupera elementos das estruturas para popular lista de variaveis
    # para i = 1 ate i = t-1
    for i in range(t):
    #   print 'nivel',i
       for f in predicate_fluents:
           variables.append(f + str(i)) 
       for f in action_fluents:
           variables.append(f + str(i))
    else:
       i = i+1
    #   print 'nivel',i+1   
       for f in predicate_fluents:
           variables.append(f + str(i))
    #print variables

    # lista de cláusulas
    clauses = []

    # adiciona objetivo e estado inicial a lista de clausulas
    for p in initial:
    #    print p
        clauses.append(get_literal_id(variables,p+'0'))
    for p in goal:
    #    print p
        clauses.append(get_literal_id(variables,p+str(t)))
    #print clauses

    # extrair axiomas de precondições, efeitos, persistencia, continuidade e não-paralelismo
    for i in range(t):
        for a in actions:
           for p in a.prec:
               clauses.append(get_literal_id(variables, not_literal(a.name)+str(i)) + " " + get_literal_id(variables, p+str(i)))
           for p in a.eff:
               clauses.append(get_literal_id(variables, not_literal(a.name)+str(i)) + " " + get_literal_id(variables, p+str(i+1)))
           # extrair axioma de persistencia           
           for p in predicate_fluents:
              if p not in a.eff and not_literal(p) not in a.eff:
                  clauses.append(get_literal_id(variables, not_literal(a.name)+str(i)) + " " + get_literal_id(variables, not_literal(p)+str(i))  + " " + get_literal_id(variables, p+str(i+1)))
                  clauses.append(get_literal_id(variables, not_literal(a.name)+str(i)) + " " + get_literal_id(variables, p+str(i))  + " " + get_literal_id(variables, not_literal(p)+str(i+1)))
           #clauses = clauses + axiom_persistence(a, predicate_fluents, i)

        # extrair axioma de continuidade de plano
        clauses.append(" ".join([get_literal_id(variables, a.name+str(i)) for a in actions]))
        # extrair axioma de não-paralelismo
        combination_actions = [j for j in itertools.combinations(action_fluents, 2)]
        clauses = clauses + [get_literal_id(variables, not_literal(ca[0])+str(i)) + " " + get_literal_id(variables, not_literal(ca[1])+str(i)) for ca in combination_actions]

    export_to_cnf(clauses,variables)
    return variables


def plan_extract(variables):
    iter_solver = iter(open("result.txt").readlines())
    while iter_solver.next() != "Instance Satisfiable\n":
        continue 
    aux = iter_solver.next().split()
    model = [int(id) for id in aux[:aux.index('Random')]]
    print model
    plan = []
    for m in model:
        l = get_literal(variables,m)
        action_name = l.translate(None, digits)
        if action_name in action_fluents:
            plan.append(action_name)
            #plan.append(l) 
            #l.translate(None, letters + '~')
    print 'plan:<'+';'.join(plan)+'>'


# t = tamanho do plano
t = 0
loop = True
while loop:
    t = t + 1
    variables = main(t)
    os.system("./zchaff-2/zchaff cnf > result.txt")
    solver_result = open("result.txt").read()
    if "RESULT:	SAT" in solver_result:
        loop = False
        plan_extract(variables)

