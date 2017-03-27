import gp
import time
from datetime import timedelta
import dill


print('************** start random1 ****')
random1 = gp.makeRandomTree(5)
random1.display()
print ('************* end of random1')

print('************** start random2 ****')
random2 = gp.makeRandomTree(5)
random2.display()
print ('************* end of random2')

print('The gamescore is: ', gp.gridgame([random1, random2]))

 
