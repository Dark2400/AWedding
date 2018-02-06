# Driver class for Evolutionary Population Epop
# COEN 432
# Marc Bass - 26488994
# 01/27/2018
#
#
# CHANGES SINCE SUBMISSON:
# 1. testSuite() is not calibrated for other sizes yet. It needs problem object oriented techniques and calibration to use static variables. Disabled for demonstration. Line 26
# 2. obj3 was being created using preferences2.csv. This will cause errors when running the test. It was adjusted to preferences.csv. Line 55


import EPop

obj1 = EPop.EPop(pop = 1000, 
                 children = 2, 
                 generations = 10, 
                 tourn = 5, 
                 prob = 0.15, 
                 fitnessTarget = 10,
                 growth = 7,
                 windowSize = 15,
                 settings = "settings.txt", 
                 guestsPref = "preferences.csv",
                 output = "output.csv")

#obj1.testSuite()
del obj1

lambdaPlus = True
useDiversity = False
obj2 = EPop.EPop(pop = 100, 
                 children = 2, 
                 generations = 20, 
                 tourn = 5, 
                 prob = 0.3, 
                 fitnessTarget = 10,
                 growth = 7,
                 windowSize = 10,
                 settings = "settings.txt", 
                 guestsPref = "preferences.csv",
                 output = "output.csv")

obj2.generations( useDiversity = useDiversity, lambdaPlus = lambdaPlus)
del obj2
lambdaPlus = False
obj3 = EPop.EPop(pop = 100, 
                 children = 2, 
                 generations = 10, 
                 tourn = 5, 
                 prob = 0.3, 
                 fitnessTarget = 10,
                 growth = 7,
                 windowSize = 10,
                 settings = "settings.txt", 
                 guestsPref = "preferences.csv",
                 output = "output.csv")
# Compares /w and w/o Crowding
obj3.testDiversity(lambdaPlus)
del obj3
     