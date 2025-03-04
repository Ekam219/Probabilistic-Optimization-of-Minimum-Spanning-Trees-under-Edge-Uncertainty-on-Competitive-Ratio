
from graph import *
from optimal import *
from generator import *
from algoCycle import *
from algoCut import *
import random
import os

script_dir = os.path.dirname(__file__)

def CompetitiveRatio(a, b):
    if b == 0:
        return 1.0
    else:
        return a/b


# TESTING for optimal query set
# randomly generated cases
testcases = 0
testcases = int(input("Enter number of cases to generate and test: "))
debug = input("Do you want to print generator arguments? [Y/N]: ")
totalCycleSet = 0
totalCutSet = 0
totalOptSet = 0
for i in range(1, testcases + 1):
    generatorObject = GraphGenerator(debug == 'Y')
    g = generatorObject.constructGraphB(
        100, 200, random.uniform(0, 100), random.uniform(100, 200))
    # print(g)
    optimalSet = optimalQuerySet(g)
    # assert checkOPT(g, optimalSet)
    algoCycleObject = CycleModel(g)
    algoCycleQuery = algoCycleObject.Q
    algoCutObject = CutModel(g)
    algoCutQuery = algoCutObject.Q
    print("Algo Cycle Competitve Ratio:", CompetitiveRatio(len(
        algoCycleQuery), len(optimalSet)))
    print("Algo Cut Competitve Ratio:", CompetitiveRatio(len(
        algoCutQuery), len(optimalSet)))
    totalCycleSet += len(algoCycleQuery)
    totalCutSet += len(algoCutQuery)
    totalOptSet += len(optimalSet)
    assert len(algoCycleQuery) <= 2 * len(optimalSet)
    assert len(algoCutQuery) <= 2 * len(optimalSet)
    print("Random test " + str(i) + " passed!")

print("Average Algo Cycle Competitve Ratio:",
      CompetitiveRatio(totalCycleSet, totalOptSet))
print("Average Algo Cut Competitve Ratio:",
      CompetitiveRatio(totalCutSet, totalOptSet))