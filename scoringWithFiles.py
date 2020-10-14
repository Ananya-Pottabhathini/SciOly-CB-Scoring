"""
This is the script for my CB Scoring Application.
The aim of the application is to calculate a team's CB score given their raw
data.
"""

def createValuesDict(fname):
    try:
        valuesFile = open(fname, 'r')
    except IOError:
        return("Looks the file you entered does not exist. Please check the spelling of your file name.")    
    else: 
        valuesInfo = valuesFile.readlines()
        valuesFile.close()
        valuesDict = {}
        for num in range(len(valuesInfo)):
            valuesInfo[num] = int(valuesInfo[num].strip())
            valuesDict[num] = valuesInfo[num]
        return valuesDict

def calculateBonus(time):
    minutes = int(time)
    seconds = (time - minutes) * 100
    totalSeconds = minutes * 60 + seconds
    if totalSeconds > 600:
        totalSeconds = 600
    bonus = 4* (600 - totalSeconds)
    return(bonus)

def calculatePoints(question, answered, numErrors, valuesDict):
    questionValuesDict = valuesDict
    if answered == 0:
        finalPoints = 0
    else:
        baseValue = questionValuesDict[question]
        if numErrors <= 2:
            deduction = 0
        else:
            deduction = (numErrors - 2) * 100
        if deduction > baseValue:
            deduction = baseValue
        finalPoints = baseValue - deduction
    return finalPoints

def calculateTeamScore(teamDataList, valuesDict):
    questionValuesDict = valuesDict
    totalPoints = 0
    for (question, answered, numErrors) in teamDataList:
        if question == 0:
            if answered == 1:
                time = numErrors
                bonus = calculateBonus(time)
                totalPoints += (questionValuesDict[question] + bonus)
        else:
            totalPoints += calculatePoints(question, answered, numErrors, questionValuesDict)
    return totalPoints

def sortDict(dictname):
    sortedDict = {}
    scoresList = list(dictname.values())
    scoresList.sort(reverse = True)
    for score in scoresList:
        for key in dictname.keys():
            if dictname[key] == score:
                sortedDict[key] = score
    return sortedDict

def findSectionLength(fullList):
    sectionLength = 0
    for num in range(len(fullList)):
        if fullList[num] != '':
            sectionLength +=1
        else:
            break
    return sectionLength

def generateDataDict(fname):
    try:
        dataFile = open(fname, 'r')
    except IOError:
        return("Looks the file you entered does not exist. Please check the spelling of your file name.")    
    else: 
        dataInfo = dataFile.readlines()
        dataFile.close()
        dataDict = {}
        for num in range(len(dataInfo)):
            dataInfo[num] = dataInfo[num].strip()
        sectionLength = findSectionLength(dataInfo)
        for num in range(len(dataInfo)):
            if num % (sectionLength + 1) == 0:
                key = dataInfo[num]
                dataDict[key] = [eval(dataInfo[num+1])]
            elif (num % (sectionLength + 1) == sectionLength) or (num % (sectionLength + 1) == 1):
                continue
            else:
                dataDict[key] += [eval(dataInfo[num])]
        return dataDict

def generateScores(dataFile, valuesFile):
    scoresDict = {}
    valuesDict = createValuesDict(valuesFile)
    dataDict = generateDataDict(dataFile)
    for key in dataDict.keys():
        scoresDict[key] = calculateTeamScore(dataDict[key], valuesDict)
    scoresDict = sortDict(scoresDict)
    return scoresDict

def generateScoresFile(dataFile, valuesFile, finalFile):
    scoresDict = generateScores(dataFile, valuesFile)
    finalScores = []
    for item in scoresDict.items():
        finalScores.append(item)
    finalScoresFile = open(finalFile, 'w')
    finalScoresFile.write("Here are the final CB scores for each team. \n")
    for (rank, (name, score)) in enumerate(finalScores):
        finalScoresFile.write(str(rank + 1) + '. ' + str(name) + ' - ' + str(score) + '\n')
    finalScoresFile.close()
    print("Text file with final team scores has been generated. Look for " + finalFile + " file on your local machine.")
    

              


        
        
    
                      
