import dill
import gp



with open('Gridgame01.pkl', 'rb') as f:
    winner = dill.load(f)

winner.display()

i = gp.gridgame([winner, gp.humanplayer()])

if i == 0: print('Haha beaten by a dumb robot!')
elif i == 1: print('You win!!')
else: print('Game is a tie!')

