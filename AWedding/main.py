# Driver class for Evolutionary Population Epop
# COEN 432
# Marc Bass - 26488994
# 01/27/2018
#
#


import EPop
#import seetingArrangement

obj1 = EPop.EPop(pop = 1000, 
                 children = 2, 
                 generations = 10, 
                 tourn = 5, 
                 prob = 0.2, 
                 fitnessTarget = 10, 
                 settings = "settings.txt", 
                 guestsPref = "preferences.csv",
                 output = "output.csv")

#obj1.outputCSV(seetingArrangement.seetingArrangement([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, -1, 12, 13, 14, -1, -1, 15]))
obj1.generations()


 
