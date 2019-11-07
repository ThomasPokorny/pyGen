"""

@autor Thomas Pokorny

 ________  ___    ___ ________  _______   ________      
|\   __  \|\  \  /  /|\   ____\|\  ___ \ |\   ___  \    
\ \  \|\  \ \  \/  / | \  \___|\ \   __/|\ \  \\ \  \   
 \ \   ____\ \    / / \ \  \  __\ \  \_|/_\ \  \\ \  \  
  \ \  \___|\/  /  /   \ \  \|\  \ \  \_|\ \ \  \\ \  \ 
   \ \__\ __/  / /      \ \_______\ \_______\ \__\\ \__\
    \|__||\___/ /        \|_______|\|_______|\|__| \|__|
         \|___|/                                        
                                                        

@brief a probably completely useless tool that I wrote when I was bored instead of actually learning for Uni


"""

import json
import sys
import os

versionString = "pyGen version: 1.0"
helpString = "Calling Synopsis:\npyGen [path_to_json_file] [-a author]"

## calling arguments
commandAuthor = "-a"

#### SOME JAVA IDENTIFIERS

pubJ    = "public"
priJ    = "private"

statJ   = "static"

classJ  = "class"
abstJ   = "abstract"
intJ    = "interface"
extenJ  = "extends"
implH   = "implements"

beginJ  = "{"
endJ    = "}"

# doxygen comment styling
headerC         = "/**\n*\n* @author $a$\n*\n*/"
headerBlankC    = "/**\n*\n*\n*/"

def main():

    # the only arg. is the json file 
    args = sys.argv

    if len(args) <= 1:
        print(versionString+"\n"+helpString)
        raise SystemExit

    if args[1] == '-V':
        print(versionString)
        raise SystemExit
    if args[1] == '-help':
        print(helpString)
        raise SystemExit

    author = ""
    if len(args) == 4 and args[2] == commandAuthor:
        author = args[3]

    try:
        f = open(args[1], 'r')
        javaGen = json.load(f)

        # CODE GENERATION: every key in the json File is a seperate Java class #
        keys = javaGen.keys()
        for c in keys:
            print(">> creating new Java Class: "+c+".java")
            createClass(c, javaGen[c], author)

        f.close()

    except FileNotFoundError:
        print('The given file does not exist!')

def createClass(className, values, author):
    # creating the file
    javaFile = open(className+".java","w+")

    accessModifier      = pubJ
    classIdentifier     = classJ # this can be either an "interface" or a "class"
    abstract            = "" # per default the class is not abstract 
    inheritClass        = ""
    compisitionClass    = ""
    extendsC            = False
    implemntsC          = False
    isInterface         = False

    classComment        = headerBlankC #default class comment

    if "private" in values and values["private"] is True:
        accessModifier = priJ
    if "abstract" in values and values["abstract"] is True:
        abstract = " " + abstJ
    if "interface" in values and values["interface"] is True:
        isInterface = True
        classIdentifier = intJ
    if "extends" in values:
        extendsC = True
        inheritClass = values["extends"]
    if "implements" in values:
        implemntsC = True
        compisitionClass = values["implements"]

    if author != "" :
        classComment = headerC.replace("$a$", author)

    classString = accessModifier + abstract + " " + classIdentifier + " " + className 
    if extendsC is True:
        classString = classString + " " + extenJ + " " + inheritClass
    if implemntsC is True:
        classString = classString + " " + implH + " " + compisitionClass

    ## WRTIE TO GENERATED FILE ##
    javaFile.write(classComment+"\r\n") 
    javaFile.write(classString+"\r\n") 

    javaFile.write(beginJ+"\r\n")  

    # generating attributes
    if "fields" in values:
        for a in values["fields"]:
            createAttribute(javaFile, a)

    # generating methods
    if "methods" in values:
        for m in values["methods"]:
            createMethod(javaFile, m, isInterface)


    # generating setters
    if "fields" in values:
        for a in values["fields"]:
            if "s" in a or "gs" in a:
                createSetter(javaFile, a)
    
     # generating getters
    if "fields" in values:
        for a in values["fields"]:
            if "g" in a or "gs" in a:
                createGetter(javaFile, a)

    javaFile.write(endJ+"\r\n")

    javaFile.close() 


def createAttribute(javaFile, values):
    accessModifier      = priJ # the default is private
    static              = ""
    attributeName       = values["name"]
    attributeType       = values["t"]

    if "public" in values and values["public"] is True:
        accessModifier = pubJ
    if "static" in values and values["static"] is True:
        static = " " + statJ

    attributeString = accessModifier + static + " " + attributeType + " " + attributeName

    javaFile.write("\r\n")
    javaFile.write("\t" + attributeString +";\r\n")

def createMethod(javaFile, values, isInterface):
    accessModifier      = pubJ
    static              = ""
    returnType          = "void"
    params              = "()"
    methodName          = values["name"]
    abstract            = "" # per default the class is not abstract 
    isAbstract          = False
    
    if "private" in values and values["private"] is True:
        accessModifier = priJ
    if "static" in values and values["static"] is True:
        static = " " + statJ
    if "abstract" in values and values["abstract"] is True:
        isAbstract = True
        abstract = " " + abstJ
    if "return" in values:
        returnType = values["return"]
    if "param" in values:
        params = "(" + values["param"] +")"

    methodString = accessModifier + abstract +static + " " + returnType + " " + methodName + params

    javaFile.write("\r\n")
    javaFile.write("\t" + methodString)
    if isInterface is not True and isAbstract is not True:
        javaFile.write("\r\n")
        javaFile.write("\t" + beginJ + "\r\n")
        javaFile.write("\t" + endJ + "\r\n")  
    else:
        javaFile.write(";" + "\r\n")
    
def createGetter(javaFile, values):
    accessModifier      = pubJ
    static              = ""
    attributeName       = values["name"].title()
    attributeType       = values["t"]

    if "static" in values and values["static"] is True:
        static = " " + statJ

    getterString = accessModifier + static + " " + attributeType + " "+  "get"+attributeName+"()"
    returnString = "return" + " " + values["name"]+";"

    javaFile.write("\r\n")
    javaFile.write("\t" +getterString+ beginJ + "\r\n")
    javaFile.write("\t\t" + returnString + "\r\n")
    javaFile.write("\t" + endJ + "\r\n")


def createSetter(javaFile, values):
    accessModifier      = pubJ
    static              = ""
    attributeName       = values["name"].title()
    attributeType       = values["t"]
    returnValue         = "void"

    if "static" in values and values["static"] is True:
        static = " " + statJ

    setterString = accessModifier + static + " " + returnValue + " "+  "set"+attributeName + "(" + attributeType + " " + values["name"] +")"
    setString = "this." + values["name"] + " = "+values["name"] + ";"

    javaFile.write("\r\n")
    javaFile.write("\t" +setterString+ beginJ + "\r\n")
    javaFile.write("\t\t" + setString + "\r\n")
    javaFile.write("\t" + endJ + "\r\n")


if __name__ == "__main__":
    main()