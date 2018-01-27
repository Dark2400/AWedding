import csv
import sys
import random
import math
import seetingArrangement
import copy
import time

class EPop(object):
    def readSettings(self, fileName):
        with open(fileName, 'r') as infile:
          data = infile.read()
        list = data.splitlines()
        self.TABLE_SIZE = list[0]
        seetingArrangement.TABLE_SIZE = list[0]
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
        return;
        

    def initialize(self, settings, guests):
        self.readSettings(settings)
        self.readGuests(guests)
        return;

    def populate(self):
        seetings = []
        print("Population Progress: ", end = "")
        for num in range(1, int(self.SEATS) + 1):
            if num <= int(self.NUMBER_OF_GUESTS):
                self.defaultLine.append(num)
            else:
                self.defaultLine.append(-1)
        for i in range(self.POPULATION_SIZE):
            if (i % math.ceil(self.POPULATION_SIZE / 10) == 0):
                print("||", end = "", flush = True)
            plan = seetingArrangement.seetingArrangement(self.defaultLine)
            # randomize seeting plan
            plan.shuffle()
            seetings.append(plan)
        print("||")
        return seetings;
    
    def __init__(self, size = 0, guests = 0, tables = 0, seats = 0, pop = 0, children = 0, generations = 0, tourn = 0, prob = 0, fitnessTarget = 10, settings = "", guestsPref = ""):
        self.TABLE_SIZE = size
        self.NUMBER_OF_GUESTS = guests
        self.NUMBER_OF_TABLES = tables
        self.SEATS = seats
        self.GROWTH_RATE = 6
        self.POPULATION_SIZE = pop
        self.CHILD_POPULATION = pop * self.GROWTH_RATE
        self.CHILDREN_COUNT = children
        self.NUMBER_OF_GENERATIONS = generations
        self.TOURNAMENT_COUNT = tourn
        self.PROBABILITY_MUTATE = prob
        self.FITNESS_GOAL = fitnessTarget
        self.guestList = []
        self.guests = []
        self.population = []
        self.childPopulation = []
        self.SETTINGS_FILE = settings
        self.GUESTS_FILE = guestsPref
        self.outputActive = False
        self.defaultLine = []
        print("\t\t\tCOEN 432 - Part A")
        print("\t\t\tPlease note, -1 is an empty seat")
        print("Population Size:\t\t" + str(self.POPULATION_SIZE))
        print("Child Population Size:\t\t" + str(self.CHILD_POPULATION))
        print("Number of generations:\t\t" + str(self.NUMBER_OF_GENERATIONS))
        print("Tournament selection size:\t" + str(self.TOURNAMENT_COUNT))
        print("Children from tournament:\t" + str(self.CHILDREN_COUNT))
        print("Probablity of Mutation:\t\t" + str(self.PROBABILITY_MUTATE))
        print("Fitness goal:\t\t\t" + str(self.FITNESS_GOAL))
        # Initialize parameters and guest list
        self.initialize(self.SETTINGS_FILE, self.GUESTS_FILE)
        # Creating initial population
        self.population = self.populate()
        self.childPopulation = self.populate()
        return;

        
    def realFitness(self, plan):
        personAIndex = -2
        personBIndex = -2
        rating = 0
        penalty = 0
        posOrNeg = 0
        sameTable = False
        # For each guest
        for i in range (1, int(self.NUMBER_OF_GUESTS) + 1):
            # Find their index
            personAIndex = plan.plan.index(i)
            # For each other guests
            for k in range (1, int(self.NUMBER_OF_GUESTS) + 1):
                sameTable = False
                # Find ta index
                personBIndex = plan.plan.index(k)   
                # Check if same person
                if plan[personAIndex] == plan[personBIndex]: 
                    continue;
                # Check rating between personAIndex and personBIndex
                rating = self.guests[i-1][k-1]
                if rating == "3": # Skip neutral
                    continue
                # Check if same table
                tableA = int(personAIndex / int(self.TABLE_SIZE))
                tableB = int(personBIndex / int(self.TABLE_SIZE))
                if tableA == tableB:
                    sameTable = True
                currentTable = tableA
                # seats are ONLY checked if they are on the same table
                if sameTable:
                    seatR = (personAIndex + 1) % int(self.TABLE_SIZE)
                    seatL = (personAIndex - 1) % int(self.TABLE_SIZE)
                    if seatL < 0:
                        seatL += int(self.TABLE_SIZE)
                tableOffset = int(tableA) * int(self.TABLE_SIZE)
                # Due to check above, assume MUST BE ON SAME TABLE
                if rating == "1": # Not near
                    if sameTable:
                        # if person is NEXT TO
                        if personBIndex == seatR + tableOffset or personBIndex == seatL + tableOffset:
                            penalty += 15
                        else:
                            penalty += 10
                elif rating == "2": # Not next-to
                    if sameTable:
                        if personBIndex == seatR + tableOffset or personBIndex == seatL + tableOffset:
                            penalty += 15
                elif rating == "4": # Sits Next-to
                    if not sameTable: # Not on same table
                        # if personBIndex is not same table as personAIndex
                        penalty += 10     
                elif rating == "5": # Sits near to
                    if not sameTable: 
                        penalty += 20
                    else: # Sitting on same table
                        if personBIndex != seatR + tableOffset and personBIndex != seatL + tableOffset:
                            penalty += 15 # Same table, but not next to
        return penalty;


    def two_child_tournament(self):
        parents = []
        random.seed(version = 2)
        for i in range (self.TOURNAMENT_COUNT):
            parents.append(self.population[random.randint(0, self.POPULATION_SIZE - 2)])
            if self.outputActive: 
                print(parents[i])
        winners = []
        # Default is high since we are selecting for lowest
        first = 9999999
        indexFirst = -1
        second = 9999999
        indexSecond = -1
        index = -1
        for row in parents:
            index += 1
            rowFit = self.realFitness(row)
            if rowFit <= second:
                if rowFit < first:
                    first = rowFit
                    indexFirst = index
                else:
                    second = rowFit
                    indexSecond = index
        winners.append(parents[indexSecond])
        winners.append(parents[indexFirst])

        return winners;

    # Not used, was benchmark
    def orderOne(self, parents):
        children = []
        for i in range(self.CHILDREN_COUNT):
            children.append(seetingArrangement.seetingArrangement(self.defaultLine))
            for k in range (self.SEATS):
                children[i].plan.append(-2)
        length = random.randint(1, self.SEATS - 1)
        startIndex = random.randint(0, self.SEATS - length)
        i = -1
        for child in children:
            i += 1
            for k in range (startIndex, startIndex + length):
                child.plan[k % self.SEATS] = parents[i][k % self.SEATS]
            childIndex = (startIndex + length) % self.SEATS
            emptySeats = 0
            for guest in child.plan:
                if guest == -1:
                    emptySeats += 1
            for k in range (self.SEATS):
                outerCircle = (startIndex + k + length) % self.SEATS
                innerCircle = (i + 1) % 2
                selectedGene = parents[innerCircle][outerCircle]
                alreadyThere = 0
                if selectedGene in child.plan:
                    if selectedGene != -1:
                        continue;
                    else:           
                        if emptySeats < int(self.SEATS) - int(self.NUMBER_OF_GUESTS):
                            emptySeats += 1
                        else:
                            continue;
                child.plan[childIndex] = selectedGene
                childIndex = (childIndex + 1) % self.SEATS

        return children;

    # Preferred method of Recombination for this situation
    def PMX(self, parents):
        # in the odd occurence that the same parent is selected (Parent selection is a Random Tournament)
        # PMX produces identical children with identical parents. Therefore, we skip
        if parents[0] == parents[1]:
            return parents;
        children = []
        # Initialize children array
        for i in range(self.CHILDREN_COUNT):
            children.append(seetingArrangement.seetingArrangement())
            # Initilize seats as -2 to indicate not used. -1 indicates an empty seat
            for k in range (self.SEATS):
                children[i].plan.append(-2)
        # Select random subset
        length = random.randint(1, self.SEATS - 1)
        startIndex = random.randint(0, self.SEATS - length)
        i = -1 # Allows for alternating parents to run each PMX twice
        for child in children:
            i += 1
            emptySeats = 0
            # Copy over subset
            for k in range (startIndex, startIndex + length):
                child.plan[k % self.SEATS] = parents[i][k % self.SEATS]
            # Starting from crossover, look for elements not yet copied
            for k in range (startIndex, startIndex + length):
                emptySeats = child.plan.count(-1) # Count empty seats
                # Find value at current index
                value = parents[(i + 1) % 2].plan[k % self.SEATS]
                valueIndex = k
                # Check if in copied subset
                count = emptySeats 
                # This stage repeats (could have been recursive) to find the final free location
                while (True): 
                    if value in child.plan:
                        if value == -1: # Accomodate maximum number of empty seats
                            if count < int(self.SEATS) - int(self.NUMBER_OF_GUESTS):
                                count += 1
                                break
                        break;
                    # Find opposite parent's value
                    altValue = parents[i].plan[valueIndex]
                    count = 0
                    if altValue == -1:
                        for num in range(self.SEATS -1):
                            if parents[(i + 1) % 2].plan[num] == -1: # Deals with empty seats
                                if emptySeats >= int(self.SEATS) - int(self.NUMBER_OF_GUESTS):
                                    count += 1
                                    continue
                                if count == emptySeats:
                                    valueIndex = num
                                    break
                                elif count < emptySeats:
                                    if child.plan[num] == -2:
                                        valueIndex = num
                                        break
                                    else:
                                        count += 1        
                    else:
                        valueIndex = parents[(i + 1) % 2].plan.index(altValue)
                    if valueIndex >= startIndex and valueIndex <= startIndex + length - 1:
                        value = altValue
                        continue
                    child.plan[valueIndex % self.SEATS] = value
                    break

            # Copy over the reamiaing values
            # Only write into empty spaces (-2) in children
            # Skip child index if not empty, skip parent index if value already in child
            childIndex = startIndex + length
            k = startIndex + length - 1
            while k < int(startIndex) + int(length) + 1 + int(self.SEATS):
                k += 1
                emptySeats = child.plan.count(-1)
                targetValue = parents[(i + 1) % 2].plan[k % self.SEATS]
                if child.plan[childIndex % self.SEATS] == -2:
                    if targetValue in child.plan:
                        if targetValue == -1:
                           if emptySeats < int(self.SEATS) - int(self.NUMBER_OF_GUESTS):
                               emptySeats += 1
                           else:
                                continue
                        else:
                            continue
                    child.plan[childIndex % self.SEATS] = targetValue
                    childIndex = (childIndex + 1) % self.SEATS
                else:
                    if -2 in child.plan:
                        k -= 1
                        childIndex = (childIndex + 1) % self.SEATS
                    else:
                        break
        return children;

    # Inversion Mutaion
    def mutate(self, children):
        for child in children:
            line = []
            if random.randint(0, 100) >= (100 - self.PROBABILITY_MUTATE):
                if self.outputActive:
                    ("Mutation occured.")
                spareChild = []
                a = random.randint(0, int(self.NUMBER_OF_GUESTS) - 1)
                b = random.randint(0, int(self.NUMBER_OF_GUESTS) - 1)
                if a < b:
                    c = a
                    a = b
                    b = c
                line = child.plan[b:a];
                child.plan[b:a] = line[::-1]
        return children;


    def selectLowestFitness(self, pop):
        lowest = 99999
        index = 0
        count = 0
        current = 9999999
        for plan in pop:
            current = self.realFitness(plan)
            if current < lowest:
                lowest = current
                index = count
            count += 1
        return pop[index];

    def fitnessGoalReached(self, population):
        plan = self.selectLowestFitness(population)
        if self.realFitness(plan) <= self.FITNESS_GOAL:
            return True;
        else:
            return False;
    
    def getKey(self, plan):
        return plan[0];

    def selectSurvivor(self):
        fullPop = self.population.copy()
        myList = []
        for pop in self.childPopulation:
            fullPop.append(pop)
        # Create a list of [fitness, index] to sort
        for i in range(len(fullPop)):
            myList.append([self.realFitness(fullPop[i]), i])
        # getKey defined to return the first element of the tuple
        # sors in ascending order, lowest at [0] and highest at [n]
        myList = sorted(myList, key = self.getKey)
        # take lowest POPULATION_SIZE
        myList = myList[0 : self.POPULATION_SIZE]
        returnPop = []
        # Take the corresponding seetingArrangement objects from the combined population
        for i in range(len(myList)):
            returnPop.append(fullPop[myList[i][1]])
        return returnPop

    def output(self, text, pop):
        if self.outputActive: 
            print(text)
            for child in pop:
                print(child)
        return;

    def generations(self):
        # Generation Loop: Number limits the generations, or a previously set upper/lower bound
        for i in range(self.NUMBER_OF_GENERATIONS):
            print("Generation " + str(i + 1) + ":\t     ", end = "")
            self.childPopulation = []
            # Apply a u+lambda selection by creating 6 x population size
            uB = int(self.POPULATION_SIZE) * int(self.GROWTH_RATE)

            for k in range(math.ceil(int(uB) / 2)):
                if (k % math.ceil(int(uB) / 20) == 0):
                    print("||", end = "", flush = True)    
                if self.outputActive:
                        print("Tournament selection, " + str(self.TOURNAMENT_COUNT) + " parents, " + str(self.CHILDREN_COUNT) + " offspring")
                
                # Parent Selection - Tournament w/ replacement - 5 parents, select 2
                winners = self.two_child_tournament()             
                self.output("Winners / Offspring:", winners)

                ## Recombination - Permutation - PMX - 2 children
                self.output("Recombination: - PMX\nParents:", winners)
    
                children = self.PMX(winners)
                self.output("Recombination:\nChildren", children)

                # Mutation - Inversion Mutation - 10% Pm
                children = self.mutate(children)
                self.output("Mutation stage: - Inversion, Pm = 0.10", children)
                
                # Collect population size * growth rate
                for child in children:
                    self.childPopulation.append(child)
                # Continue
            # Extra output for loading bar
            print("||")

            # Output to demonstrate
            self.output("Parent pop:", self.population)
            print("Parent Pop Size:\t" + str(len(self.population)) + "\tLowest Fitness:\t" + str(self.realFitness(self.selectLowestFitness(self.population))))

            self.output("Child Pop:", self.childPopulation)
            print("Child Pop Size:\t\t" + str(len(self.childPopulation)) + "\tLowest Fitness:\t" + str(self.realFitness(self.selectLowestFitness(self.childPopulation))))

            # (u + lamba) selection - top POPULATION_SIZE of childPopulation and population are used as new population
            self.population = self.selectSurvivor().copy()
            self.output("New Parent Pop:", self.population)
            print("New Parent Pop Size:\t" + str(len(self.population)) + "\tLowest Fitness:\t" + str(self.realFitness(self.selectLowestFitness(self.population))))
            
            # Test for end condition
            best = self.selectLowestFitness(self.population)
            print("Fitness Goal:\tfitness < " + str(self.FITNESS_GOAL) + "\tBest:\t" + str(self.realFitness(best)))
            print(best)
            if self.fitnessGoalReached(self.population):
                return best;
            
            # Give delay for legibility
            time.sleep(2)


        best = self.selectLowestFitness(self.population)
        print("\n" + str(self.NUMBER_OF_GENERATIONS) + " generations have elapsed.")
        print("Best:\t" + str(best.fitness) + ":\t")
        print(best)
        return best;


    def testFitness(self, plan):
        return self.realFitness(plan)

