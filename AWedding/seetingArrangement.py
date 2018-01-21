import random

class seetingArrangement(object):
 # Representation of evolving object. 
 #
 # Represented by a string of integers, with -1 indicating empty and -2 indicating errors.
 # Each integer counts as a p[otential guests, no fractional numbers allowed
 #
 # Table Size is given, index % tablesize will give the proper index
 # _________ ________ ________ __   _______
 # [0][1][2][3][4][5][6][7][8][9]...[14][15]
 #


    def shuffle(self):
        random.shuffle(self.plan)
        return;

    def __str__(self):
        count = 0;
        output = []
        for seat in self.plan:
            output.append("[" + str(seat) + "]")
        temp = "".join(output)
        return temp;

    def __getitem__(self, key):
        return self.plan[key];

    def __init__(self, seats, guests, size):
        self.fitness = 99999999
        self.plan = []
        self.SEATS = seats
        self.NUMBER_OF_GUESTS = guests
        self.TABLE_SIZE = size
        for num in range(1, int(self.SEATS) + 1):
            if num <= int(self.NUMBER_OF_GUESTS):
                self.plan.append(num)
            else:
                self.plan.append(-1)
        return;




