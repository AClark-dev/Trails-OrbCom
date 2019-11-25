import csv
import itertools as it

# Parameters
l = 3 #Line Length
mustInclude = ['Seal']
mustExclude = ["Heaven's Eye", 'EP Cut 1', 'Evade 1']

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

# Data Processing
cbnTuple = list(it.combinations(quartz,l))

sumDict = []
keys = ['Earth','Water','Fire','Wind','Time','Space','Mirage']

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

lstDict = []
for i in range(len(sumDict)):
    lst = []
    for j in range(len(arts)):
        sum = 0
        for k in keys:
            if sumDict[i][k] >= arts[j][k]:
                sum += 1
        if sum == 7:
            newdict = {
                    'Name': arts[j]['Name'],
                    'Effect': arts[j]['Effect'],
                    'Cast Cost': arts[j]['Cast Cost']
                }
            lst.append(newdict)
    lstDict.append(lst)
    
# Format the output
#for i in range(len(cbnTuple)):
#    print('Quartz:')
#    for j in range(l):
#        print(cbnTuple[i][j]['Name'] + ': ' + cbnTuple[i][j]['Effect'])
#    print('Arts:')
#    for k in range(len(lstDict[i])):
#            print(lstDict[i][k]['Name'] + ' (' + lstDict[i][k]['Cast Cost'] + ' EP): ' + lstDict[i][k]['Effect'])
#    print('')
#    print('')
    
maxval = 0
for i in range(len(cbnTuple)):
    if len(lstDict[i]) > maxval:
        maxval = len(lstDict[i])
#newLstDict = []
#for i in range(len(lstDict)):
#    if len(lstDict[i]) >= maxval-2:
#        newLstDict.append(lstDict[i])

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
        
idxSort = list(zip(idxQuartz, idxArts))
idxSort.sort(key = lambda row: len(row[1]), reverse=True)
idxQuartz, idxArts = list(zip(*idxSort))
    
#with open('Orbments.csv', mode='w', newline='') as csv_file:
#    fieldnames = ['Quartz Name', 'Quartz Effect', 'Art Name', 'Cast Cost', 'Art Effect']
#    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#    
#    writer.writeheader()
#    for i in range(len(cbnTuple)):
#        n = len(lstDict[i])
#        for j in range(max(n,l)):
#            if j < l:
#                qname = cbnTuple[i][j]['Name']
#                qeffect = cbnTuple[i][j]['Effect']
#            else:
#                qname = ''
#                qeffect = ''
#            if j < n:
#                aname = lstDict[i][j]['Name']
#                acost = lstDict[i][j]['Cast Cost']
#                aeffect = lstDict[i][j]['Effect']
#            else:
#                aname = ''
#                acost = ''
#                aeffect = ''
#            writer.writerow({'Quartz Name': qname, 'Quartz Effect': qeffect, 'Art Name': aname, 'Cast Cost': acost, 'Art Effect': aeffect})
#        writer.writerow({'Quartz Name': '', 'Quartz Effect': '', 'Art Name': '', 'Cast Cost': '', 'Art Effect': ''})

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