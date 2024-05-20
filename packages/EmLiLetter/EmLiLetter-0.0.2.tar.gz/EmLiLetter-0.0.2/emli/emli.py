# configure local environment
import sys
import os
# configure system path
sys.path.append(os.getcwd())

# import local libraries
import emli 

# entry point for EmLi package
def main():
    # debug code
    entryFilePath = os.path.dirname(os.path.abspath(__file__))
    # create builder
    builder = emli.createBuilder(os.path.join(entryFilePath, emli.filenameBuilder))
    # create main GUI objects
    mainWindow = emli.receiveObject(builder, emli.nameMainWindow)
    mailButton = emli.receiveObject(builder, emli.nameMailButton)
    # create file chooser objects
    dataFileChooser = emli.receiveObject(builder, emli.nameDataFileChooser)
    # create text entry field objects
    subjectEnrty = emli.receiveObject(builder, emli.nameSubjectEntry)
    # create text field objects
    contTextField = emli.receiveObject(builder, emli.nameContTextField)
    # create file chooser wigget objects
    attachFileChooserWidget = emli.receiveObject(builder, emli.nameAttachFileChooserWidget)
    # create label objects
    errorLabel = emli.receiveObject(builder, emli.nameErrorLabel)
    # create toolbar for text modification
    toolbarTextMod = emli.receiveObject(builder, emli.nameToolbarTextMod)
    # create new tags for text modification
    boldTag, italicTag, underlineTag = emli.createTextTags(contTextField)
    # add new buttons to toolbar object
    boldButton, italicButton, underlineButton = emli.addNewButtonsToToolbar(toolbarTextMod)
    # add handlers to visual objects
    emli.attachDestroyEvent(mainWindow, emli.handleDestroyButton)
    emli.attachClickEvent(mailButton, emli.handleSendMail)
    emli.attachClickEventArg(boldButton, emli.handleBoldButton, boldTag)
    emli.attachClickEventArg(italicButton, emli.handleItalicButton, italicTag)
    emli.attachClickEventArg(underlineButton, emli.handleUnderlineButton, underlineTag)
    # save references to file chooser objects in GUI module
    emli.saveRefToFileChooserObjects(dataFileChooser)
    # save references to text entry objects in GUI module
    emli.saveRefToTextEntryObjects(subjectEnrty)
    # save references to file chooser widget objects in GUI module
    emli.saveRefToFileChooserWidgetObjects(attachFileChooserWidget)
    # save references to label objects in GUI module
    emli.saveRefToLabelObjects(errorLabel)
    # save references to text field objects in GUI module
    emli.saveRefToTexfFieldObjects(contTextField)
    # save references to toolbar objects in GUI module
    emli.saveRefToToolbarObjects(toolbarTextMod)
    # initialize visual objects for GUI
    emli.initializeVisualObjects()
    # launch graphical interface
    emli.launchInterface(mainWindow)

# specify entry point
if __name__ == "__main__":
    main()
