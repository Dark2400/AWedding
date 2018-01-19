import csv
import sys
import random
import math

guestList = []
guests = []
population = []
childPopulation = []
SETTINGS_FILE = "settings.txt"
GUESTS_FILE = "preferences.csv"

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
    print("Guest Count:\t" + str(NUMBER_OF_GUESTS))
    global NUMBER_OF_TABLES
    NUMBER_OF_TABLES = math.ceil(int(NUMBER_OF_GUESTS) / int(TABLE_SIZE))
    print("Tables:\t" + str(NUMBER_OF_TABLES))
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
            #print(row)
    return;
        

def initialize(settings, guests):
    readSettings(settings)
    readGuests(guests)
    return;

def populate():
    global POPULATION_SIZE
    # Must be greater than number of guests, even numbers
    POPULATION_SIZE = 16
    seetings = []
    print("Progress: ", end = "")
    for seetingArrangement in range(POPULATION_SIZE - 1):
        if (seetingArrangement % math.ceil(POPULATION_SIZE / 10) == 0):
            print("||", end = "")
        line = []
        for num in range(1, int(TABLE_SIZE) * int(NUMBER_OF_TABLES) + 1):
            if num <= int(NUMBER_OF_GUESTS):
               line.append(num)
            else:
               line.append(-1)
        random.shuffle(line)
        seetings.append(line)
    print("||")
    return seetings;
    
def fitness(parent):
    score = random.randint(0, 100)
    return score;

def two_child_tournament(count):
    parents = []
    random.seed(version = 2)
    for i in range (count - 1):
        parents.append(population[random.randint(0, POPULATION_SIZE - 2)])
        #print(parents[i])
    winners = []
    first = -1
    indexFirst = -1
    second = -1
    indexSecond = -1
    index = -1
    for row in parents:
        index += 1
        rowFit = fitness(row)
        #print(rowFit)
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
    for i in range (2):
        child = []
        for k in range (int(TABLE_SIZE) * int(NUMBER_OF_TABLES)):
            child.append(-1)
        length = random.randint(1, int(NUMBER_OF_GUESTS) - 1)
        #print("Length:\t" + str(length))
        startIndex = random.randint(0, int(NUMBER_OF_GUESTS) - length)
       # print("Index: \t" + str(startIndex))
        for k in range (startIndex, startIndex + length):
            child[k] = parents[i][k]
        #print(child)
        childIndex = (startIndex + length) % int(NUMBER_OF_GUESTS)
        for k in range (int(NUMBER_OF_GUESTS)):
            outerCircle = (startIndex + k + length) % int(NUMBER_OF_GUESTS)
            #print("Outer:\t" + str(outerCircle))
            innerCircle = (i + 1) % 2
            selectedGene = parents[innerCircle][outerCircle]
            #print("Selected gene:\t" + str(selectedGene))
            alreadyThere = 0
            if selectedGene in child:
                continue;
            ######old code######
            #for j in range(int(NUMBER_OF_GUESTS) -1):
            #    if selectedGene == child[j]:
            #        alreadyThere = 1
            #if alreadyThere == 1:
            #    #print("Skip")
            #    continue

            child[childIndex] = selectedGene
            #print("Gene added to child[" + str(childIndex) + "]")
            childIndex = (childIndex + 1) % int(NUMBER_OF_GUESTS)
        #print(child)
        children.append(child)
    
    return children;

# Initialize parameters and guest list
initialize(SETTINGS_FILE, GUESTS_FILE)


# Creating initial population
population = populate()

# Generation Loop:
NUMBER_OF_GENERATIONS = 1
TOURNAMENT_COUNT = 5
PROBABILITY_MUTATE = 10
for i in range(NUMBER_OF_GENERATIONS):
    for k in range(math.ceil(int(POPULATION_SIZE) / 2)):
        # Parent Selection - Tournament w/ replacement - 5 parents, select 2
        winners = two_child_tournament(TOURNAMENT_COUNT)
        #print(winners)


        # Recombination - Permutation - Order 1 cross-over.
        # TODO: PMX - 2 children
        children = recombine(winners)
        #print(children)

        # Mutation - Swap Mutation - 10% Pm
        for child in children:
            if random.randint(0, 100) >= (100 - PROBABILITY_MUTATE):
                a = random.randint(0, int(NUMBER_OF_GUESTS) - 1)
                b = random.randint(0, int(NUMBER_OF_GUESTS) - 1)
                spareGene = child[a]
                child[a] = child[b]
                child[b] = spareGene
                #print("Mutated")
        #print(children)

        # Child Selection - Complete replacement 1:1
        # New population = same size old population
        for child in children:
            childPopulation.append(child)
        #print("Enter any key to continue to next generation")
        #wait = input();

        # Continue
    print("Parent Pop:")
    print(population)
    print("Child Pop:")
    print(childPopulation)



