import csv
import itertools as it

# Parameters
l = 3 #Line Length
mustInclude = ['Seal'] #Quartz which must be included
mustExclude = ["Heaven's Eye", 'EP Cut 1', 'Evade 1'] #Quartz which must be excluded

# What about orbment tiers?
# What about orbment elemental slots?
# What about required arts?

#
# Input data
#

# Open and input the quartz
with open('Quartz.csv') as fQuartz:
    csv_reader = csv.DictReader(fQuartz)
    
    quartz = []
    
    for row in csv_reader:
        if row['Enabled'] == 'TRUE':
            newrow = {
                    'Earth': int(row['Earth']),
                    'Effect': row['Effect'],
                    'Fire': int(row['Fire']),
                    'Mirage': int(row['Mirage']),
                    'Name': row['Name'],
                    'Space': int(row['Space']),
                    'Time': int(row['Time']),
                    'Water': int(row['Water']),
                    'Wind': int(row['Wind'])
                }
            quartz.append(newrow)

# Open and input the arts
with open('Arts.csv') as fArts:
    csv_reader = csv.DictReader(fArts)
    
    arts = []
    
    for row in csv_reader:
        newrow = {
                'Cast Cost': row['Cast Cost'],
                'Earth': int(row['Earth']),
                'Effect': row['Effect'],
                'Fire': int(row['Fire']),
                'Mirage': int(row['Mirage']),
                'Name': row['Name'],
                'Space': int(row['Space']),
                'Time': int(row['Time']),
                'Water': int(row['Water']),
                'Wind': int(row['Wind'])
            }
        arts.append(newrow)

#
# Process data
#

# Find combinations of 'l' (line length) many quartz without repeats
cbnTuple = list(it.combinations(quartz,l))

# Initialise list and keys
sumDict = []
keys = ['Earth','Water','Fire','Wind','Time','Space','Mirage']

# Find dict of element values for each quartz combination and add to the list 'sumDict'
for i in range(len(cbnTuple)):
    val = [0]*7
    for j in range(l):
        qtz = cbnTuple[i][j]
        val[0] += qtz['Earth']
        val[1] += qtz['Water']
        val[2] += qtz['Fire']
        val[3] += qtz['Wind']
        val[4] += qtz['Time']
        val[5] += qtz['Space']
        val[6] += qtz['Mirage']
    sumDict.append(dict(zip(keys, val)))

# Initialise list
lstDict = []

# Loop over all the dicts in 'sumDict'
# i.e. the elemental values corresponding to each quartz combination
for i in range(len(sumDict)):
    lst = []
    # Loop over all the arts
    for j in range(len(arts)):
        sum = 0
        # Loop over all the keys
        # i.e. the 7 different elements
        for k in keys:
            # For this element of this quartz combination,
            # check if it is above the number of this element required for this art
            if sumDict[i][k] >= arts[j][k]:
                sum += 1
        # If all of the elements are above the threshold for this art, add it as a dict to the list 'lst' 
        if sum == 7:
            newdict = {
                    'Name': arts[j]['Name'],
                    'Effect': arts[j]['Effect'],
                    'Cast Cost': arts[j]['Cast Cost']
                }
            lst.append(newdict)
    lstDict.append(lst)

# Check that specified quartz have been included/excluded
idxQuartz = []
idxArts = []
for i in range(len(cbnTuple)):
    countInclude = 0
    countExclude = 0
    for j in range(l):
        if cbnTuple[i][j]['Name'] in mustInclude:
            countInclude += 1
        if cbnTuple[i][j]['Name'] in mustExclude:
            countExclude += 1
    if countInclude == len(mustInclude) and countExclude == 0:
        idxQuartz.append(cbnTuple[i])
        idxArts.append(lstDict[i])

# Sort the data
# By number of arts in descending order
idxSort = list(zip(idxQuartz, idxArts))
idxSort.sort(key = lambda row: len(row[1]), reverse=True)
idxQuartz, idxArts = list(zip(*idxSort))

#
# Output data
#

# Output quarts combinations and resulting arts
with open('Orbments.csv', mode='w', newline='') as csv_file:
    fieldnames = ['Quartz Name', 'Quartz Effect', 'Art Name', 'Cast Cost', 'Art Effect']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    writer.writeheader()
    for i in range(len(idxQuartz)):
        n = len(idxArts[i])
        for j in range(max(n,l)):
            if j < l:
                qname = idxQuartz[i][j]['Name']
                qeffect = idxQuartz[i][j]['Effect']
            else:
                qname = ''
                qeffect = ''
            if j < n:
                aname = idxArts[i][j]['Name']
                acost = idxArts[i][j]['Cast Cost']
                aeffect = idxArts[i][j]['Effect']
            else:
                aname = ''
                acost = ''
                aeffect = ''
            writer.writerow({'Quartz Name': qname, 'Quartz Effect': qeffect, 'Art Name': aname, 'Cast Cost': acost, 'Art Effect': aeffect})
        writer.writerow({'Quartz Name': '', 'Quartz Effect': '', 'Art Name': '', 'Cast Cost': '', 'Art Effect': ''})
print('Done processing')
