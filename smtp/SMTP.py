from socket import *
msg = '\r\n I love computer networks!'
endmsg = '\r\n.\r\n'
# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'relay.unc.edu'
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 25))
recv = clientSocket.recv(1024)
print(recv)

if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')
 
 #Send AUTH command and print server response.
print('Sending AUTH Command')
#AUTH with base64 encoded user name password
clientSocket.send("AUTH PLAIN AG15ZW1haWxAZ21haWwuY29tAG15cGFzc3dvcmQ=\r\n")
recv2 = clientSocket.recv(1024)
print(recv2)
if recv2[:3] != '250':
	print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
print('Sending MAIL FROM Command')
clientSocket.send("MAIL From: ayush159@gmail.com\r\n")
recv2 = clientSocket.recv(1024)
print(recv2)
if recv2[:3] != '250':
	print('250 reply not received from server.')
    
# Send RCPT TO command and print server response.
print('Sending RCPT TO Command')
clientSocket.send("RCPT TO: ayush.sethi159@gmail.com\r\n")
recv2 = clientSocket.recv(1024)
print(recv2)
if recv2[:3] != '250':
	print('250 reply not received from server.')
    
# Send DATA command and print server response.
print('Sending DATA Command')
clientSocket.send("DATA\r\n")
recv2 = clientSocket.recv(1024)
print(recv2)
if recv2[:3] != '250':
	print('250 reply not received from server.')
    
# Send message data.
print('Sending Data')
clientSocket.send("SUBJECT: SMTP Mail Client Test\nSMTP Mail Client Test\n.\n\r\n")
recv2 = clientSocket.recv(1024)
print(recv2)
if recv2[:3] != '250':
	print('250 reply not received from server.')
    
# Message ends with a single period.
# Fill in start
# Fill in end

# Send QUIT command and get server response.
print('Sending QUIT')
clientSocket.send("QUIT\r\n")
recv2 = clientSocket.recv(1024)
print(recv2)
if recv2[:3] != '250':
	print('250 reply not received from server.')
    
print('Mail Sent')
