#!/usr/bin/python3

import os
import xml.etree.ElementTree

NAME = "Interactive Stories CLI"
AUTHOR = "LNJ"
VERSION = "0.1.0"
YEAR = "2016"

print( "{} v{} by {}, {}".format(NAME, VERSION, AUTHOR, YEAR) )

def Load():
    # file name (in data folder)
    FileName = "story_signal_from_mars.de_DE.ias"
    # full file path
    FullPath = os.path.abspath(os.path.join("data", FileName))
    # loaded xml file
    global XMLFile
    XMLFile = xml.etree.ElementTree.parse(FullPath)
    
    print (XMLFile.find("story/title").text, "in", XMLFile.find("story/lang").text)

def Start():
    if input ("Do you want to start? [Y/n]: ") == "n":
        print ("okay... bye")
        exit()

def DisplayPage(PageNum):
    # the path of the page
    Path = "story/page[@id='{}']/{}"
    
    # the text of the page
    Text = XMLFile.find(Path.format(PageNum, "text")).text
    
    # the number of options
    NumOfOptions = int( XMLFile.find(Path.format(PageNum, "options")).text )
    
    print("––––––––––––––––––––––––––––––––––––––––")
    print(Text)
    print("\nYour Options: ")

    PrintingOptions = True
    CurID = int(1)
    MaxID = NumOfOptions
    while PrintingOptions:
        OptionText = XMLFile.find("story/page[@id='{}']/option[@id='{}']".format(PageNum, CurID)).text
        print (OptionText)
        if CurID >= MaxID:
            PrintingOptions = False
            break
        else:
            CurID += 1
    
    Answer = AskNextPage(MaxID)

    
    NextPage = XMLFile.find("story/page[@id='{}']/option[@id='{}']".format(PageNum, Answer)).get("topage")
    DisplayPage(NextPage)

def AskNextPage(MaxID):
    Answer = input("What do you want to do? [{}-{}]: ".format(1, MaxID))
    try:
        Answer = int(Answer)
    except:
        print("Please enter a number from 1 to {}!".format(MaxID))
        Answer = AskNextPage(MaxID)
    if Answer <= MaxID and Answer >= 1:
        return Answer
    else:
        Answer = AskNextPage(MaxID)
        return Answer

Load()
Start()
DisplayPage("1")
