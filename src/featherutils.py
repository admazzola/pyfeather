from os import walk
import os

def getFilesAtPath(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break
    return f

def findFileAtPathWithName(projPath,templateFileName):
    files = getFilesAtPath(projPath)
    print("searching for file " + templateFileName)
    for file in files:
        if(file.startswith(templateFileName)):
            print("found file " + file)
            return file
    return templateFileName

def getYieldContentInFile(projPath,file,yieldtag):
    #if tag is empty then return everything that is not in contentfor
    fullFilePath = str(projPath +os.sep + file)
    content=""    
    if(len(yieldtag.strip()) == 0):
        with open(fullFilePath, "r") as ins:
            insideOtherYield=False
            for line in ins:
                if(line.strip().startswith("%")):
                    if(line.find("contentfor") > -1):
                        contentfortag = line[line.find(":")+1:]
                        insideOtherYield = True
                    if(line.find("end") > -1):
                        insideOtherYield=False
                elif(not insideOtherYield):
                    content+=line
    else:
        with open(fullFilePath, "r") as ins:
            insideMyYield=False
            for line in ins:
                if(line.strip().startswith("%")):
                    if(line.find("contentfor") > -1):
                        contentfortag = line[line.find(":")+1:]
                        insideMyYield = contentfortag == yieldtag
                    if(line.find("end") > -1):
                        insideMyYield=False
                elif(insideMyYield):
                    content+=line
    print("yielding " + yieldtag + " " + content)
    return content
