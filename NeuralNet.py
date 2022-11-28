from random import randint
from itertools import product

class Genome:

    #inputPaths = []

    #internalPaths = []

    def __init__(self, inputs, internal, outputs) -> None:

        self.inputPaths = list(range(inputs))

        self.internalPaths = list(range(internal))
        
        for neuron in range(inputs):
            self.inputPaths[neuron] = (randint(0, internal-1), randint(0, 100)/100)
        for neuron in range(internal):
            self.internalPaths[neuron] = (randint(0, outputs-1), randint(0,100)/100)

class NeuralNet:

    numInputs = 4
    numInternal = 2
    numOutputs = 4

    numOfNeurons = numInputs + numInternal + numOutputs
    
    def __init__(self) -> None:
        
        self.genes = Genome(self.numInputs, self.numInternal, self.numOutputs)

        #Add the actual neural net connections

class Agent:

    def __init__(self):
        
        self.neuralNet = NeuralNet()
        """ This is how I was gonna do it but I decided to have each agent register with the board instead
        Now board will return their position after assigning it and making sure that there are no conflicts
        self.pos['x'] = randint(0, 255)
        self.pos['y'] = randint(0, 255)
        """

        self.pos = board.register(self)

    def act(self):

        up = self.checkUp()
        down = self.checkDown()
        left = self.checkLeft()
        right = self.checkRight()

        self.neuralNet.genes.inputPaths

    def checkUp(self):

        check = game.board.grid.check(self.pos[0], self.pos[1] + 1)

        return check

    def checkDown(self):

        check = game.board.grid.check(self.pos[0], self.pos[1] - 1)

        return check

    def checkLeft(self):

        check = game.board.grid.check(self.pos[0] - 1, self.pos[1])

        return check

    def checkRight(self):

        check = game.board.grid.check(self.pos[0] + 1, self.pos[1])

        return check

class Board:

    def __init__(self) -> None:
        
        self.grid = [[None for _ in range(255)] for _ in range(255)] # This makes a matrix of 255x255 filled with None-thing 
        # board[n][n] = i this is board[xcoord][ycoord] = what's in that spot

        self.agentList = []

    def register(self, agent) -> tuple:

        #index = len(self.agentList) Maybe use this to make a list of agents whose indexes are in board spots

        #self.agentList.append(agent)

        spaceOpen = True

        while(spaceOpen == True):

            x = randint(0,254)

            y = randint(0,254)

            space = self.check(x,y)

            if space != None:

                spaceOpen = False
        
        self.grid[x][y] = agent

        return (x,y)

    def check(self, x, y):

        return self.grid[x][y]

class Game:

    def __init__(self) -> None:

        self.board = Board()

        self.agentList = []

        for i in range(255): # This is where I instantiate every agent

            self.agent1 = Agent()

            self.agentList.append(self.agent1)

        for i in self.agentList:

            print(self.board.grid[i.pos[0]][i.pos[1]].neuralNet.genes.inputPaths)

        #{board.grid[agent1.pos[0]][agent1.pos[1]].neuralNet.genes.inputPaths}

    def tick(self):

        for i in self.agentList:
            
            i.act

game = Game()