#!/usr/bin/env python3.5
#Tpix is a python email tracking pixel
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from lxml import etree
from pytracking.html import adapt_html
from pytracking.webhook import send_webhook
import smtplib
import pytracking
import lxml

emailHost = "smtp.gmail.com"#Change to SMTP server IP or hostname
emailPort = 587 #Change to port smtp is on
msg = MIMEMultipart('alternative')
uName = input("Enter your email: ")
passWord = getpass("Password: ")
msg['To'] = input("Enter email recipient: ")
msg['Subject'] = input("Enter email subject: ")
msg['From'] = uName
emailCont = []
print("Enter email content: ")

configuration = pytracking.Configuration(
   # base_open_tracking_url="https://webhook.site/",
   # webhook_url="https://webhook.site/642696b3-0386-46ed-80fe-5e3604c970d8",
    base_open_tracking_url="http://mehltrej.pythonanywhere.com/",
    webhook_url="http://mehltrej.pythonanywhere.com/trust/",
    include_webhook_url=True)

(pixel, mime) = pytracking.get_open_tracking_pixel()
webhook = '<img src="' + configuration.webhook_url + '" alt="">'
print(webhook)
while True:
    line = input()
    if line:
        emailCont.append(line)
    else:
        break
htmlBody = ""
for line in emailCont:
    htmlBody = htmlBody + "<p>" + line + "</p> "
htmlBody = htmlBody + webhook

root = etree.HTML(htmlBody)
htmlText = etree.tostring(root)
pytrackHtml = adapt_html(htmlText, extra_metadata={"customer_id": 1},
    click_tracking=True, open_tracking=True)
emailBod = MIMEText(pytrackHtml, 'html')
open_tracking_url = pytracking.get_open_tracking_url(
    {"customer_id": 1}, configuration=configuration)
tracking_result = pytracking.get_open_tracking_result(
    open_tracking_url, base_open_tracking_url="http://mehltrej.pythonanywhere.com/")
msg.attach(emailBod)

#Send email

try:
    print("Attempting to connect")
    smtpObj = smtplib.SMTP(emailHost, emailPort)
    print("Successful connection")
    print("Attemping to connect to email")
    try:
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(uName, passWord)
        print("Successful connection")
    except smtplib.SMTPAuthenticationError:
        print("Incorrect Password or Email")
    print("Attempting to send email")
    smtpObj.sendmail(uName, msg['To'], msg.as_string())
    print("Sent successful.")
except smtplib.SMTPException:
    print("Error. Could not send email")

print(tracking_result.metadata)
