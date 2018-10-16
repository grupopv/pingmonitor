#!/usr/bin/python3

#PingMonitor Telnet Mail Sender.
#authors rgonzalez, cetinajero. Sep 2009

import telnetlib
import datetime
import sys
import sendgrid
from sendgrid.helpers.mail import *
from yaml import load

# Define variables
host = "mail.pvlider.com"
port = "25"
msg = """Solo para comunicarle que la direccion ip %s no responde desde el %s de %s del %s.

Atte.
PingMonitor
\r\n.\r\n
"""

today = datetime.datetime.today()
day = today.strftime('%d')
month = today.strftime('%h')
year = today.strftime('%Y')
time = today.strftime('%l:%M %p')

def read_config():
    with open('config.yml', 'r') as f:
        doc = load(f)
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
    sg = sendgrid.SendGridAPIClient(config["apikey"])
    from_email = Email(config["from"])
    to_email = Email(config["to"])
    subject = config["subject"][type] % (name)
    content = Content("text/html",config["html-content"][type] % (name, value, time, day, month, year))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print("Sending mail...")
