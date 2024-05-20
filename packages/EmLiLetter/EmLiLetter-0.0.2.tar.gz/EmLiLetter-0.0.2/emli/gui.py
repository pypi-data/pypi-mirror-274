# import libraries
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GLib
import emli

# variable for text entry objects
subjectEnrty = None
# variable for file chooser objects
dataFileChooser = None
# variable for file chooser widget object
attachFileChooserWidget = None
# variable for text field object
contTextField = None
# variable for label objects
errorLabel = None
# variable for toolbar object (text modification)
toolbarTextMod = None

# function to handle signal of mail sending
def handleSendMail(self):

    # initialization
    errorLabel.set_text(emli.emptyRow)
    # read configuration constants from special module
    senderEmail = emli.senderEmail
    smtpServer = emli.smtpServer
    username = emli.username
    appPassword = emli.appPassword

    # read filenames of different files
    filenameTable = dataFileChooser.get_filename()
    filenamesAttach = attachFileChooserWidget.get_filenames()

    # read HTML body for letter from text field
    textBuffer = contTextField.get_buffer()
    startIter = textBuffer.get_start_iter()
    endIter = textBuffer.get_end_iter()
    formatBuf = textBuffer.register_serialize_tagset()
    exported = textBuffer.serialize(textBuffer, formatBuf, startIter, endIter)
    pangoConverter = emli.PangoToHtml()
    bodyHTML = pangoConverter.feed(exported)
    # modify body HTML text
    bodyHTML = emli.addHeadersHTML(bodyHTML)
    # read subject from special text entry object
    subject = subjectEnrty.get_text()

    # debug code
    # print(bodyHTML)
    # print(subject)

    # read data from table file (CSV)
    try:
        titles, names, recipientEmails = emli.readTableFromCSVFile(filenameTable)
    except Exception as error:
        # handle exception situation
        errorLabel.set_text(str(error))
        # finish working
        return

    # go through all mail boxes
    index = 0
    numMails = len(recipientEmails)
    while index < numMails:
        # extract data from arrays
        recipientEmail = recipientEmails[index]
        name = names[index]
        title = titles[index]
        try:
            # send one mail to end user seperatly
            emli.sendMail(senderEmail, recipientEmail, smtpServer, username, appPassword, subject, title, name, bodyHTML, filenamesAttach, alltypes.smtpPort)
        except Exception as error:
            # handle exception situation
            errorLabel.set_text(str(error))
            # finish working
            return
        # go to the next mail box
        index = index + 1

# function to handle signal of destruction
def handleDestroyButton(self):
    Gtk.main_quit()

# function to handle signal for bold button
def handleBoldButton(self, tag):
    applyTagToTextView(tag)

# function to handle signal for italic button
def handleItalicButton(self, tag):
    applyTagToTextView(tag)

# function to handle signal for underline button
def handleUnderlineButton(self, tag):
    applyTagToTextView(tag)

# function to apply tag to text view object
def applyTagToTextView(tag):

    # get the text buffer from view object
    textBuffer = contTextField.get_buffer()
    # define boundaries of text
    bounds = textBuffer.get_selection_bounds()
    if len(bounds) != 0:
        # apply new tag for text
        start, end = bounds
        textBuffer.apply_tag(tag, start, end)


# function to create builder for GUI app
def createBuilder(filenameBuilder):
    # create builder
    builder = Gtk.Builder()
    builder.add_from_file(filenameBuilder)
    # return builder
    return builder

# function to create tags for text modification
def createTextTags(textField):

    # receive text buffer from text field
    textBuffer = textField.get_buffer()
    # create tags using found buffer
    boldTag = textBuffer.create_tag("bold", weight=Pango.Weight.BOLD)
    italicTag = textBuffer.create_tag("italic", style=Pango.Style.ITALIC)
    underlineTag = textBuffer.create_tag("underline", underline=Pango.Underline.SINGLE)
    # return tags
    return boldTag, italicTag, underlineTag


# function to receive GUI object from builder
def receiveObject(builder, nameObject):
    # find out object
    visObject = builder.get_object(nameObject)
    # return object
    return visObject

# function to create new buttons for toolbar of modification of text
def addNewButtonsToToolbar(toolbarObject):

    # create three buttons (different text styles)
    boldButton = Gtk.ToolButton(Gtk.STOCK_BOLD)
    italicButton = Gtk.ToolButton(Gtk.STOCK_ITALIC)
    underlineButton = Gtk.ToolButton(Gtk.STOCK_UNDERLINE)
    # insert buttons into toolbar object
    toolbarObject.insert(boldButton, 0)
    toolbarObject.insert(italicButton, 1)
    toolbarObject.insert(underlineButton, 2)
    # return create buttons
    return boldButton, italicButton, underlineButton

# function to attach function to click event of visual object
def attachClickEvent(visObject, handlerFunc):
    # attach function to visual object
    visObject.connect("clicked", handlerFunc)

# function to attach function to click event of visual object with one argument
def attachClickEventArg(visObject, handlerFunc, argument):
    # attach function to visual object
    visObject.connect("clicked", handlerFunc, argument)

# function to attach function to destroy event of visual object
def attachDestroyEvent(visObject, handlerFunc):
    # attach function to visual object
    visObject.connect("destroy", handlerFunc)

# function to save references to file chooser objects
def saveRefToFileChooserObjects(ref1):
    # specify global variables
    global dataFileChooser
    # save references in special variables
    dataFileChooser = ref1

# function to save references to file chooser widget objects
def saveRefToFileChooserWidgetObjects(ref1):
    # specify global variables
    global attachFileChooserWidget
    # save references in special variables
    attachFileChooserWidget = ref1

# function to save references to text entry objects
def saveRefToTextEntryObjects(ref1):
    # specify global variables
    global subjectEnrty
    # save references in special variables
    subjectEnrty = ref1

# function to save references to text field objects
def saveRefToTexfFieldObjects(ref1):
    # specify global variables
    global contTextField
    # save references in special variables
    contTextField = ref1

# function to save references to label objects
def saveRefToLabelObjects(ref1):
    # specify global variables
    global errorLabel
    # save references in special variables
    errorLabel = ref1

# function to save references to label objects
def saveRefToToolbarObjects(ref1):
    # specify global variables
    global toolbarTextMod
    # save references in special variables
    toolbarTextMod = ref1

# function to initialize properties of visual objects
def initializeVisualObjects():
    # empty row for error label
    errorLabel.set_text(emli.emptyRow)
    # "convenient" text for letter content
    textBuffer = contTextField.get_buffer()
    textBuffer.set_text("")
    contTextField.set_wrap_mode(Gtk.WrapMode.WORD)

# function to launch graphical user interface (GTK+)
def launchInterface(window):
    # launch interface
    window.show_all()
    Gtk.main()
