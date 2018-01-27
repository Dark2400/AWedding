import EPop
import seetingArrangement

obj1 = EPop.EPop(pop = 5000, children = 2, generations = 10, tourn = 5, prob = 0.2, fitnessTarget = 10, settings = "settings.txt", guestsPref = "preferences2.csv")
#plan = seetingArrangement.seetingArrangement(18, 15, 6)
#plan.plan = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, -1, 12, 13, 14, 15, -1, -1]
#print(obj1.testFitness(plan))
obj1.generations()


 
