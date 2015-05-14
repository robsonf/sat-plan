# -*- coding: UTF-8 -*-
import itertools

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

def clauses_extractor(time, problem):
    # o valor do indice do elemento da lista de variaveis
    # corresponde ao literal utilizado na cnf, exemplo:
    # 1 haveCake0
    # 2 eatenCake0
    variables = []

    # recupera elementos das estruturas para popular lista de variaveis
    # para i = 1 ate i = t-1
    for i in range(time):
    #   print 'nivel',i
       for f in problem.predicate_fluents:
           variables.append(f + str(i)) 
       for f in problem.action_fluents:
           variables.append(f + str(i))
    else:
       i = i+1
    #   print 'nivel',i+1   
       for f in problem.predicate_fluents:
           variables.append(f + str(i))

    # lista de cláusulas no formato DIMACS
    clauses = []

    # adiciona estado inicial a lista de clausulas
    for p in problem.initial:
    #    print p
        clauses.append(get_literal_id(variables,p+'0'))
    # adiciona os fluentes negados para o estado inicial
    for p in problem.predicate_fluents:
        if p not in problem.initial:
            clauses.append(get_literal_id(variables,not_literal(p)+'0'))
    # adiciona objetivo a lista de clausulas
    for p in problem.goal:
    #    print p
        clauses.append(get_literal_id(variables,p+str(time)))
    #print clauses

    # extrair axiomas de precondições, efeitos, persistencia, continuidade e não-paralelismo
    for i in range(time):
        for a in problem.actions:
           for p in a.prec:
               clauses.append(get_literal_id(variables, not_literal(a.name)+str(i)) + " " + get_literal_id(variables, p+str(i)))
           for p in a.eff:
               clauses.append(get_literal_id(variables, not_literal(a.name)+str(i)) + " " + get_literal_id(variables, p+str(i+1)))
           # extrair axioma de persistencia           
           for p in problem.predicate_fluents:
              if p not in a.eff and not_literal(p) not in a.eff:
                  clauses.append(get_literal_id(variables, not_literal(a.name)+str(i)) + " " + get_literal_id(variables, not_literal(p)+str(i))  + " " + get_literal_id(variables, p+str(i+1)))
                  clauses.append(get_literal_id(variables, not_literal(a.name)+str(i)) + " " + get_literal_id(variables, p+str(i))  + " " + get_literal_id(variables, not_literal(p)+str(i+1)))
        # extrair axioma de continuidade de plano
        clauses.append(" ".join([get_literal_id(variables, a.name+str(i)) for a in problem.actions]))
        # extrair axioma de não-paralelismo
        combination_actions = [j for j in itertools.combinations(problem.action_fluents, 2)]
        clauses = clauses + [get_literal_id(variables, not_literal(ca[0])+str(i)) + " " + get_literal_id(variables, not_literal(ca[1])+str(i)) for ca in combination_actions]

    return variables, clauses
