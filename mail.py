import telnetlib
import datetime
import sys
#PingMonitor Telnet Mail Sender.
#author rgonzalez, etinajero. Sep 2009

HOST = "mail.pvlider.com"
PORT = "25"
ip = sys.argv[1]
msg = """Solo para comunicarle que la direccion ip %s no responde desde el %s de %s del %s.

Atte.
PingMonitor
\r\n.\r\n
"""
today = datetime.date.today()
day = today.strftime('%d')
month = today.strftime('%h')
year = today.strftime('%Y')

tn = telnetlib.Telnet(HOST,PORT)
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
