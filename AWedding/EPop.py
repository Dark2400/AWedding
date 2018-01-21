import csv
import sys
import random
import math
import seetingArrangement

class EPop(object):
    def readSettings(self, fileName):
        with open(fileName, 'r') as infile:
          data = infile.read()
        list = data.splitlines()
        self.TABLE_SIZE = list[0]
        self.TABLE_SIZE.strip('\n')
        print("Table Size:\t\t\t" + self.TABLE_SIZE)
        self.NUMBER_OF_GUESTS = list[1]
        print("Guest Count:\t\t\t" + str(self.NUMBER_OF_GUESTS))
        self.NUMBER_OF_TABLES = math.ceil(int(self.NUMBER_OF_GUESTS) / int(self.TABLE_SIZE))
        print("Tables:\t\t\t\t" + str(self.NUMBER_OF_TABLES))
        self.SEATS = int(self.TABLE_SIZE) * int(self.NUMBER_OF_TABLES);
        print("Seats:\t\t\t\t" + str(self.SEATS))
        return;

    def readGuests(self, fileName):
        with open(fileName, 'rt') as infile:
            data = csv.reader(infile)
            for row in data:
                self.guestList.append(row[0])
                self.guests.append(row)
            self.guests.remove(self.guests[0])
            self.guestList.remove(self.guestList[0])
            for row in self.guests:
                row.remove(row[0])

            #print(self.guests)
        return;
        

    def initialize(self, settings, guests):
        self.readSettings(settings)
        self.readGuests(guests)
        return;

    def populate(self):
        seetings = []
        print("Population Progress: ", end = "")
        for i in range(self.POPULATION_SIZE - 1):
            if (i % math.ceil(self.POPULATION_SIZE / 10) == 0):
                print("||", end = "", flush = True)
            plan = seetingArrangement.seetingArrangement(self.SEATS, self.NUMBER_OF_GUESTS, self.TABLE_SIZE)
            plan.shuffle()
            seetings.append(plan)
        print("||")
        return seetings;
    
    def __init__(self, size = 0, guests = 0, tables = 0, seats = 0, pop = 0, children = 0, generations = 0, tourn = 0, prob = 0, fitnessTarget = 10, settings = "", guestsPref = ""):
        self.TABLE_SIZE = size
        self.NUMBER_OF_GUESTS = guests
        self.NUMBER_OF_TABLES = tables
        self.SEATS = seats
        self.POPULATION_SIZE = pop
        self.CHILDREN_COUNT = children
        self.NUMBER_OF_GENERATIONS = generations
        self.TOURNAMENT_COUNT = tourn
        self.PROBABILITY_MUTATE = prob
        self.FITNESS_GOAL = fitnessTarget
        self.guestList = []
        self.guests = []
        self.population = []
        self.SETTINGS_FILE = settings
        self.GUESTS_FILE = guestsPref
        print("Population Size:\t\t" + str(self.POPULATION_SIZE))
        print("Number of generations:\t\t" + str(self.NUMBER_OF_GENERATIONS))
        print("Tournament selection size:\t" + str(self.TOURNAMENT_COUNT))
        print("Children from tournament:\t" + str(self.CHILDREN_COUNT))
        print("Probablity of Mutation:\t\t" + str(self.PROBABILITY_MUTATE))
        print("Fitness goal:\t\t\t" + str(self.FITNESS_GOAL))

        # Initialize parameters and guest list
        self.initialize(self.SETTINGS_FILE, self.GUESTS_FILE)
        # Creating initial population
        self.population = self.populate()
        return;

    def fitness(self, plan):
        if plan.fitness == -1:
            plan.fitness = ( random.randint(0,99) * 100 + random.randint(0,100) ) / 100
        return plan.fitness;

        
    def realFitness(self, plan):
        personA = -2
        personB = -2
        rating = 0
        penalty = 0
        posOrNeg = 0
        sameTable = False
        for i in range (int(self.NUMBER_OF_GUESTS) - 1):
            personA = i
            for k in range (int(self.NUMBER_OF_GUESTS) - 1):
                sameTable = False
                personB = k   
                # Check if same person
                if personA == personB: 
                    #print("Skip - Same Person")
                    continue;
                # Check rating between personA and personB
                rating = self.guests[personA][personB]
                tableA = int(i / int(self.TABLE_SIZE))
                tableB = int(k / int(self.TABLE_SIZE))
                if tableA == tableB:
                    sameTable = True
                seatR = (i + 1) % int(self.TABLE_SIZE)
                if i == 0:
                    seatL = 5
                seatL = (i - 1) % int(self.TABLE_SIZE)
                # Due to check above, assume MUST BE ON SAME TABLE
                if rating == "1": # Not near
                    if sameTable:
                        # if person is NEXT TO
                        if personB == plan[seatR] or personB == plan[seatL]:
                            penalty += 15
                        else:
                            penalty += 10
                elif rating == "2": # Not next-to
                    if sameTable:
                        if personB == plan[seatR] or personB == plan[seatL]:
                            penalty += 15
                elif rating == "4": # Sits Next-to
                    if not sameTable: # Not on same table
                        # if personB is not same table as personA
                        penalty += 10     
                elif rating == "5": # Sits near to
                    if not sameTable: 
                        penalty += 20
                    else: # Sitting on same table
                        if personB != plan[seatR] and personB != plan[seatL]:
                            penalty += 15 # Same table, but not next to
                #else:
                    #print("Rating 3 or empty:\t" + str(rating))
                #elif rating == 3: # Neutral
        plan.fitness = penalty
        return penalty;


    def two_child_tournament(self):
        parents = []
        random.seed(version = 2)
        for i in range (self.TOURNAMENT_COUNT):
            parents.append(self.population[random.randint(0, self.POPULATION_SIZE - 2)])
            #print(parents[i])
        winners = []
        first = 9999999
        indexFirst = -1
        second = 9999999
        indexSecond = -1
        index = -1
        for row in parents:
            index += 1
            rowFit = self.realFitness(row)
            #print(rowFit)
            if rowFit <= second:
                if rowFit < first:
                    first = rowFit
                    indexFirst = index
                else:
                    second = rowFit
                    indexSecond = index
        #print("First:\t" + str(first))
        #print("Second:\t" + str(second))
        winners.append(parents[indexFirst])
        winners.append(parents[indexSecond])

        return winners;

    def recombine(self, parents):
        #print("Parents:")
        #print(parents)
        children = []
        length = random.randint(1, self.SEATS - 1)
        #print("Length:\t" + str(length))
        startIndex = random.randint(0, self.SEATS - length)
        #print("Index: \t" + str(startIndex))
        for i in range (self.CHILDREN_COUNT):
            child = []
            for k in range (self.SEATS):
                child.append(-2)
            for k in range (startIndex, startIndex + length):
                child[k % self.SEATS] = parents[i][k % self.SEATS]
            #print("Length and swap index done")
            #print(child)
            childIndex = (startIndex + length) % self.SEATS
            emptySeats = 0
            for k in range (self.SEATS):
                outerCircle = (startIndex + k + length) % self.SEATS
                #print("Outer:\t" + str(outerCircle))
                innerCircle = (i + 1) % 2
                selectedGene = parents[innerCircle][outerCircle]
                #print("Selected gene:\t" + str(selectedGene))
                alreadyThere = 0
                if selectedGene in child:
                    if selectedGene != -1:
                        #print("Skip")
                        continue;
                    else:
                        if emptySeats < int(self.SEATS) - int(self.NUMBER_OF_GUESTS):
                            emptySeats = emptySeats + 1
                        else:
                            #print("Skip")
                            continue;
                child[childIndex] = selectedGene
                #print("Gene added to child[" + str(childIndex) + "]")
                #print(child)
                childIndex = (childIndex + 1) % self.SEATS
        
            children.append(child)
        #print("Children:")
        #print(children)
        return children;

    def testRecombine(self):
        self.population = populate()
        winners = two_child_tournament()
        children = recombine(winners)
        if child in children == parent in winners:
            print("Child: ")
            print(child)
            print("Parent:")
            print(parent)
            print("Recombine Failed")


    def mutate(self, children):
        for child in children:
            line = []
            if random.randint(0, 100) >= (100 - self.PROBABILITY_MUTATE):
                spareChild = []
                a = random.randint(0, int(self.NUMBER_OF_GUESTS) - 1)
                b = random.randint(0, int(self.NUMBER_OF_GUESTS) - 1)
                if a < b:
                    c = a
                    a = b
                    b = c
                line = child[b:a];
                child[b:a] = line[::-1]
        return children;


    def childSelection(self, children):
        childPopulation = []
        for child in children:
            childPopulation.append(child)
        return childPopulation;

    def selectLowestFitness(self):
        lowest = 99999
        index = 0
        count = 0
        for plan in self.population:
            if plan.fitness < lowest:
                lowest = plan.fitness
                index = count
            count += 1
        return self.population[index];

    def fitnessGoalReached(self):
        plan = self.selectLowestFitness()
        if plan.fitness <= self.FITNESS_GOAL:
            return True;
        else:
            return False;

    def generations(self):
        # Generation Loop:
        print("Generation Progress: ", end = "")
        for i in range(self.NUMBER_OF_GENERATIONS):
            if (i % math.ceil(self.NUMBER_OF_GENERATIONS / 10) == 0):
                print("||", end = "", flush = True)
            childPopulation = []
            for k in range(math.ceil(int(self.POPULATION_SIZE) / 2)):

                # Parent Selection - Tournament w/ replacement - 5 parents, select 2
                winners = self.two_child_tournament()
                #print("Winners:")
                #for plan in winners:
                #    print(plan)
    
    
                # Recombination - Permutation - Order 1 cross-over.
                # TODO: PMX - 2 children
                children = self.recombine(winners)
                #print(children)
    
                # Mutation - Inversion Mutation - 10% Pm
                children = self.mutate(children)
                #print(children)
    
                # Child Selection - Complete replacement 1:1
                # New population = same size old population
                for child in self.childSelection(children):
                    childPopulation.append(child)


                # Continue

            population = childPopulation

            # Test for end condition
            if self.fitnessGoalReached():
                best = self.selectLowestFitness()
                print("\nFitness Goal:\t" + str(self.FITNESS_GOAL) + "\tBest:\t", end = "")
                print(best)
                return best;
            #print("Enter any key to continue to next generation")
            #wait = input();
        print("||")

        #print("Parent Pop:")
        #print(population)
        #print("Child Pop:")
        #print(childPopulation)

        best = self.selectLowestFitness()
        print("\n" + str(self.NUMBER_OF_GENERATIONS) + " generations have elapsed.")
        print("Best:\t" + str(best.fitness) + ":\t")
        print(best)
        return best;



