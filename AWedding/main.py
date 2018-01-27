# Driver class for Evolutionary Population Epop
# COEN 432
# Marc Bass - 26488994
# 01/27/2018
#
#


import EPop
import seetingArrangement

obj1 = EPop.EPop(pop = 200, 
                 children = 2, 
                 generations = 10, 
                 tourn = 5, 
                 prob = 0.2, 
                 fitnessTarget = 10, 
                 settings = "settings.txt", 
                 guestsPref = "preferences.csv",
                 output = "output.csv")

#obj1.realFitness(seetingArrangement.seetingArrangement([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, -1, 12, 13, 14, -1, -1, 15]))
#obj1.outputCSV(seetingArrangement.seetingArrangement([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, -1, 12, 13, 14, -1, -1, 15]))
# Tests diversity function, same plan = 1 diversity
#print(obj1.diversity(seetingArrangement.seetingArrangement([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, -1, 12, 13, 14, -1, -1, 15]), seetingArrangement.seetingArrangement([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, -1, 12, 13, 14, -1, -1, 15])))
obj1.generations()


 
