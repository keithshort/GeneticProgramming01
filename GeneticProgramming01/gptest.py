import gp
import time
from datetime import timedelta
from random import random, randint, choice
import dill


exampletree = gp.exampletree()
exampletree.display()

print('Value for exampletree [2,3]: ', exampletree.evaluate([2,3]))
print('Value for exampletree [5,3]: ', exampletree.evaluate([5,3]))

exampletree2 = gp.exampletree2()
exampletree2.display()
print('Value for exampletree2 [2,3]: ', exampletree2.evaluate([2,3]))
print('Value for exampletree2 [5,3]: ', exampletree2.evaluate([5,3]))


print('************** start random1 ****')
random1 = gp.makeRandomTree(2)
random1.display()
print('Value for random1 using [7,1]: ', random1.evaluate([7,1]))
print ('************* end of random1')

print('************** start random2 ****')
random2 = gp.makeRandomTree(2)
random2.display()
print('Value for random2 using [1,7]: ', random2.evaluate([1,7]))
print ('************* end of random2')


def hiddenfunction(x, y):
    return (x**2) + (2*y) + (3*x) + 5

def buildhiddendataset():
    rows=[]
    for i in range(200):
        x = randint(0, 40)
        y = randint(0, 40)
        rows.append([x, y, hiddenfunction(x, y)])
    return rows


def scorefunction(tree, s):
    dif = 0
    for data in s:
        v = tree.evaluate([data[0], data[1]])
        dif += abs(v - data[2])
    return dif


def getrankfunction(dataset):
    def rankfunction(population):
        scores = [(scorefunction(t, dataset), t) for t in population]
        scores.sort(key=lambda score: score[0])   # sort by score
        return scores

    return rankfunction



hiddenset = buildhiddendataset()
print(hiddenset)
print ('**** hiddendataset built')

print('scorefunction for random1: ', scorefunction(random1, hiddenset))

print('scorefunction for random2: ', scorefunction(random2, hiddenset))

mttree = gp.mutate(random2, 2)
print('***** mutated random2: ')  
mttree.display()
print('end of mutated random2: ')

print('scorefunction for mutated random2: ', scorefunction(mttree, hiddenset))


cross = gp.crossover(random1, random2)
print('***** crossover random1 & random2: ')
cross.display()
print('end of crossedover random1 & random2') 

print('scorefunction for crossed trees: ', scorefunction(cross, hiddenset))

print('********* start of evolve run')
input('Press <ENTER> to continue')

rf = getrankfunction(hiddenset)

start = time.process_time()

finaltree = gp.evolve(2, 150, rf, mutationrate=0.2, breedingrate=0.1, pexp=0.7, pnew=0.1)

elapsed = (time.process_time() - start)
print("Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed)))

print(hiddenset[0])
print('Value using finaltree: ', finaltree.evaluate([hiddenset[0][0], hiddenset[0][1]]))
print('Value from hiddenset: ', hiddenset[0][2])

with open('gp_program.pkl', 'wb') as f:
    dill.dump(finaltree, f)

with open('gp_program.pkl', 'rb') as f:
    finaltree_new = dill.load(f)

finaltree_new.display()
