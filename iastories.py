#!/usr/bin/python3

import os
import xml.etree.ElementTree

NAME = "Interactive Stories CLI"
AUTHOR = "LNJ"
VERSION = "0.1.1"
YEAR = "2016"

print( "{} v{} by {}, {}".format(NAME, VERSION, AUTHOR, YEAR) )

def Load():
    # file name (in data folder)
    FileName = "story_signal_from_mars.ias"
    # full file path
    FullPath = os.path.abspath(os.path.join("data", FileName))
    # loaded xml file
    global XMLFile
    XMLFile = xml.etree.ElementTree.parse(FullPath)
    
    print (XMLFile.find("story/title").text, "in", XMLFile.find("story/lang").text)

def Start(again):
    if again == True:
        Question = "\nDo you want to start again? [Y/n]: "
    else:
        Question = "Do you want to start? [Y/n]: "
    
    if input (Question) == "n":
        print ("okay... bye")
        exit()

def DisplayPage(PageNum):
    StoryName = XMLFile.find("story/title").text
    
    # the path of the page
    Path = "story/page[@id='{}']/{}"

    # the text of the page
    Text = XMLFile.find(Path.format(PageNum, "text")).text
    
    # the number of options
    NumOfOptions = int( XMLFile.find(Path.format(PageNum, "options")).text )

    print("––––––––––––––––––––––––––––––––––––––––")
    print(Text)
    print("")

    # Check if there are no options / this is the end of the story
    if NumOfOptions == 0:
        print("THE END!")
        print("This was the Story: {}".format(StoryName))
        Start(True)
    else:
        print("Your Options: ")

        PrintOptions = True
        CurOpt = int(1)
        MaxOpt = NumOfOptions

        while PrintOptions:
            # get and print the text of the option
            OptionText = XMLFile.find("story/page[@id='{}']/option[@id='{}']".format(PageNum, CurOpt)).text
            print (OptionText)

            # if this was the last option to print: get the answer and break
            if CurOpt >= MaxOpt:
                PrintOptions = False
                Answer = AskNextPage(MaxOpt)
                NextPage = XMLFile.find("story/page[@id='{}']/option[@id='{}']".format(PageNum, Answer)).get("topage")
                DisplayPage(NextPage)
                break
            else:
                CurOpt += 1


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
        print("Please enter a number from 1 to {}!".format(MaxID))
        Answer = AskNextPage(MaxID)
        return Answer

Load()
Start(False)
DisplayPage("1")
