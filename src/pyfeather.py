import featherutils
import os
import sys

def getYieldedTemplate(projPath,file,templateFileName):

    newTemplateFileName = featherutils.findFileAtPathWithName(projPath,templateFileName)
    finalcontent = ""
    fullTemplatePath = str(projPath +os.sep + newTemplateFileName)

    print("template file is "+templateFileName)
    with open(fullTemplatePath, "r") as ins:
        for line in ins:            
            if(line.strip().startswith("%")):
                if(line.find("yield") > -1):
                    if(line.find(":")>-1):
                        yieldtag = line[line.find(":")+1:]
                    else:
                        yieldtag = ""
                    finalcontent+=featherutils.getYieldContentInFile(projPath,file,yieldtag)
                    print("yielding with "+ file)
            else:
                finalcontent+=str(line +"\n")

    return finalcontent


def exportBuiltFile(projPath,filename,contents):
    if not os.path.exists(projPath+os.sep+"build"): os.makedirs(projPath+os.sep+"build")
    filename = filename[:filename.find(".fea")] + ".html"
    target = open(projPath+os.sep+"build"+os.sep+filename, 'w')
    target.write(contents)
    
def getUpdatedFileContents(projPath, file):
    fullFilePath = str(projPath +os.sep + file)
    
    print("opening " + fullFilePath)

    templateFileName = "template"
    
    with open(fullFilePath, "r") as ins:
        for line in ins: 
            if(line.strip().startswith("%")):             
                if(line.find("childof") > -1):      
                    templateFileName = line[line.find(" ")+1:].rstrip()   #remove newline
                    return getYieldedTemplate(projPath,file,templateFileName)
    ins.close()
    return ""
        

#program starts here
 
if(len(sys.argv) > 1):
    projPath = str(sys.argv[2])
else:
    projPath = input("Where is the local HTML/CSS project that you would like PyFeather to build? \n")

files=featherutils.getFilesAtPath(projPath)

for file in files:
    if(file.endswith(".fea.html")):
        updatedContent = getUpdatedFileContents( projPath , file  )
        exportBuiltFile(projPath,file,updatedContent);


print ("Built project at " + projPath)

k=input("press return to exit")
