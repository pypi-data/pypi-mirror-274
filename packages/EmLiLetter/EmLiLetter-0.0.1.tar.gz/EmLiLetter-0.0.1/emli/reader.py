# import libraries
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GLib
import re
import csv
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple
from xml.etree.ElementTree import fromstring
import emli

# function to read configuration file from file
def readConfigurationFile(filenameConf):

    # find out number of lines in file
    fileConf = open(filenameConf, "r")
    numLines = len(fileConf.readlines())
    fileConf.close()
    # open file for reading
    fileConf = open(filenameConf, "r")

    # verify number of lines in file
    if numLines < 4:
        # throw exceptional situation
        raise IndexError("File is too small for app configuration!")

    # read configuration data from file
    senderMail = re.sub("\n", "", fileConf.readline())
    smtpServer = re.sub("\n", "", fileConf.readline())
    username = re.sub("\n", "", fileConf.readline())
    appPassword = re.sub("\n", "", fileConf.readline())

    # check correctness of email address
    if not alltypes.isValidEmail(senderMail):
        # throw exceptional situation
        raise ValueError("Sender mail in file is incorrect!")
    # check correctness of domain address
    if not alltypes.isValidDomain(smtpServer):
        # throw exceptional situation
        raise ValueError("Sender mail in file is incorrect!")

    # close file
    fileConf.close()
    # return configuration data
    return senderMail, smtpServer, username, appPassword

# function to read emails from file
def readEmailsFromTextFile(filenameEmail):

    # initialization
    emails = []
    # open file
    fileEmail = open(filenameEmail, "r")

    # go through all lines of file
    for line in fileEmail.readlines():
        # delete extra symbol in line
        line = re.sub("\n", "", line)
        # check correctness of email address
        if alltypes.isValidEmail(line):
            emails.append(line)
        else:
            # throw exceptional situation
            raise ValueError("Recepeint email in file is incorrect!")

    # close file
    fileEmail.close()
    # return array of emails
    return emails

# function to read table from CSV file
def readTableFromCSVFile(filenameTable):

    # initialization
    titles = []
    names = []
    emails = []
    index = 1
    # open file
    fileTable = open(filenameTable, "r")

    # create reader using file object
    reader = csv.reader(fileTable)
    # go through all rows of table
    for row in reader:
        # the first row will be ignored
        if index != 1:
            # add data in special arrays
            titles.append(row[0])
            names.append(row[1] + " " + row[2])
            emails.append(row[3])
        # add index to variable
        index = index + 1

    # return array of emails
    return titles, names, emails

# function to read subject and body from file
def readSubjectAndBodyFromFile(filenameContent):

    # find out number of lines in file
    fileCont = open(filenameContent, "r")
    numLines = len(fileCont.readlines())
    fileCont.close()

    # verify number of lines in file
    if numLines < 2:
        # throw exceptional situation
        raise IndexError("File is too small for email content!")

    # initialization
    subject = ""
    bodyPlain = ""
    i = 1
    ind = False
    # open file (plain version)
    fileCont = open(filenameContent, "r")

    # go through all lines of file
    for line in fileCont.readlines():
        # delete extra symbol in line
        line = re.sub("\n", "", line)
        # consider different situations
        if i == 1:
            # subject situation
            subject = line
        else:
            # find out delimeter row
            if line == alltypes.delimeterTypeContent:
                ind = True
            # body situation (plain text)
            if ind == False:
                bodyPlain = bodyPlain + line + "\n"
        i = i + 1


    # close file
    fileCont.close()
    # open file again
    fileCont = open(filenameContent, "r")
    # initialization (HTML version)
    ind = False
    bodyHTML = ""

    # go through all lines of file
    for line in fileCont.readlines():
        # delete extra symbol in line
        line = re.sub("\n", "", line)
        # find out delimeter row
        if line == alltypes.delimeterTypeContent:
            # change value of indicator
            ind = True
            # go to the next row
            continue
        # body situation (HTML text)
        if ind == True:
            bodyHTML = bodyHTML + line + "\n"

    # close file
    fileCont.close()

    # return subject and body
    return subject, bodyPlain, bodyHTML


# function to read subject and body from file
def readFilenamesFromFile(filename):

    # initialization
    filenames = []
    # open file
    fileInput = open(filename, "r")

    # go through all lines of file
    for line in fileInput.readlines():
        # delete extra symbol in line
        line = re.sub("\n", "", line)
        # check correctness of file
        if alltypes.isValidFile(line):
            # add line in special array
            filenames.append(line)
        else:
            # throw exceptional situation
            raise ValueError("Filename for attachment is not correct!")

    # close file
    fileInput.close()
    # return filenames that were read
    return filenames

# class to convert Pango to HTML code
class PangoToHtml(HTMLParser):
    """Decode a subset of Pango markup and serialize it as HTML.

    Only the Pango markup used within Gourmet is handled, although expanding it
    is not difficult.

    Due to the way that Pango attributes work, the HTML is not necessarily the
    simplest. For example italic tags may be closed early and reopened if other
    attributes, eg. bold, are inserted mid-way:

        <i> italic text </i><i><u>and underlined</u></i>

    This means that the HTML resulting from the conversion by this object may
    differ from the original that was fed to the caller.
    """
    def __init__(self):
        super().__init__()
        self.markup_text:           str  = ""  # the resulting content
        self.current_opening_tags:  str  = ""  # used during parsing
        self.current_closing_tags:  List = []  # used during parsing

        # the key is the Pango id of a tag, and the value is a tuple of opening
        # and closing html tags for this id.
        self.tags: Dict[str: Tuple[str, str]] = {}

    tag2html: Dict[str, Tuple[str, str]] = {
                                            Pango.Style.ITALIC.value_name:      ("<i>", "</i>"),  # Pango doesn't do <em>
                                            str(Pango.Weight.BOLD.real):        ("<b>", "</b>"),
                                            Pango.Underline.SINGLE.value_name:  ("<u>", "</u>"),
                                            "foreground-gdk":                   (r'<span foreground="{}">', "</span>"),
                                            "background-gdk":                   (r'<span background="{}">', "</span>")
                                            }

    def feed(self, data: bytes) -> str:
        """Convert a buffer (text and and the buffer's iterators to html string.

        Unlike an HTMLParser, the whole string must be passed at once, chunks
        are not supported.
        """
        # Remove the Pango header: it contains a length mark, which we don't
        # care about, but which does not necessarily decodes as valid char.
        header_end  = data.find(b"<text_view_markup>")
        data        = data[header_end:].decode()

        # get the tags
        tags_begin  = data.index("<tags>")
        tags_end    = data.index("</tags>") + len("</tags>")
        tags        = data[tags_begin:tags_end]
        data        = data[tags_end:]

        # get the textual content
        text_begin  = data.index("<text>")
        text_end    = data.index("</text>") + len("</text>")
        text        = data[text_begin:text_end]

        # convert the tags to html.
        # we know that only a subset of HTML is handled in Gourmet:
        # italics, bold, underlined and normal

        root            = fromstring(tags)
        tags_name       = list(root.iter('tag'))
        tags_attributes = list(root.iter('attr'))
        tags            = [ [tag_name, tag_attribute] for tag_name, tag_attribute in zip(tags_name, tags_attributes)]

        tags_list = {}
        for tag in tags:
            opening_tags = ""
            closing_tags = ""

            tag_name    = tag[0].attrib['name']
            vtype       = tag[1].attrib['type']
            value       = tag[1].attrib['value']
            name        = tag[1].attrib['name']

            if vtype == "GdkColor":  # convert colours to html
                if name in ['foreground-gdk', 'background-gdk']:
                    opening, closing = self.tag2html[name]
                    hex_color = f'{value.replace(":","")}' # hex color already handled by gtk.gdk.color.to_string() method
                    opening = opening.format(hex_color)
                else:
                    continue  # no idea!
            else:
                opening, closing = self.tag2html[value]

            opening_tags += opening
            closing_tags = closing + closing_tags   # closing tags are FILO

            tags_list[tag_name] = opening_tags, closing_tags

            if opening_tags:
                tags_list[tag_name] = opening_tags, closing_tags

        self.tags = tags_list

        # create a single output string that will be sequentially appended to
        # during feeding of text. It can then be returned once we've parse all
        self.markup_text                = ""
        self.current_opening_tags       = ""
        self.current_closing_tags       = []  # Closing tags are FILO

        super().feed(text)

        return self.markup_text

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
        # the pango tags are either "apply_tag", or "text"
        # we only really care about the "apply_tag"
        # there could be an assert, but we let the parser quietly handle nonsense.
        if tag == "apply_tag":
            attrs       = dict(attrs)
            tag_name    = attrs.get('name')
            tags        = self.tags.get(tag_name)

            if tags is not None:
                (self.current_opening_tags, closing_tag) = tags
                self.current_closing_tags.append(closing_tag)

    def handle_data(self, data: str) -> None:
        data = self.current_opening_tags + data
        self.markup_text += data

    def handle_endtag(self, tag: str) -> None:
        if self.current_closing_tags:  # Can be empty due to closing "text" tag
            self.markup_text += self.current_closing_tags.pop()
        self.current_opening_tags = ""
