'''
Created on Feb 27, 2012

@author: josh-daniel
'''


from numpy import random
import math
import json
import os

pathname = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(pathname, "fakeInput.txt")
fileOut=open(filename, "w")

nBills = 1000
nLegislators = 435

for i in range(nBills):
    votes = []
    # Generate a list of nLegislators votes, where each vote is a -1 (nay), 0 (abstain), or 1 (yea).
    for j in range(nLegislators):
        # Generate -1, 0, or 1, and build into a list.
        votes.append(math.floor(random.rand()*3)-1)
    outString = json.dumps(["bill"+str(i), "bill"+str(i)+"Description", votes]) + "\n"
    fileOut.write(outString)
        
fileOut.close()

