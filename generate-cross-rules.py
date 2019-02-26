#!/bin/python

def toStr(a,b,c):
    return str(a)+str(b)+str(c)

count_literals = 153
count_rules = 9 * 9 * 8 * 2

path = './cross-rules.txt'
rules = open(path,'w+')
rules.write('p cnf ' + str(count_literals) + ' ' + str(count_rules) +'\n')
    
for i in range(1,10):
    for j in range(1,10):
        for num in range (1,10):
            #first diameter
            if(i == j):
                for k in range (1,10):
                    if(k==i):
                        continue
                    rules.write('-' + toStr(i,i,num)+' ' + '-' + toStr(k,k,num) +' 0\n')
                    
            if (i+j==10):
                for k1 in range (1,10):
                    for k2 in range (1,10):
                        if (k1==i and k2==j): continue
                        if (k1+k2==10):
                            rules.write('-' + toStr(i,j,num)+' ' + '-' + toStr(k1,k2,num) +' 0\n')

rules.close()
print(count_rules)

