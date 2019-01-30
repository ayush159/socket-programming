#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)


#Prepare a sever socket
serverPort = 8080
serverIP = '0.0.0.0'
serverAddress = (serverIP,serverPort)
serverSocket.bind(serverAddress)    
serverSocket.listen(5)

while True:
#Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        print('client IP:%s client port:%s'%(addr[0],addr[1]))
        message = connectionSocket.recv(2048)
        filename = message.split()[1]
        f = open(filename[1:],'r')
        #print(filename)
        outputdata = f.read()
        f.close()
        #Send one HTTP header line into socket
        connectionSocket.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.close()

    except IOError:
        #Send response message for file not found
        connectionSocket.send(b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n <html><body> <p>File Not Found</p></body><html>')
        #Close client socket
        connectionSocket.close()


serverSocket.close()
