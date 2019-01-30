# Web-server

##  A web server that handles one HTTP request at a time.
This web server accepts and parse the HTTP request, get the requested file from the server’s file system, create an HTTP response
message consisting of the requested file preceded by header lines, and then send the response directly to
the client. If the requested file is not present in the server, the server sends an HTTP “404 Not
Found” message back to the client.
