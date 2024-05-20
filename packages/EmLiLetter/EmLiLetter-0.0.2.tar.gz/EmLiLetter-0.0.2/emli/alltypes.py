# import library
from urllib.parse import urlparse
import re
import os

### Constant section

## define numeric constants
smtpPort = 587 # port for SMTP protocol

## define SMTP configuration constants
senderEmail = "tomilo.art.forscience@gmail.com"
smtpServer = "smtp.gmail.com"
username = "tomilo.art.forscience@gmail.com"
appPassword = "epbk ardc hgky mnwa"

## define visual interface string constants
filenameBuilder = "emli.glade" # filename for builder file of GTK GUI
nameMainWindow = "mainWindow" # name of main window in graphical user interface
nameMailButton = "mailButton" # name of button in graphical user interface
nameConfFileChooser = "confFileChooser" # name of chooser for configuration file
nameDataFileChooser = "dataFileChooser" # name of chooser for data file
nameContTextField = "contTextField" # name of special text field for
nameAttachFileChooserWidget = "attachFileChooserWidget" # name of chooser widget for attachments of letter
nameSubjectEntry = "subjectEntry" # name of entry field for letter subject
nameErrorLabel = "errorLabel" # name of error label in GUI
nameToolbarTextMod = "toolbarTextMod" # name of toolbar object for text modification
nameBoldText = "bold" # name of bold text in GTK library
nameItalicText = "italic" # name of italic text in GTK library
nameUnderlineText = "underline" # name of underline text in GTK library

## define email content string constants

manTitle = "Herr" # title for men in greeting
womanTitle = "Frau" # title for women in greeting
manGreeting = "Sehr geehrter" # greeting for men in letter
womanGreeting = "Sehr geehrte" # greeting for women in letter
begHTMLBody = "<p>" # indicator row for beginning of HTML body
breakSymbol = "<br>" # indicator of break symbol in HTML file
delimeterTypeContent = "************" # split the content into two parts (plain and HTML)

## define initial and final letter texts for sending mails

initialLetterText = """<html>
  <body>
    <p>"""
finalLetterText = """    </p>
  </body>
</html>"""


## define general string constants

emptyRow = "" # constant for empty row

# define constants for regular expression
regexMail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
regexDomain = "[a-zA-Z0-9]+(\.[a-zA-Z]{2,})+$"

## Function section

# function to verify whether string variable contains correct email address
def isValidEmail(addr):
    # check correctness of email address
    if (re.fullmatch(regexMail, addr)):
        return True
    else:
        return False

# function to verify whether string variable contains correct domain address
def isValidDomain(addr):
    # check correctness of domain address
    if (re.match(regexDomain, addr)):
        return True
    else:
        return False

# function to verify correctness of path in file system
def isValidFile(path):
    # check correctness of path
    if os.path.isfile(path):
        return True
    else:
        return False

# function to add headers of HTML text for SMTP protocol
def addHeadersHTML(textHTML):
    # add special headers in text
    modTextHTML = initialLetterText + "\n" + textHTML + "\n" + finalLetterText
    # return modified HTML text
    return modTextHTML
