from random import random, randint, choice
from copy import deepcopy
from math import log

from PIL import Image, ImageDraw

class fwrapper:
    def __init__(self, function, childcount, name):
        self.function = function
        self.childcount = childcount
        self.name = name


class node:
    def __init__(self, fw, children):
        self.function = fw.function
        self.name = fw.name
        self.children = children

    def evaluate(self, inp):
        results = [n.evaluate(inp) for n in self.children]
        return self.function(results)

    def display(self, indent=0):
        print(' '*indent+self.name)
        for c in self.children:
            c.display(indent+4)


class paramnode:
    def __init__(self, idx):
        self.idx = idx

    def evaluate(self, inp):
        return inp[self.idx]

    def display(self, indent=0):
        print('%sp%d' % (' '*indent, self.idx))


class constnode:
    def __init__(self, v):
        self.v = v

    def evaluate(self, inp):
        return self.v

    def display(self, indent=0):
        print('%s%d' % (' '*indent, self.v))



addw = fwrapper(lambda l:l[0]+l[1], 2, 'add')
subw = fwrapper (lambda l:l[0]-l[1], 2, 'subtract')
mulw = fwrapper (lambda l:l[0]*l[1], 2, 'multiply')

def iffunc(l):
    if l[0]>0: return l[1]
    else: return l[2]

ifw = fwrapper(iffunc, 3, 'if')


def isgreater(l):
    if l[0]>l[1]: return 1
    else: return 0

gtw = fwrapper(isgreater, 2, 'isgreater')

flist = [addw, mulw, ifw, gtw, subw]

#  *******************  Examples used for tests

def exampletree():
    return node(ifw, [
                        node(gtw, [paramnode(0), constnode(3)]),
                        node(addw, [paramnode(1), constnode(5)]),
                        node(subw, [paramnode(1), constnode(2)]),
                     ]
                )

def exampletree2():
    return node(ifw, [
                        node(gtw, [paramnode(0), constnode(3)]),
                        node(mulw, [paramnode(1), node(addw, [paramnode(1), constnode(5)])]),
                        node(subw, [paramnode(1), constnode(2)]),
                     ]
                )


#  *******************  End of test examples

def makeRandomTree(pc, maxdepth=5, fpr=0.5, ppr=0.6):
    if random()<fpr and maxdepth>0:
        f=choice(flist)
        children=[makeRandomTree(pc, maxdepth-1, fpr, ppr)
                  for i in range(f.childcount)]
        return node(f, children)
    elif random()<ppr:
        return paramnode(randint(0, pc-1))
    else:
        return constnode(randint(0, 10))



def mutate(t, pc, probchange=0.1):
    if random()<probchange:
        return makeRandomTree(pc)
    else:
        result = deepcopy(t)
        if isinstance(t, node):
            result.children = [mutate(c, pc, probchange) for c in t.children]
        return result

  
def crossover(t1, t2, probswap=0.7, top=1):
    if random()<probswap and not top:
        return deepcopy(t2)
    else:
        result = deepcopy(t1)
        if isinstance(t1, node) and isinstance(t2, node):
            result.children = [crossover(c, choice(t2.children), probswap, 0) for c in t1.children]
        return result


def evolve(pc, popsize, rankfunction, maxgen=50, mutationrate=0.1, breedingrate=0.4, pexp=0.7, pnew=0.05):

    # selectindex returns a random number, trending towards lower numbers. The lower
    # pexp is, the more lower numbers returned
    def selectRandomIndex():
        return int(log(random())/log(pexp))

    # create a random initial population
    found = False
    population = [makeRandomTree(pc) for i in range(popsize)]
    for i in range(maxgen):
        rankedProgramsByScore = rankfunction(population)
        print('lowest score: ', rankedProgramsByScore[0][0])
        if rankedProgramsByScore[0][0]==0:
            found = True
            break

        # the best two always make it
        newpop = [rankedProgramsByScore[0][1], rankedProgramsByScore[1][1]]

        # build the next generation
        while len(newpop)<popsize:
            if random()>pnew:
                newpop.append(mutate(
                                    crossover(
                                        rankedProgramsByScore[selectRandomIndex()][1], 
                                        rankedProgramsByScore[selectRandomIndex()][1], 
                                        probswap=breedingrate),
                                    pc, 
                                    probchange=mutationrate))
            else:
                # add a random node to mix things up
                newpop.append(makeRandomTree(pc))

        population=newpop

    if not found: print('Run limit of %s reached' % maxgen)
    rankedProgramsByScore[0][1].display()
    return rankedProgramsByScore[0][1]



#def getwidth(tree):
#    if isinstance(tree, node): return leng(tree.children)
#    elif isinstance(tree, 


def gridgame(p, boardsize=4, maxmoves=30):
    # Board size 4 by default
    max = (boardsize-1,boardsize-1)

    # Remember the last move
    lastmove = [-1,-1]

    # Remember the players's locations
    location = [[randint(0, max[0]), randint(0, max[1])]]

    # Put the second player a sufficent distance from the first
    location.append([(location[0][0]+2)%4, (location[0][1]+2)%4])

    # maximum of maxmoves moves before a tie
    for o in range(maxmoves):

        # For each player
        for i in range(2):
            gameState = location[i][:] + location[1-i][:]
            gameState.append(lastmove[i])
            move = p[i].evaluate(gameState)%4

            print('location before move for player %s : ' % i, ' move is: %s ' % move, location)

            # You lose if you move the same direction twice in a row
            if lastmove[i]==move: return i-1
            lastmove[i] = move

            # Make move and check for board limits
            if move==0:
                location[i][0] -= 1
                if location[i][0]<0: location[i][0] = 0
            if move==1:
                location[i][0] += 1
                if location[i][0]>max[0]: location[i][0] = max[0]
            if move==2:
                location[i][1] -= 1
                if location[i][1]<0: location[i][1] = 0
            if move==3:
                location[i][1] += 1
                if location[i][1]>max[1]: location [i][1] = max[1]

            print('location after move for player %s : ' % i, location)

            # You win if you have captured the other player 
            if location[i][0]==location[i-1][0] and location[i][1] == location[i-1][1]: return i

    return -1


def tournament(programList):
    # Count losses
    losses=[0 for p in programList]

    # Every player plays every other player
    for i in range(len(programList)):
        for j in range(len(programList)):
            if i==j: continue  # Don't play against yourself

            # Who is the winner?
            winner = gridgame([programList[i], programList[j]])

            # Two points for a loss, one point for a tie
            if winner==0:
                losses[j] += 2
            elif winner==1:
                losses[i] += 2
            elif winner==-1:
                losses[i] += 1
                losses[j] += 1;

    # Sort and return the results
    z_list = list(zip(losses, programList))
    z_list.sort(key=lambda score: score[0])
    return z_list


class humanplayer:
    def evaluate(self, board, boardsize=4):
        # Get my location and the location of other players
        me = tuple(board[0:2])
        others = [tuple(board[x:x+2]) for x in range(2, len(board)-1, 2)]

        # Display the board
        for i in range(boardsize):
            for j in range(boardsize):
                if (i,j) == me:
                    print('0', end=' ')
                elif (i,j) in others:
                    print('X', end=' ')
                else:
                    print('.', end=' ')
            print('')

        # Show moves for reference
        print('Your last move was %d' % board[len(board)-1])
        print(' O')
        print('2  3')
        print(' 1')
        print('Enter Move: ')

        move = int(input())
        return move












