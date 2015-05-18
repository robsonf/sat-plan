d = 'domains/Satellite-ground/'
f1 = open(d+'/files_input').read().split('\n')
f1 = f1[:len(f1)-1]
for l1 in f1:
    faux = open(d+'/'+l1).read().split('\n\n')
    f3 = open(d+'/'+l1,'w')
    for f2 in faux:
        lines = f2.split('\n')
        for l2 in lines:
            aux = ''
            l3 = l2.split(';')
            if len(l3) > 1:
                for e in l3[:len(l3)-1]:
                    aux += e + '_;'
            aux += l3[-1] + '_\n'
            f3.write(aux)
        f3.write('\n')
    f3.close()
