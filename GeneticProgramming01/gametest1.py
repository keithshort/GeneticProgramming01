import gp
import time
from datetime import timedelta
import dill


print('****** start of robotic game *****')
winner = gp.evolve(5, 100, gp.tournament, maxgen=50)
print('****** endof robotic game  *****')
winner.display()
print('end of winning program display')

input('Press <ENTER> to write winning program to a file')

with open('Gridgame01.pkl', 'wb') as f:
    dill.dump(winner, f)