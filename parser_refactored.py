# -*- coding: UTF-8 -*-
import os
from time import clock
from string import digits,letters
from clauses_manipulation import clauses_extractor, get_literal
from problem import Problem

import argparse


def export_cnf(variables, clauses):
    cnf_file = open('cnf','w')
    #cnf_file.write(" c "+str(variables)+"\n")
    cnf_file.write('p cnf '+str(len(variables))+' '+str(len(clauses)) + '\n')
    for l in clauses:
        cnf_file.write(l + ' 0\n')
    cnf_file.close()

def run_solver():
    os.system("./zchaff64/zchaff cnf > result.txt")
    #os.system("rm cnf")

def is_solution():
    output_solver = open("result.txt").read()
    return "RESULT:	SAT" in output_solver

def extract_plan(variables, action_fluents):
    iter_solver = iter(open("result.txt").readlines())
    while iter_solver.next() != "Instance Satisfiable\n":
        continue 
    aux = iter_solver.next().split()
    # valoração das variáveis das cláusulas que são verdadeiras
    model = [int(id) for id in aux[:aux.index('Random')]]
    #print model
    plan = []
    for m in model:
        l = get_literal(variables,m)
        action_name = l.translate(None, digits)
        if action_name in action_fluents:
            plan.append(action_name)
            #plan.append(l) 
            #l.translate(None, letters + '~')
    #print 'plan:<'+';'.join(plan)+'>'
#    aux = open("result.txt","a")
#    aux.write(str(variables))
#    aux.close()
    return plan

'''
TODO: ESTATÍSTICAS
plano com tabela de símbolos,
número de proposições (variáveis) e
número de cláusulas da CNF, 
tamanho do plano solução, 
tempo para encontrar o plano (incluindo o tempo de geração da CNF).
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', help='foo help', default = 'cake.strips')
    args = parser.parse_args()

    initial_time = clock()
    #problem = Problem.read_strips(file_name)

    problem = Problem.read_strips(args.input)
    time = 0
    while(True):
        time = time + 1
        variables, clauses = clauses_extractor(time, problem)
        export_cnf(variables, clauses)
        run_solver()
        if is_solution():
            plan = extract_plan(variables, problem.action_fluents)
            break
    return plan, len(variables), len(clauses), len(plan), clock()-initial_time

print main()
