import csv
import sys
import random

guestList = []
guests = []
population = []

def readSettings(fileName):
    with open(fileName, 'r') as infile:
      data = infile.read()
    list = data.splitlines()
    global TABLE_SIZE
    TABLE_SIZE = list[0]
    TABLE_SIZE.strip('\n')
    print("Table Size:\t" + TABLE_SIZE)
    global NUMBER_OF_GUESTS
    NUMBER_OF_GUESTS = list[1]
    print("Guest Count:\t" + NUMBER_OF_GUESTS)
    return;

def readGuests(fileName):
    with open(fileName, 'rt') as infile:
        data = csv.reader(infile)
        for row in data:
            guestList.append(row[0])
            guests.append(row)
        guests.remove(guests[0])
        guestList.remove(guestList[0])
        for row in guests:
            row.remove(row[0])
            print(row)
    return;
        

def initialize(settings, guests):
    readSettings(settings)
    readGuests(guests)
    return;

def populate():
    global POPULATION_SIZE
    POPULATION_SIZE = 3000

    seetings = []
    percentDone = 0
    for seetingArrangement in range(0, POPULATION_SIZE - 1):
        if (seetingArrangement % (POPULATION_SIZE / 10) == 0):
            percentDone += 10
            print(str(percentDone) + "% population generation complete")
        line = []
        for num in range(0, int(NUMBER_OF_GUESTS)):
            line.append(num)
        random.shuffle(line)
        seetings.append(line)
    return seetings;
    
def fitness(parent):
    score = random.randint(0, 100)
    return score;

def tournament(parents, children):
    parents = []
    random.seed(version = 2)
    for i in range (0, 4):
        parents.append(population[random.randint(0, POPULATION_SIZE - 1)])
        print(parents[i])
    winners = []
    first = -1
    indexFirst = -1
    second = -1
    indexSecond = -1
    index = -1
    for row in parents:
        index += 1
        rowFit = fitness(row)
        print(rowFit)
        if rowFit > second:
            if rowFit > first:
                first = rowFit
                indexFirst = index
            else:
                second = rowFit
                indexSecond = index
    winners.append(parents[indexFirst])
    winners.append(parents[indexSecond])
    return winners;

def recombine(parents):
    children = []
    for i in range (0, 1):
        child = []
        for k in range (0, int(NUMBER_OF_GUESTS)):
            child.append(-1)
        length = random.randint(1, int(NUMBER_OF_GUESTS) - 1)
        #print("Length:\t" + str(length))
        startIndex = random.randint(0, int(NUMBER_OF_GUESTS) - length)
       # print("Index: \t" + str(startIndex))
        for k in range (startIndex, startIndex + length):
            child[k] = parents[i][k]
        #print(child)
        childIndex = (startIndex + length) % int(NUMBER_OF_GUESTS)
        for k in range (0, int(NUMBER_OF_GUESTS)):
            offset = 0
            outerCircle = (startIndex + k + length) % int(NUMBER_OF_GUESTS)
            #print("Outer:\t" + str(outerCircle))
            innerCircle = (i + 1) % 2
            selectedGene = parents[innerCircle][outerCircle]
            #print("Selected gene:\t" + str(selectedGene))
            alreadyThere = 0
            for j in range(0, int(NUMBER_OF_GUESTS) -1):
                if selectedGene == child[j]:
                    alreadyThere = 1
            if alreadyThere == 1:
                #print("Skip")
                continue
            child[childIndex] = selectedGene
            #print("Gene added to child[" + str(childIndex) + "]")
            childIndex = (childIndex + 1) % int(NUMBER_OF_GUESTS)
        print(child)
        children.append(child[i])
    
    return children;

# Initialize parameters and guest list
initialize("settings.txt", "guests.csv")


# Creating initial population
population = populate()

# Generation Loop:
NUMBER_OF_GENERATIONS = 100
TOURNAMENT_COUNT = 5
for generation in range(0, NUMBER_OF_GENERATIONS - 1):

    # Parent Selection - Tournament w/ replacement - 5 parents, select 2
    winners = tournament(5, 2)
    print(winners)

    # Recombination - Permutation - Order 1 cross-over.
    # TODO: PMX - 2 children
    children = recombine(winners)

    # Mutation - Swap Mutation - 10% Pm
    #TODO:


    # Child Selection - Complete replacement 1:1
    #TODO:

    print("Enter any key to continue to next generation")
    wait = input();

# Continue



