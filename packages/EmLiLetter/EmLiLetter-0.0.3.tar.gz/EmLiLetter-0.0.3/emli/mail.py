# import libraries
import smtplib
import os
import re
import pathlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import emli

# function to send email from one mail to another mail
def sendMail(senderEmail, recipientEmail, smtpServer, username, appPassword, subject, title, name, bodyHTML,
             filenames, port):

    # generate greeting for email
    greeting = ""
    # consider all possible situations (male and female)
    if title == emli.manTitle:
        greeting = emli.manGreeting + " " + name + ","
    elif title == emli.womanTitle:
        greeting = emli.womanGreeting + " " + name + ","

    # create full body for letter (HTML version)
    fullBodyHTML = ""
    splitBodyHTML = bodyHTML.split("\n")
    # go through all lines of HTML body
    for line in splitBodyHTML:
        # find out row for beginning of HTML body
        if emli.begHTMLBody in line:
            # add additional greeting for HTML body
            fullBodyHTML = fullBodyHTML + line + "\n"
            fullBodyHTML = fullBodyHTML + "        " + greeting + emli.breakSymbol + "\n"
        else:
            # general case
            fullBodyHTML = fullBodyHTML + line + "\n"

    # debug code
    # print(bodyHTML)
    # print(fullBodyHTML)

    # generate message for mail client
    msg = MIMEMultipart()
    msg['From'] = Header(senderEmail)
    msg['To'] = Header(recipientEmail)
    msg['Subject'] = Header(subject)

    # attach two types of content (plain and HTML) for mail client
    # msg.attach(MIMEText(fullBodyPlain, 'plain', 'utf-8'))
    msg.attach(MIMEText(fullBodyHTML, 'html', 'utf-8'))

    # add attachments in letter
    for pathInput in filenames:
        # handle filename for message
        attName = os.path.basename(pathInput)
        # open file
        fileInput = open(pathInput, 'rb')
        # receive extension of file
        ext = pathlib.Path(pathInput).suffix
        ext = ext[1:]
        # attach file in message
        att = MIMEApplication(fileInput.read(), _subtype=ext)
        # close file
        fileInput.close()
        # attach header in message
        att.add_header('Content-Disposition', 'attachment', filename=attName)
        # do final attachment
        msg.attach(att)

    # create a SMTP connection
    server = smtplib.SMTP(smtpServer, port)
    # configure SMTP connection
    server.ehlo()
    server.starttls()
    server.ehlo()

    # log in to the server
    server.login(username, appPassword)
    # define the recipient's email address
    server.sendmail(senderEmail, recipientEmail, msg.as_string())
    # close the connection
    server.quit()
