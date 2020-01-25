#!/usr/bin/python3

# pingmonitor mail sender library
# authors rgonzalez, cetinajero. Sep 2009

import telnetlib
import datetime
import sys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from yaml import safe_load

# Define variables
today = datetime.datetime.today()
day = today.strftime('%d')
month = today.strftime('%h')
year = today.strftime('%Y')
time = today.strftime('%l:%M %p')

def read_config():
    with open('config.yml', 'r') as f:
        doc = safe_load(f)
    return doc

def telnet_mail(name, ip):
    tn = telnetlib.Telnet(host, port)
    tn.read_until("Postfix")
    tn.write("ehlo pvlider.com\n")
    tn.read_until("DSN")
    tn.write("mail from:PingMonitor@pvlider.com\n")
    tn.read_until("Ok")
    tn.write("rcpt to:sistemas@pvlider.com\n")
    tn.read_until("Ok")
    tn.write("data\n")
    tn.read_until(".<CR><LF>")
    tn.write("subject:Fallo de Conexion con IP %s.\n\n" % ip)
    tn.write(msg % (ip,day,month,year))
    tn.read_until("queued as XXXXXX",1)
    tn.write("quit\n")

def sendgrid_mail(type, name, value):
    config = read_config()
    subject = config["subject"][type] % (name)

    message = Mail(
        from_email = config["from"],
        to_emails = config["to"],
        subject = subject,
        html_content = config["html-content"][type] % (name, value, time, day, month, year)
    )

    sg = SendGridAPIClient(config["apikey"])
    response = sg.send(message)
    print("[INFO]", "Sending mail:", subject)
