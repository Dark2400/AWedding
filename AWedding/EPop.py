class EPop(object):
#
# This is an Evolving Population, EPop. Given an object, it can run recombination and mutation to achieve a final offspring that meets a given criteria or generation limit.
# Parent selection:   from tournament of y, defined in class members. Full replacement stratedgy, 1:1 for next generation
# Recombination: Order 1 crossover
#               TODO: PMX
# Mutation: Swap Gene: Pm = 0.10
#               TODO: Find more appropriate (adjacent) stratedgy
# Child Selection: x from tournament of y, defined in class members. Full replacement stratedgy, 1:1 for next generation
#
    import csv
    import sys
    import random
    import math
    import seetingArrangement
    import EPop
    guestListPref = []
    guestsPref = []
    population = []
    childPopulation = []
    POPULATION_SIZE = 3000
    NUMBER_OF_GENERATIONS = 1
    TOURNAMENT_COUNT = 5
    PROBABILITY_MUTATE = 0.1
    NUMBER_OF_GUESTS = 0
    TABLE_SIZE = 0
    NUMBER_OF_TABLES = 0

    SETTINGS_FILE = "settings.txt"
    GUESTS_FILE = "preferences.csv"

    def readSettings():
        with open(SETTINGS_FILE, 'r') as infile:
          data = infile.read()
        list = data.splitlines()
        TABLE_SIZE = list[0]
        TABLE_SIZE.strip('\n')
        print("Table Size:\t" + TABLE_SIZE)
        NUMBER_OF_GUESTS = list[1]
        print("Guest Count:\t" + str(NUMBER_OF_GUESTS))
        NUMBER_OF_TABLES = math.ceil(int(NUMBER_OF_GUESTS) / int(TABLE_SIZE))
        print("Tables:\t" + str(NUMBER_OF_TABLES))
        return;

    def readGuests():
        with open(GUESTS_FILE, 'rt') as infile:
            data = csv.reader(infile)
            for row in data:
                guestListPref.append(row[0])
                guestsPref.append(row)
            guestsPref.remove(guestsPref[0])
            guestListPref.remove(guestListPref[0])
            for row in guestsPref:
                row.remove(row[0])
                #print(row)
        return;
        

    def initialize(self):
        EPop.readSettings()
        EPop.readGuests()
        return;

    def __init__(self):
        guestListPref = []
        guestsPref = []
        population = []
        childPopulation = []
        POPULATION_SIZE = 3000
        NUMBER_OF_GENERATIONS = 1
        TOURNAMENT_COUNT = 5
        PROBABILITY_MUTATE = 0.1
        NUMBER_OF_GUESTS = 0
        TABLE_SIZE = 0
        NUMBER_OF_TABLES = 0

        SETTINGS_FILE = "settings.txt"
        GUESTS_FILE = "preferences.csv"
        EPop.initialize(self)
        print("Init done")

    def populate():
        # Must be greater than number of guests, even numbers
        seetings = []
        print("Progress: ", end = "")
        for i in range(POPULATION_SIZE - 1):
            if (i % math.ceil(POPULATION_SIZE / 10) == 0):
                print("||", end = "")
            plan = seetingArrangement()
            plan.seetInOrder()
            random.shuffle(line)
            seetings.append(line)
        print("||")
        return seetings;
    
    def fitness(parent):
        score = random.randint(0, 100)
        return score;

    ### TODO: just changed, need to test #####
    def tournament(count):
        parents = []
        random.seed(version = 2)
        for k in range(math.ceil((count - 1) / 2)):
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

    def Mutation(children):
        for child in children:
            if random.randfloat(0, 1) <= PROBABILITY_MUTATE:
                a = random.randint(0, int(NUMBER_OF_GUESTS) - 1)
                b = random.randint(0, int(NUMBER_OF_GUESTS) - 1)
                spareGene = child[a]
                child[a] = child[b]
                child[b] = spareGene
                print("Mutated")
            print(children)
    
    def run(self):
        ## CONSTRUCTOR
        # Initialize parameters and guest list
        EPop.initialize(SETTINGS_FILE, GUESTS_FILE)

        # Creating initial population
        population = EPop.populate()

        # Generation Loop:
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
                Mutation(children)

                # Child Selection - Complete replacement 1:1
                # New population = same size old population
                for child in children:
                    childPopulation.append(child)
                print("Enter any key to continue to next generation")
                wait = input();

                # Continue
            print("Parent Pop:")
            print(population)
            print("Child Pop:")
            print(childPopulation)
