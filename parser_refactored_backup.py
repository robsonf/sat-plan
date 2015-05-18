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
    os.system("./zchaff64/zchaff cnf > result_solver.txt")
    #os.system("rm cnf")

def is_solution():
    output_solver = open("result_solver.txt").read()
    return "RESULT:	SAT" in output_solver

def extract_plan(variables, action_fluents):
    iter_solver = iter(open("result_solver.txt").readlines())
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

def output_list(l):
    output_file = open('output_list.txt','a')
    output_file.write(str(l) + '\n')
    output_file.close()

def output_lattex(l):
    output_file = open('output_lattex.txt','a')
    output_file.write(l[0] + ' & ' + str(l[1]) + ' & ' + str(l[2]) + ' & ' + str(l[3]) + ' & ' + "%.2f" % round(l[4],2) + ' \\\\ \n')
    output_file.close()
    
def output_chart():
    return

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
    #parser.add_argument('-i','--input', help='help', default = 'cake.strips')
    parser.add_argument('-f','--input', help='help', default = 'domains/Blocks-Ground/')
    args = parser.parse_args()
    files_input = open(args.input+'files_input').read().split('\n')
    files_input = files_input[:len(files_input)-1]
    output_lines = []
    #print [file_name for file_name in files_input]
    for file_name in files_input:
        initial_time = clock()
        problem = Problem.read_strips(args.input+file_name)
        #problem = Problem.read_strips(args.input)
        time = 0
        while(True):
            time = time + 1
            variables, clauses = clauses_extractor(time, problem)
            export_cnf(variables, clauses)
            run_solver()
            if is_solution():
                plan = extract_plan(variables, problem.action_fluents)
                break
        output_line = [file_name] + [len(variables)] + [len(clauses)] + [len(plan)] + [clock()-initial_time] + [plan]
        output_list(output_line)
        output_lattex(output_line)
        #output_lines.append([file_name] + [len(variables)] + [len(clauses)] + [len(plan)] + [clock()-initial_time] + [plan])
    #return output_lines
    
main()
