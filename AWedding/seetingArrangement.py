import random

class seetingArrangement(object):
 # Representation of evolving object. 
 #
 # Represented by a string of integers, with -1 indicating empty and -2 indicating errors.
 # Each integer counts as a p[otential guests, no fractional numbers allowed
 #
 # Table Size is given, index % tablesize will give the proper index
 # _________ ________  ________   __   _______
 # [0][1][2] [3][4][5] [6][7][8] [9]...[14][15]
 #

    global TABLE_SIZE

    def shuffle(self):
        random.shuffle(self.plan)
        return;

    def __str__(self):
        count = 0;
        output = []
        for seat in self.plan:
            if count % int(TABLE_SIZE) == 0:
                output.append("\tT" + str(int(count / int(TABLE_SIZE))) + ": ")
            output.append("[" + str(seat) + "]")
            count += 1
        temp = "".join(output)
        return temp;

    def __getitem__(self, key):
        return self.plan[key];

    def __init__(self, newPlan = []):
        self.plan = newPlan.copy()
        return;

    def setFitness(self, fit):
        self.fitness = fit
        return;

    def getFitness(self):
        return self.fitness;




