import os
import subprocess
import json
import gzip
import shutil
import secrets

def randomStatementCoverage(testLines,cFilePath,outPutObjectPath,tcasFolderPath):
    maxPercentage=-1
    testSuit=[]
    lines=[]
    for line in testLines:
        lines.append(line.replace("\n",""))

    while maxPercentage<=100 and len(lines)>0:
        randomIndex=secrets.SystemRandom().randint(0,len(lines)-1)
        testLine=lines[randomIndex]
        res= lines.pop(randomIndex)
        command="cd "+tcasFolderPath+" ; " +outPutObjectPath+" "+testLine+"; gcov-11 "+cFilePath+" -m -j -b 2>&1 | tee "+tcasFolderPath+"/output.txt"
        process=subprocess.call(command,shell=True)
        coverageLines=[]

        with open(tcasFolderPath+"/output.txt", "r") as f:
            coverageLines=f.readlines()

        stmtCoveragePercent=0.0
        for eachLine in coverageLines:
            if "Lines executed" in eachLine:
                stmtCoveragePercent=float(eachLine.split(':')[1].split('%')[0])
                break
        if stmtCoveragePercent>maxPercentage:
            maxPercentage=stmtCoveragePercent
            testSuit.append(testLine)
            if stmtCoveragePercent==100.0:
                break

    with open(os.path.join(tcasFolderPath,"random-statement-suite.txt"),"w") as f:
        for test in testSuit:
            f.write(test+"\n")

def randomBranchCoverage(testLines,cFilePath,outPutObjectPath,tcasFolderPath):
    maxPercentage=-1
    testSuit=[]
    lines=[]
    for line in testLines:
        lines.append(line.replace("\n",""))

    while len(lines)>0:
        randomIndex=secrets.SystemRandom().randint(0,len(lines)-1)
        testLine=lines[randomIndex]
        res= lines.pop(randomIndex)
        command="cd "+tcasFolderPath+" ; " +outPutObjectPath+" "+testLine+"; gcov-11 "+cFilePath+" -m -j -b 2>&1 | tee "+tcasFolderPath+"/output.txt"
        process=subprocess.call(command,shell=True)
        coverageLines=[]

        with open(tcasFolderPath+"/output.txt", "r") as f:
            coverageLines=f.readlines()

        stmtCoveragePercent=0.0
        for eachLine in coverageLines:
            if "Taken at least once" in eachLine:
                stmtCoveragePercent=float(eachLine.split(':')[1].split('%')[0])
                break
        if stmtCoveragePercent>maxPercentage:
            maxPercentage=stmtCoveragePercent
            testSuit.append(testLine)
            if stmtCoveragePercent==100.0:
                break

    with open(os.path.join(tcasFolderPath,"random-branch-suite.txt"),"w") as f:
        for test in testSuit:
            f.write(test+"\n")

def totalStatementCoverage(testLines,cFilePath,outPutObjectPath,tcasFolderPath, processName):
    testSuit={}
    resTestSuit=[]
    lines=[]
    for line in testLines:
        lines.append(line.replace("\n",""))

    while len(lines)>0:
        testLine=lines[0]
        res= lines.pop(0)
        command="cd "+tcasFolderPath+" ; " +outPutObjectPath+" "+testLine+"; gcov-11 "+cFilePath+" -m -j -b 2>&1 | tee "+tcasFolderPath+"/output.txt"
        process=subprocess.call(command,shell=True)
        coverageLines=[]

        with open(tcasFolderPath+"/output.txt", "r") as f:
            coverageLines=f.readlines()

        stmtCoveragePercent=0.0
        for eachLine in coverageLines:
            if "Lines executed" in eachLine:
                stmtCoveragePercent=float(eachLine.split(':')[1].split('%')[0])
                testSuit[res] = stmtCoveragePercent
                break

        # if stmtCoveragePercent>maxPercentage:
        #     maxPercentage=stmtCoveragePercent
        #     testSuit.append(testLine)
        #     if stmtCoveragePercent==100.0:
        #         break

        #delete the gcda path in each iteration
        gcdapath=os.path.join(tcasFolderPath, processName+".gcda")
        command = "rm " + gcdapath
        process = subprocess.Popen(command, shell=True)
        process.wait()

    sortedTestSuit = dict(sorted(testSuit.items(), key=lambda item: item[1],reverse=True))

    #second pass
    maxPercentage=-1

    while maxPercentage<=100 and sortedTestSuit:
        testLine = list(sortedTestSuit.keys())[0]
        sortedTestSuit.pop(testLine)

        command="cd "+tcasFolderPath+" ; " +outPutObjectPath+" "+testLine+"; gcov-11 "+cFilePath+" -m -j -b 2>&1 | tee "+tcasFolderPath+"/output.txt"
        process=subprocess.call(command,shell=True)
        coverageLines=[]

        with open(tcasFolderPath+"/output.txt", "r") as f:
            coverageLines=f.readlines()

        stmtCoveragePercent=0.0
        for eachLine in coverageLines:
            if "Lines executed" in eachLine:
                stmtCoveragePercent=float(eachLine.split(':')[1].split('%')[0])
                break
        if stmtCoveragePercent>maxPercentage:
            maxPercentage=stmtCoveragePercent
            resTestSuit.append(testLine)
            if stmtCoveragePercent==100.0:
                break

    with open(os.path.join(tcasFolderPath,"total-statement-suite.txt"),"w") as f:
        for test in resTestSuit:
            f.write(test+"\n")

def totalBranchCoverage(testLines,cFilePath,outPutObjectPath,tcasFolderPath,processName):
    testSuit={}
    resTestSuit=[]
    lines=[]
    for line in testLines:
        lines.append(line.replace("\n",""))

    while len(lines)>0:
        testLine=lines[0]
        res= lines.pop(0)
        command="cd "+tcasFolderPath+" ; " +outPutObjectPath+" "+testLine+"; gcov-11 "+cFilePath+" -m -j -b 2>&1 | tee "+tcasFolderPath+"/output.txt"
        process=subprocess.call(command,shell=True)
        coverageLines=[]

        with open(tcasFolderPath+"/output.txt", "r") as f:
            coverageLines=f.readlines()

        stmtCoveragePercent=0.0
        for eachLine in coverageLines:
            if "Taken at least once" in eachLine:
                stmtCoveragePercent=float(eachLine.split(':')[1].split('%')[0])
                testSuit[res] = stmtCoveragePercent
                break

        # if stmtCoveragePercent>maxPercentage:
        #     maxPercentage=stmtCoveragePercent
        #     testSuit.append(testLine)
        #     if stmtCoveragePercent==100.0:
        #         break

        #delete the gcda path in each iteration
        gcdapath=os.path.join(tcasFolderPath, processName+".gcda")
        command = "rm " + gcdapath
        process = subprocess.Popen(command, shell=True)
        process.wait()

    sortedTestSuit = dict(sorted(testSuit.items(), key=lambda item: item[1],reverse=True))

    #second pass
    maxPercentage=-1

    while sortedTestSuit:
        testLine = list(sortedTestSuit.keys())[0]
        sortedTestSuit.pop(testLine)

        command="cd "+tcasFolderPath+" ; " +outPutObjectPath+" "+testLine+"; gcov-11 "+cFilePath+" -m -j -b 2>&1 | tee "+tcasFolderPath+"/output.txt"
        process=subprocess.call(command,shell=True)
        coverageLines=[]

        with open(tcasFolderPath+"/output.txt", "r") as f:
            coverageLines=f.readlines()

        stmtCoveragePercent=0.0
        for eachLine in coverageLines:
            if "Taken at least once" in eachLine:
                stmtCoveragePercent=float(eachLine.split(':')[1].split('%')[0])
                break
        if stmtCoveragePercent>maxPercentage:
            maxPercentage=stmtCoveragePercent
            resTestSuit.append(testLine)
            if stmtCoveragePercent==100.0:
                break

    with open(os.path.join(tcasFolderPath,"total-branch-suite.txt"),"w") as f:
        for test in resTestSuit:
            f.write(test+"\n")

def additionalStatementCoverage(testLines,cFilePath,outPutObjectPath,tcasFolderPath,processName):
    testSuit={}
    resTestSuit=[]
    lines=[]
    lineCountSet = {}
    lineSet = set()

    #change this for every process names


    for line in testLines:
        lines.append(line.replace("\n",""))

    while len(lines)>0:
        testLine=lines[0]
        res= lines.pop(0)
        print (tcasFolderPath)
        print (outPutObjectPath)
        print (testLine)
        print (cFilePath)
        print (tcasFolderPath)
        command="cd "+tcasFolderPath+" ; " +outPutObjectPath+" "+testLine+"; gcov-11 "+cFilePath+" -m -j -b 2>&1 | tee "+tcasFolderPath+"/output.txt"
        process=subprocess.call(command,shell=True)
        coverageLines=[]

        tcasJsonZip = os.path.join(tcasFolderPath, processName+".gcov.json.gz")
        tcasJsonFile = os.path.join(tcasFolderPath, processName+".gcov.json")
        print ('tcasJsonZip'+tcasJsonZip)

        with gzip.open(tcasJsonZip, 'rb') as f_in:
            with open(tcasJsonFile, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        f = open(tcasJsonFile)
        data = json.load(f)
        lines2 = data["files"][0]["lines"]

        testSuit[res] = set()

        for i in lines2:
            lineSet.add(i["line_number"])
            if i["count"] > 0:
                testSuit[res].add(i["line_number"])

        lineCountSet[res] = len(testSuit[res])

        #delete the gcda path in each iteration
        gcdapath=os.path.join(tcasFolderPath, processName+".gcda")
        command = "rm " + gcdapath + " " + tcasJsonZip + " " + tcasJsonFile
        process = subprocess.Popen(command, shell=True)
        process.wait()

    #sorting the key value in desc
    sortedTestSuit = dict(sorted(lineCountSet.items(), key=lambda item: item[1],reverse=True))
    with open(os.path.join(tcasFolderPath,'printDict.txt'),"w") as f:
        for key in testSuit:
            f.write(key+":")
            f.write(str(sortedTestSuit[key])+"\n")

    print(lineSet)
    #second pass : select the testLine which has most coverage and execute that
    while (len(sortedTestSuit) > 0) and (len(lineSet) > 0):
        testLine = list(sortedTestSuit.keys())[0]
        currSet = testSuit[testLine]
        if len(currSet)==0:
            break
        sortedTestSuit.pop(testLine)
        testSuit.pop(testLine)
        lineSet = lineSet.difference(currSet)
        print (len(lineSet))
        #update the dicts subtracting the currSet
        for k,v in testSuit.items():
            newSet = v.difference(currSet)
            testSuit[k] = newSet
            sortedTestSuit[k] = len(newSet)

        #sorting the key value in desc again
        sortedTestSuit = dict(sorted(sortedTestSuit.items(), key=lambda item: item[1],reverse=True))




        resTestSuit.append(testLine)

    with open(os.path.join(tcasFolderPath,"additional-statement-suite.txt"),"w") as f:
        for test in resTestSuit:
            f.write(test+"\n")

def additionalBranchCoverage(testLines,cFilePath,outPutObjectPath,tcasFolderPath,processName):
    testSuit={}
    resTestSuit=[]
    lines=[]
    lineCountSet = {}
    lineSet = set()

    #change this for every process names


    for line in testLines:
        lines.append(line.replace("\n",""))

    while len(lines)>0:
        testLine=lines[0]
        res= lines.pop(0)
        print (tcasFolderPath)
        print (outPutObjectPath)
        print (testLine)
        print (cFilePath)
        print (tcasFolderPath)
        command="cd "+tcasFolderPath+" ; " +outPutObjectPath+" "+testLine+"; gcov-11 "+cFilePath+" -m -j -b 2>&1 | tee "+tcasFolderPath+"/output.txt"
        process=subprocess.call(command,shell=True)
        coverageLines=[]

        tcasJsonZip = os.path.join(tcasFolderPath, processName+".gcov.json.gz")
        tcasJsonFile = os.path.join(tcasFolderPath, processName+".gcov.json")
        print ('tcasJsonZip'+tcasJsonZip)

        with gzip.open(tcasJsonZip, 'rb') as f_in:
            with open(tcasJsonFile, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        f = open(tcasJsonFile)
        data = json.load(f)
        lines2 = data["files"][0]["lines"]

        testSuit[res] = set()

        for i in lines2:
            #lineSet.add(i["line_number"])
            branches=i["branches"]
            lineNumber= i["line_number"]
            if len(branches)>0:
                for m in range(len(branches)):
                    lineSet.add(str(lineNumber)+"-"+str(m))
                    if branches[m]['count']>0:
                        testSuit[res].add(str(lineNumber)+"-"+str(m))

        lineCountSet[res] = len(testSuit[res])

        #delete the gcda path in each iteration
        gcdapath=os.path.join(tcasFolderPath, processName+".gcda")
        command = "rm " + gcdapath + " " + tcasJsonZip + " " + tcasJsonFile
        process = subprocess.Popen(command, shell=True)
        process.wait()

    #sorting the key value in desc
    sortedTestSuit = dict(sorted(lineCountSet.items(), key=lambda item: item[1],reverse=True))
    with open(os.path.join(tcasFolderPath,'printDict.txt'),"w") as f:
        for key in testSuit:
            f.write(key+":")
            f.write(str(testSuit[key])+"\n")

    #second pass : select the testLine which has most coverage and execute that
    while (len(sortedTestSuit) > 0) and (len(lineSet) > 0):
        testLine = list(sortedTestSuit.keys())[0]
        currSet = testSuit[testLine]
        if len(currSet)==0:
            break

        sortedTestSuit.pop(testLine)
        testSuit.pop(testLine)
        lineSet = lineSet.difference(currSet)
        print (len(lineSet))
        #update the dicts subtracting the currSet
        for k,v in testSuit.items():
            newSet = v.difference(currSet)
            testSuit[k] = newSet
            sortedTestSuit[k] = len(newSet)

        #sorting the key value in desc again
        sortedTestSuit = dict(sorted(sortedTestSuit.items(), key=lambda item: item[1],reverse=True))




        resTestSuit.append(testLine)

    with open(os.path.join(tcasFolderPath,"additional-branch-suite.txt"),"w") as f:
        for test in resTestSuit:
            f.write(test+"\n")


def tcasProcess(dir):
    tcasFolderPath=os.path.join(dir,'tcas')
    cFilePath=os.path.join(tcasFolderPath,'tcas.c')
    outPutObjectPath=os.path.join(tcasFolderPath,'tcas')
    command="gcc-11 --coverage -Wno-return-type -g -o "+outPutObjectPath+" "+cFilePath+";"
    process=subprocess.Popen(command,shell=True)
    process.wait()
    testFilePath=os.path.join(tcasFolderPath,'universe.txt')
    lines=[]
    with open(testFilePath,"r") as f:
        lines=f.readlines()

    randomStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)
    gcdapath=os.path.join(tcasFolderPath, "tcas.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    totalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'tcas')
    gcdapath=os.path.join(tcasFolderPath, "tcas.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    additionalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'tcas')
    print("done with statement coverage")

    ##deleting gcda file code her


    randomBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)
    gcdapath=os.path.join(tcasFolderPath, "tcas.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    totalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'tcas')
    gcdapath=os.path.join(tcasFolderPath, "tcas.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    additionalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'tcas')

    ##deleting gcda file code her


def totinfoProcess(dir):
    tcasFolderPath=os.path.join(dir,'totinfo')
    cFilePath=os.path.join(tcasFolderPath,'totinfo.c')
    outPutObjectPath=os.path.join(tcasFolderPath,'totinfo')
    command="gcc-11 --coverage -Wno-return-type -g -o "+outPutObjectPath+" "+cFilePath+" -lm ;"
    process=subprocess.Popen(command,shell=True)
    process.wait()
    testFilePath=os.path.join(tcasFolderPath,'universe.txt')
    lines=[]
    with open(testFilePath,"r") as f:
        lines=f.readlines()

    randomStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)

    ##deleting gcda file code her
    gcdapath=os.path.join(tcasFolderPath, "totinfo.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()

    totalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath,'totinfo')
    gcdapath=os.path.join(tcasFolderPath, "totinfo.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    additionalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath,'totinfo')

    randomBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)
    ##deleting gcda file code her
    gcdapath=os.path.join(tcasFolderPath, "totinfo.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()

    totalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath,'totinfo')
    gcdapath=os.path.join(tcasFolderPath, "totinfo.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    additionalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath,'totinfo')

    



def scheduleProcess(dir):
        tcasFolderPath=os.path.join(dir,'schedule')
        cFilePath=os.path.join(tcasFolderPath,'schedule.c')
        outPutObjectPath=os.path.join(tcasFolderPath,'schedule')
        command="gcc-11 --coverage -Wno-return-type -g -o "+outPutObjectPath+" "+cFilePath+";"
        process=subprocess.Popen(command,shell=True)
        process.wait()
        testFilePath=os.path.join(tcasFolderPath,'universe.txt')
        lines=[]
        with open(testFilePath,"r") as f:
            lines=f.readlines()

        randomStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)

        ##deleting gcda file code her
        gcdapath=os.path.join(tcasFolderPath, "schedule.gcda")
        command = "rm " + gcdapath
        process = subprocess.Popen(command, shell=True)
        process.wait()
        totalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'schedule')
        gcdapath=os.path.join(tcasFolderPath, "schedule.gcda")
        command = "rm " + gcdapath
        process = subprocess.Popen(command, shell=True)
        process.wait()
        additionalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'schedule')
        randomBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)
        ##deleting gcda file code her
        gcdapath=os.path.join(tcasFolderPath, "schedule.gcda")
        command = "rm " + gcdapath
        process = subprocess.Popen(command, shell=True)
        process.wait()
        totalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'schedule')
        gcdapath=os.path.join(tcasFolderPath, "schedule.gcda")
        command = "rm " + gcdapath
        process = subprocess.Popen(command, shell=True)
        process.wait()
        additionalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'schedule')

def schedule2Process(dir):
    tcasFolderPath=os.path.join(dir,'schedule2')
    cFilePath=os.path.join(tcasFolderPath,'schedule2.c')
    outPutObjectPath=os.path.join(tcasFolderPath,'schedule2')
    command="gcc-11 --coverage -Wno-return-type -g -o "+outPutObjectPath+" "+cFilePath+";"
    process=subprocess.Popen(command,shell=True)
    process.wait()
    testFilePath=os.path.join(tcasFolderPath,'universe.txt')
    lines=[]
    with open(testFilePath,"r") as f:
        lines=f.readlines()

    randomStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)

    ##deleting gcda file code her
    gcdapath=os.path.join(tcasFolderPath, "schedule2.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()

    totalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'schedule2')
    gcdapath=os.path.join(tcasFolderPath, "schedule2.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    additionalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'schedule2')

    randomBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)
    ##deleting gcda file code her
    gcdapath=os.path.join(tcasFolderPath, "schedule2.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    totalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'schedule2')
    gcdapath=os.path.join(tcasFolderPath, "schedule2.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    additionalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'schedule2')

def printtokensProcess(dir):
    tcasFolderPath=os.path.join(dir,'printtokens')
    cFilePath=os.path.join(tcasFolderPath,'printtokens.c')
    outPutObjectPath=os.path.join(tcasFolderPath,'printtokens')
    command="gcc-11 --coverage -Wno-return-type -g -o "+outPutObjectPath+" "+cFilePath+";"
    process=subprocess.Popen(command,shell=True)
    process.wait()
    testFilePath=os.path.join(tcasFolderPath,'universe.txt')
    lines=[]
    with open(testFilePath,"r") as f:
        lines=f.readlines()

    randomStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)

    ##deleting gcda file code her
    gcdapath=os.path.join(tcasFolderPath, "printtokens.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    totalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'printtokens')
    gcdapath=os.path.join(tcasFolderPath, "printtokens.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    additionalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'printtokens')
    randomBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)
    ##deleting gcda file code her
    gcdapath=os.path.join(tcasFolderPath, "printtokens.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    totalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'printtokens')
    gcdapath=os.path.join(tcasFolderPath, "printtokens.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    additionalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'printtokens')


def printtokens2Process(dir):
    tcasFolderPath=os.path.join(dir,'printtokens2')
    cFilePath=os.path.join(tcasFolderPath,'printtokens2.c')
    outPutObjectPath=os.path.join(tcasFolderPath,'printtokens2')
    command="gcc-11 --coverage -Wno-return-type -g -o "+outPutObjectPath+" "+cFilePath+";"
    process=subprocess.Popen(command,shell=True)
    process.wait()
    testFilePath=os.path.join(tcasFolderPath,'universe.txt')
    lines=[]
    with open(testFilePath,"r") as f:
        lines=f.readlines()

    randomStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)

    ##deleting gcda file code her
    gcdapath=os.path.join(tcasFolderPath, "printtokens2.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    totalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'printtokens2')
    gcdapath=os.path.join(tcasFolderPath, "printtokens2.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    additionalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'printtokens2')
    randomBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)
    ##deleting gcda file code her
    gcdapath=os.path.join(tcasFolderPath, "printtokens2.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    totalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'printtokens2')
    gcdapath=os.path.join(tcasFolderPath, "printtokens2.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    additionalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'printtokens2')


def replaceProcess(dir):
    tcasFolderPath=os.path.join(dir,'replace')
    cFilePath=os.path.join(tcasFolderPath,'replace.c')
    outPutObjectPath=os.path.join(tcasFolderPath,'replace')
    command="gcc-11 --coverage -Wno-return-type -g -o "+outPutObjectPath+" "+cFilePath+" -lm ;"
    process=subprocess.Popen(command,shell=True)
    process.wait()
    testFilePath=os.path.join(tcasFolderPath,'universe.txt')
    lines=[]
    with open(testFilePath,"r") as f:
        lines=f.readlines()

    randomStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)

    ##deleting gcda file code her
    gcdapath=os.path.join(tcasFolderPath, "replace.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    totalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'replace')
    gcdapath=os.path.join(tcasFolderPath, "replace.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    additionalStatementCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'replace')

    randomBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath)
    ##deleting gcda file code her
    gcdapath=os.path.join(tcasFolderPath, "replace.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    totalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'replace')
    gcdapath=os.path.join(tcasFolderPath, "replace.gcda")
    command = "rm " + gcdapath
    process = subprocess.Popen(command, shell=True)
    process.wait()
    additionalBranchCoverage(lines,cFilePath,outPutObjectPath,tcasFolderPath, 'replace')

def main():
    path=os.path.join(os.getcwd(),'benchmarks')
    tcasProcess(path)
    totinfoProcess(path)
    scheduleProcess(path)
    schedule2Process(path)
    printtokensProcess(path)
    printtokens2Process(path)
    replaceProcess(path)
if __name__ == "__main__":
    main()
