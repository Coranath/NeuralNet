from random import randint
from itertools import product

STIMULATION_CUTOFF = 0.75
NUM_INPUT_NEURONS = 4 # These are directly connected to input so you can't change this number without adding new input manually
NUM_INTERNAL_NEURONS = 2
NUM_OUTPUT_NEURONS = 4 # Same as inputs, if you increase this number you have to add additional outputs manually

class Genome:

    #inputPaths = []

    #internalPaths = []

    def __init__(self, inputs, internal, outputs) -> None:

        self.inputPaths = list(range(inputs))

        self.internalPaths = list(range(internal))
        
        for neuron in range(inputs):
            self.inputPaths[neuron] = (randint(0, internal-1))#, randint(0, 100)/100)
        for neuron in range(internal):
            self.internalPaths[neuron] = (randint(0, outputs-1))#, randint(0,100)/100)

class Neuron:

    def __init__(self, backLinks):
        
        self.backLinks = backLinks

    def __call__(self, *args, **kwds):

        data = []

        stimuli = 0

        if type(self.backLinks) == list:
        
            for backLink in self.backLinks:

                data.append(backLink)

            for stimulusList in data:

                for stimulus in stimulusList:

                    stimuli += stimulus()

            meanOfStimuli = stimuli/len(data)
        else:

            #print(f'Backlink was not iterable, running as function. Backlink was {self.backLinks}')
            #print(self.backLinks())

            meanOfStimuli = self.backLinks()

        if meanOfStimuli > STIMULATION_CUTOFF:

            return 1 # If this neuron is stimulated above the cutoff then it returns a 1
        
        else: return 0
    


class NeuralNet:

    numOfNeurons = NUM_INPUT_NEURONS + NUM_INTERNAL_NEURONS + NUM_OUTPUT_NEURONS

    inputNeurons = []

    internalNeurons = []

    outputNeurons = []
    
    def __init__(self, parent) -> None:
        
        self.genes = Genome(NUM_INPUT_NEURONS, NUM_INTERNAL_NEURONS, NUM_OUTPUT_NEURONS)

        self.inputNeurons.append(Neuron(parent.checkUp))

        self.inputNeurons.append(Neuron(parent.checkDown))

        self.inputNeurons.append(Neuron(parent.checkLeft))

        self.inputNeurons.append(Neuron(parent.checkRight))

        for i in range(NUM_INTERNAL_NEURONS):

            internalNeuronBackLinks = [[],[]]

            for j in range(NUM_INPUT_NEURONS):
                if self.genes.inputPaths[j] == i:
                    #print(j, len(internalNeuronBackLinks), len(self.genes.inputPaths), len(self.inputNeurons))
                    internalNeuronBackLinks[self.genes.inputPaths[j]].append(self.inputNeurons[j])

            self.internalNeurons.append(Neuron(internalNeuronBackLinks))

        for i in range(NUM_OUTPUT_NEURONS):

            outputNeuronBackLinks = [[],[],[],[]]

            for j in range(NUM_INTERNAL_NEURONS):
                if self.genes.internalPaths[j] == i:
                    #print(j, self.genes.internalPaths[j], len(outputNeuronBackLinks), len(self.genes.internalPaths), len(self.internalNeurons))
                    outputNeuronBackLinks[self.genes.internalPaths[j]].append(self.internalNeurons[j])

            self.outputNeurons.append(Neuron(outputNeuronBackLinks))

    def think(self):

        choice = []

        for neuron in self.outputNeurons:

            choice = neuron()

            if choice > STIMULATION_CUTOFF:
                choice = neuron # Output which neuron we're on and break
                break

        decisionSelect = { #This is how you implement a switchesque capability in Python.
                0:'moveUp',
                1:'moveDown',
                2:'moveLeft',
                3:'moveRight'
                }
        
        return(decisionSelect.get(choice))


class Agent:

    def __init__(self, game):
        
        self.neuralNet = NeuralNet(self)
        """ This is how I was gonna do it but I decided to have each agent register with the board instead
        Now board will return their position after assigning it and making sure that there are no conflicts
        self.pos['x'] = randint(0, 255)
        self.pos['y'] = randint(0, 255)
        """

        self.pos = game.board.register(self)

    def act(self):

        decision = self.neuralNet.think()

        decisionSwitch = {
            'moveUp':self.moveUp,
            'moveDown':self.moveDown,
            'moveLeft':self.moveLeft,
            'moveRight':self.moveRight
        }

        move = decisionSwitch.get(decision)

        move()

    def checkUp(self):

        check = game.board.check(self.pos[0], self.pos[1] + 1) #returns whatever is in the spot

        if check == None:

            return 1 # Return 1 if the space is empty, this will tell the neuron that this is a valid path
        
        else: return 0

    def checkDown(self):

        check = game.board.check(self.pos[0], self.pos[1] - 1)

        if check == None:

            return 1 # Return 1 if the space is empty, this will tell the neuron that this is a valid path
        
        else: return 0

    def checkLeft(self):

        check = game.board.check(self.pos[0] - 1, self.pos[1])

        if check == None:

            return 1 # Return 1 if the space is empty, this will tell the neuron that this is a valid path
        
        else: return 0

    def checkRight(self):

        check = game.board.check(self.pos[0] + 1, self.pos[1])

        if check == None:

            return 1 # Return 1 if the space is empty, this will tell the neuron that this is a valid path
        
        else: return 0

    def moveUp(self):

        try:

            game.board.move(self.pos, (self.pos[0], self.pos[1]+1))

            self.pos = (self.pos[0], self.pos[1]+1)

        except:pass

            #print(f'Agent {self} tried to move out of bounds! Press enter to continue: ')
            #input()

    def moveDown(self):

        try:

            game.board.move(self.pos, (self.pos[0], self.pos[1]-1))

            self.pos = (self.pos[0], self.pos[1]-1)

        except:pass

            #print(f'Agent {self} tried to move out of bounds! Press enter to continue: ')
            #input()


    def moveLeft(self):

        try:

            game.board.move(self.pos, (self.pos[0]-1, self.pos[1]))

            self.pos = (self.pos[0]-1, self.pos[1])

        except:pass

            #print(f'Agent {self} tried to move out of bounds! Press enter to continue: ')
            #input()


    def moveRight(self):

        try:

            game.board.move(self.pos, (self.pos[0]+1, self.pos[1]))

            self.pos = (self.pos[0]+1, self.pos[1])

        except: pass

            #print(f'Agent {self} tried to move out of bounds! Press enter to continue: ')
            #input()

class Board:

    def __init__(self) -> None:
        
        self.grid = [[None for _ in range(255)] for _ in range(255)] # This makes a matrix of 255x255 filled with None-thing 
        # board[n][n] = i this is board[xcoord][ycoord] = what's in that spot

        self.agentList = []

    def register(self, agent) -> tuple:

        #index = len(self.agentList) Maybe use this to make a list of agents whose indexes are in board spots

        #self.agentList.append(agent)

        spaceOpen = False

        while(spaceOpen == False):

            x = randint(0,254)

            y = randint(0,254)

            space = self.check(x,y)

            if space == None:

                spaceOpen = True
        
        self.grid[x][y] = agent

        return (x,y)

    def check(self, x, y):

        try:

            return self.grid[x][y]

        except:

            #print(f'An agent checked and found the edge of the world! Please press enter to continue!')
            #input()
            return 0


    def move(self, pos, to):

        self.grid[to[0]][to[1]] = self.grid[pos[0]][pos[1]]

        self.grid[pos[0]][pos[1]] = None

    def display(self):
        print(self.grid)

class Game:

    def __init__(self) -> None:

        self.board = Board()

        self.agentList = []

        for i in range(255): # This is where I instantiate every agent

            self.agent1 = Agent(self)

            self.agentList.append(self.agent1)

        """for i in self.agentList:

            print(self.board.grid[i.pos[0]][i.pos[1]].neuralNet.genes.inputPaths)

        #{board.grid[agent1.pos[0]][agent1.pos[1]].neuralNet.genes.inputPaths}"""

    def tick(self):

        for i in self.agentList:
            
            i.act()

tick = 0

game = Game()

print(game.agent1.pos)

while tick < 255:
    print(tick)
    game.tick()
    tick += 1

print(game.agent1.pos)

#for agent in game.agentList:
#    print(f'Agent')

print(f'We done!')