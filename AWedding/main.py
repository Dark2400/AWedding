# Driver class for Evolutionary Population Epop
# COEN 432
# Marc Bass - 26488994
# 01/27/2018
#
#


import EPop

obj1 = EPop.EPop(pop = 200, 
                 children = 2, 
                 generations = 20, 
                 tourn = 5, 
                 prob = 0.35, 
                 fitnessTarget = 10, 
                 settings = "settings.txt", 
                 guestsPref = "preferences.csv",
                 output = "output.csv")

obj1.testSuite()

#obj1.generations(True)

obj1.testDiversity(False, False)
     