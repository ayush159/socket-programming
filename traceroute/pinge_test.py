import socket
import os
import sys
import struct
import time
import select
#import binascii

ICMP_ECHO_REQUEST = 8

def checksum(source_string):
    
    x = (int(len(source_string)/2))*2
    sum = 0
    count = 0
 
    # Handle bytes in pairs (decoding as short ints)
    low = 0
    high = 0
    while count < x:
        if (sys.byteorder == "little"):
            low = source_string[count]
            high = source_string[count + 1]
        else:
            low = source_string[count + 1]
            high = source_string[count]
        sum = sum + (high * 256 + low)
        count += 2
 
    # Handle last byte if applicable (odd-number of bytes)
    # Endianness should be irrelevant in this case
    if x < len(source_string): # Check for odd length
        low = source_string[len(source_string)-1]
        sum += low
 
    sum &= 0xffffffff # Truncate sum to 32 bits (a variance from ping.c, which
                      # uses signed ints, but overflow is unlikely in ping)
 
    sum = (sum >> 16) + (sum & 0xffff)    # Add high 16 bits to low 16 bits
    sum += (sum >> 16)                    # Add carry from above (if any)
    answer = ~sum & 0xffff              # Invert and truncate to 16 bits
    answer = socket.htons(answer)
    return answer


def receiveOnePing(my_socket, ID, timeout):
    """
    receive the ping from the socket.
    """
    timeLeft = timeout
    while True:
        startedSelect = time.time()
        whatReady = select.select([my_socket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = my_socket.recvfrom(1024)
        
        #Fill in start
        icmp_header = recPacket[20:28]
        #Fetch the ICMP header from the IP packet
        type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmp_header)
        
        if type != 8 and packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent
        
        #Fill in end

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return
        

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
        #Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = socket.htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    #Both LISTS and TUPLES consist of a number of objects
    #which can be referenced by their position number within the object

def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname("icmp")
    #SOCK_RAW is a powerful socket type. For more details see: http://sock-raw.org/papers/sock_raw
    #Fill in start
    #Create Socket here
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    #Fill in end
    myID = os.getpid() & 0xFFFF #Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    #delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    delay = receiveOnePing(mySocket, myID, timeout)

    mySocket.close()
    return delay

def ping(host, timeout=1):
#timeout=1 means: If one second goes by without a reply from the server,
#the client assumes that either the client’s ping or the server’s pong is lost
    dest = socket.gethostbyname(host)
    print ("Pinging " + dest + "("+host+") using Python:")
    print ("")
    #Send ping requests to a server separated by approximately one second
    c = 5
    while c>0 :
        delay = doOnePing(dest, timeout)
        print (delay)
        time.sleep(1)# one second
        c -= 1
    return delay
print("\n1. Hosted in North America")
ping("www.amazon.com")
print("\n2. Hosted in China")
ping("www.baidu.com")
print("\n3. Hosted in Europe")
ping("www.ox.ac.uk")
print("\n4. Hosted in South America")
ping("www.brasil.gov.br")
