import sys
import os
import subprocess

def findBugReport(benchmarkName,testInputFileName):
    benchmarkFolderPath=os.path.join(os.getcwd(),'benchmarks/'+benchmarkName)
    
    '''
    get original test suite fault detection
    '''
    originalObjectFilePath=os.path.join(benchmarkFolderPath,benchmarkName)
    originalCfilePath=os.path.join(benchmarkFolderPath,benchmarkName+".c")
    originalInputFilePath=os.path.join(benchmarkFolderPath,testInputFileName+'.txt')

    if(benchmarkName=="totinfo" or benchmarkName=="replace"):
        command="gcc-11 --coverage -Wno-return-type -g -o "+originalObjectFilePath+" "+originalCfilePath+ " -lm"
        process = subprocess.call(command, shell=True)
    else:
        command="gcc-11 --coverage -Wno-return-type -g -o "+originalObjectFilePath+" "+originalCfilePath
        process = subprocess.call(command, shell=True)


    listDirs=os.listdir(benchmarkFolderPath)
    buggyDirList=[]
    for dirname in listDirs:
        if dirname.startswith('v'):
            buggyDirList.append(dirname)

    '''
        count faults for universe.txt
    '''
    lines=[]

    with open(os.path.join(benchmarkFolderPath,testInputFileName+'.txt'),"r") as f: #can be different
        lines= f.readlines()
    totalFaults=0
    caughtVersions=[]

    for buggyVersionName in buggyDirList:
        buggyPath= os.path.join(benchmarkFolderPath,buggyVersionName)
        buggyCPath=os.path.join(buggyPath, benchmarkName+".c")
        buggyObjectPath=os.path.join(buggyPath,benchmarkName)

        if(benchmarkName=="totinfo" or benchmarkName=="replace"):
            command="gcc-11 -Wno-return-type -g -o "+buggyObjectPath+" "+buggyCPath+ " -lm"
            process = subprocess.call(command, shell=True)
        else:
            command="gcc-11  -Wno-return-type -g -o "+buggyObjectPath+" "+buggyCPath
            process = subprocess.call(command, shell=True)

        for line in lines:
            line=line.replace("\n","")
            command="cd " + benchmarkFolderPath + " && " + buggyObjectPath + " "+ line + " 2>&1 | tee " + buggyPath+"/wrongoutput.txt"
            process = subprocess.call(command, shell=True)

            command="cd " + benchmarkFolderPath + " && " + originalObjectFilePath + " "+ line + " 2>&1 | tee " + benchmarkFolderPath+"/correctoutput.txt"
            process = subprocess.call(command, shell=True)
            correctValue=0
            buggyValue=0
            with open(benchmarkFolderPath+"/correctoutput.txt", "rb") as f:
                correctValue=f.read()
            with open(buggyPath+"/wrongoutput.txt", "rb") as f:
                buggyValue=f.read()

            if correctValue!=buggyValue:
                totalFaults+=1
                caughtVersions.append(buggyVersionName)
                break

    with open(os.path.join(benchmarkFolderPath, testInputFileName+"-FaultReport.txt" ), "w") as f:
        f.write("Total Number of Faults: " + str(totalFaults) + "\n")
        f.write("List of Faulty Versions Detected: " + str(caughtVersions))



if __name__ == "__main__":

    argumentList=sys.argv
    benchmarkName=argumentList[1]
    
    findBugReport(benchmarkName,'universe')

    findBugReport(benchmarkName,'random-statement-suite')
    findBugReport(benchmarkName,'random-branch-suite')

    findBugReport(benchmarkName,'total-statement-suite')
    findBugReport(benchmarkName,'total-branch-suite')
    
    findBugReport(benchmarkName,'additional-statement-suite')
    findBugReport(benchmarkName,'additional-branch-suite')
