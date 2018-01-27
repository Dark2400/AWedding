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
        for i in range(self.POPULATION_SIZE):
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
        self.childPopulation = []
        self.SETTINGS_FILE = settings
        self.GUESTS_FILE = guestsPref
        self.output = False
        self.output2 = False
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
        self.childPopulation = self.populate()
        return;

    def fitness(self, plan):
        if plan.fitness == -1:
            plan.fitness = ( random.randint(0,99) * 100 + random.randint(0,100) ) / 100
        return plan.fitness;

        
    def realFitness(self, plan):
        personAIndex = -2
        personBIndex = -2
        rating = 0
        penalty = 0
        posOrNeg = 0
        sameTable = False
        for i in range (1, int(self.NUMBER_OF_GUESTS)):
            personAIndex = plan.plan.index(i)
            for k in range (1, int(self.NUMBER_OF_GUESTS)):
                sameTable = False
                personBIndex = plan.plan.index(k)   
                # Check if same person
                if plan[personAIndex] == plan[personBIndex]: 
                    #print("Skip - Same Person")
                    continue;
                # Check rating between personAIndex and personBIndex
                rating = self.guests[i-1][k-1]
                if rating == "3":
                    continue
                tableA = int(personAIndex / int(self.TABLE_SIZE))
                tableB = int(personBIndex / int(self.TABLE_SIZE))
                if tableA == tableB:
                    sameTable = True
                currentTable = tableA
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
                #else:
                    #print("Rating 3 or empty:\t" + str(rating))
                #elif rating == 3: # Neutral
        plan.fitness = penalty
        return penalty;


    def two_child_tournament(self):
        parents = []
        random.seed(version = 2)
        #if self.output: 
            #print("\nParent Selection: - tournament, choose 2 offspring / 5 parents")
        for i in range (self.TOURNAMENT_COUNT):
            parents.append(self.population[random.randint(0, self.POPULATION_SIZE - 2)])
            if self.output: 
                print(parents[i])
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
    
        #print("Winners:")
        #print("First choice:\t" + str(first))
        #print(parents[indexFirst])
        #print("Second:\t\t" + str(second))
        #print(parents[indexSecond])
        if indexFirst == indexSecond:
            if self.output: print("Error, first and second are the same!")
        winners.append(parents[indexSecond])
        winners.append(parents[indexFirst])

        return winners;

    def orderOne(self, parents):
        children = []
        for i in range(self.CHILDREN_COUNT):
            children.append(seetingArrangement.seetingArrangement(self.SEATS, self.NUMBER_OF_GUESTS, self.TABLE_SIZE))
            children[i].plan = []
            for k in range (self.SEATS):
                children[i].plan.append(-2)
        length = random.randint(1, self.SEATS - 1)
        #print("Length:\t" + str(length))
        startIndex = random.randint(0, self.SEATS - length)
        #print("Index: \t" + str(startIndex))
        i = -1
        for child in children:
            i += 1
            for k in range (startIndex, startIndex + length):
                child.plan[k % self.SEATS] = parents[i][k % self.SEATS]
            #print("Length and swap index done")
            #print(child)
            childIndex = (startIndex + length) % self.SEATS
            emptySeats = 0
            for guest in child.plan:
                if guest == -1:
                    emptySeats += 1
                    #print("Current emptySeats:\t" + str(emptySeats))
            for k in range (self.SEATS):
                outerCircle = (startIndex + k + length) % self.SEATS
                #print("Outer:\t" + str(outerCircle))
                innerCircle = (i + 1) % 2
                selectedGene = parents[innerCircle][outerCircle]
                #print("Selected gene:\t" + str(selectedGene))
                alreadyThere = 0
                if selectedGene in child.plan:
                    if selectedGene != -1:
                        #print("Skip")
                        continue;
                    else:           
                        if emptySeats < int(self.SEATS) - int(self.NUMBER_OF_GUESTS):
                            #print("Current emptySeats:\t" + str(emptySeats))
                            emptySeats += 1
                        else:
                            #print("Skip")
                            continue;
                child.plan[childIndex] = selectedGene
                #print("Gene added to child[" + str(childIndex) + "]")
                #print(child)
                childIndex = (childIndex + 1) % self.SEATS
            #print(child)

        return children;

    def PMX(self, parents):
        if parents[0] == parents[1]:
            # print("Same genotype in parents, recombination does nothing")
            return parents;
        children = []
        for i in range(self.CHILDREN_COUNT):
            children.append(seetingArrangement.seetingArrangement(self.SEATS, self.NUMBER_OF_GUESTS, self.TABLE_SIZE))
            children[i].plan = []
            for k in range (self.SEATS):
                children[i].plan.append(-2)
        length = random.randint(1, self.SEATS - 1)
        # print("Length:\t" + str(length))
        startIndex = random.randint(0, self.SEATS - length)
        # print("Index: \t" + str(startIndex))
        i = -1
        for child in children:
            i += 1
            emptySeats = 0
            # Copy subset to child
            # print("StartIndex: " + str(startIndex))
            for k in range (startIndex, startIndex + length):
                child.plan[k % self.SEATS] = parents[i][k % self.SEATS]
                # print(child)
            # Starting from crossover, look for elements not yet copied
            for k in range (startIndex, startIndex + length):
                emptySeats = child.plan.count(-1)
                value = parents[(i + 1) % 2].plan[k % self.SEATS]
                valueIndex = k
                # print("Target:\t", end = "")
                # print(value)
                # Check if in copied subset
                count = emptySeats 
                while (True): 
                    # print("EmptySeats: " + str(emptySeats))
                    if value in child.plan:
                        # Allow for empty seats
                        if value == -1:
                            if count < int(self.SEATS) - int(self.NUMBER_OF_GUESTS):
                                # print("Count: " + str(count))
                                count += 1
                                break
                            else:
                                # print("Skip placing: " + str(value))
                                break
                        else:
                            # print("Skip placing: " + str(value))
                            break # If max empty seats reached, skip
                
                    valueIndex = parents[(i + 1) % 2].plan.index(value);
                    # Selecting value from index in other parent
                    altValue = parents[i].plan[valueIndex]
                    # print("AltValue: " + str(altValue))
                    # print("EmptySeats: " + str(emptySeats))
                    count = 0
                    if altValue == -1:
                        for num in range(self.SEATS -1):
                            if parents[(i + 1) % 2].plan[num] == -1:
                                if emptySeats >= int(self.SEATS) - int(self.NUMBER_OF_GUESTS):
                                    # print("No empty seats, skipping -1")
                                    count += 1
                                    continue
                                if count == emptySeats:
                                    # print("Picking -1 at index: " + str(num))
                                    valueIndex = num
                                    break
                                elif count < emptySeats:
                                    if child.plan[num] == -2:
                                        # print("-1 not used, using this one")
                                        valueIndex = num
                                        break
                                    else:
                                        # print("spot already used, going to next -1")
                                        count += 1
                                    
                    else:
                        valueIndex = parents[(i + 1) % 2].plan.index(altValue)
                    # print("newValueIndex: " + str(valueIndex))
                    if valueIndex >= startIndex and valueIndex <= startIndex + length - 1:
                        value = altValue
                        # print("index currently occupied in child, trying again with value: " + str(value))
                        continue
                    child.plan[valueIndex % self.SEATS] = value
                    # print(child)
                    break

            # Copy over the reamiaing values
            childIndex = startIndex + length
            k = startIndex + length - 1
            while k < int(startIndex) + int(length) + 1 + int(self.SEATS):
                k += 1
                emptySeats = child.plan.count(-1)
                targetValue = parents[(i + 1) % 2].plan[k % self.SEATS]
                # print("Parent Index: " + str(k % self.SEATS) + " Child Index: " + str(childIndex % self.SEATS) + " child's index value: " + str(child.plan[childIndex % self.SEATS]) + " targetValue: " + str(targetValue))
                if child.plan[childIndex % self.SEATS] == -2:
                    if targetValue in child.plan:
                        if targetValue == -1:
                           if emptySeats < int(self.SEATS) - int(self.NUMBER_OF_GUESTS):
                               emptySeats += 1
                           else:
                                # print("Skip " + str(targetValue))
                                continue
                        else:
                            # print("Skip " + str(targetValue))
                            continue
                    child.plan[childIndex % self.SEATS] = targetValue
                    # print("Copying: " + str(targetValue) + " to child index index: " + str(childIndex % self.SEATS))
                    # print(child)
                    childIndex += 1
                else:
                    if -2 in child.plan:
                        # print("k should be lowered here: " + str(k))
                        k -= 1
                        childIndex += 1
                    else:
                        # print("Recomb done")
                        break
            # print("parents")
            #for parent in parents:
                # print(parent)
            # print("Remaining elements copied, child:")
            # print(child)
        return children;


    def mutate(self, children):
        for child in children:
            line = []
            if random.randint(0, 100) >= (100 - self.PROBABILITY_MUTATE):
                if self.output:
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

    def generations(self):
        # Generation Loop:

        #print("Generation Progress: ", end = "")
        for i in range(self.NUMBER_OF_GENERATIONS):
            #if (i % math.ceil(self.NUMBER_OF_GENERATIONS / 10) == 0):
            #    print("||", end = "", flush = True)
            print("Generation " + str(i + 1) + ":")
            self.childPopulation = []
            for k in range(math.ceil(int(self.POPULATION_SIZE) / 2)):
                if self.output:
                    print("Tournament selection, " + str(self.TOURNAMENT_COUNT) + " parents, " + str(self.CHILDREN_COUNT) + " offspring")
                # Parent Selection - Tournament w/ replacement - 5 parents, select 2
                winners = self.two_child_tournament()
                if self.output: 
                    print("Winners / Offspring:")
                    for child in winners:
                        print(child)
                ## Recombination - Permutation - Order 1 cross-over.
                ## TODO: PMX - 2 children
                #if self.output: 
                #    print("Recombination: - Order 1 crossover. TODO: PMX")
                #children = self.orderOne(winners)
                #if self.output: 
                #    print("Children:")
                #    for child in children:
                #        print(child)

                ## Recombination - Permutation - PMX - 2 children
                if self.output:
                    print("Recombination: - PMX")
                    print("Parents:")
                    for child in winners:
                        print(child)
                    
                children = self.PMX(winners)
                if self.output:
                    print("Children:")
                    for child in children:
                        print(child)


                # Mutation - Inversion Mutation - 10% Pm
                if self.output: 
                    print("Mutation stage: - Inversion, Pm = 0.10")
                children = self.mutate(children)

                # Child Selection   - Complete replacement 1:1
                #                   - Generational Model
                # New population = same size old population
                if self.output: 
                    print("Survivor selection: Full replacement")
                for child in children:
                    if self.output: 
                        print(child)
                    self.childPopulation.append(child)
                # Continue

            if self.output2: 
                print("Parent pop:")
                for pop in self.population:
                    print(pop)
            print("Size:\t" + str(len(self.population)) + "\tLowest Fitness:\t" + str(self.realFitness(self.selectLowestFitness(self.population))))
            if self.output2: 
                print(lowest)
            self.population = self.childPopulation.copy()
            if self.output2: 
                print("Child Pop:")
                for pop in self.population:
                    print(pop)
            print("Size:\t" + str(len(self.population)) + "\tLowest Fitness:\t" + str(self.realFitness(self.selectLowestFitness(self.population))))


            # Test for end condition
            best = self.selectLowestFitness(self.population)
            print("Fitness Goal:\tf < " + str(self.FITNESS_GOAL) + "\tBest:\t" + str(self.realFitness(best)))
            print(best)
            if self.fitnessGoalReached(self.population):
                return best;
            time.sleep(2)

        #print("||")

        best = self.selectLowestFitness(self.population)
        print("\n" + str(self.NUMBER_OF_GENERATIONS) + " generations have elapsed.")
        print("Best:\t" + str(best.fitness) + ":\t")
        print(best)

        return best;


    def testFitness(self, plan):
        return self.realFitness(plan)

