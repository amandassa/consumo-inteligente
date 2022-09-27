import sys 
import http.server 
import socketserver 
HandlerClass = http.server.SimpleHTTPRequestHandler 
ServerClass  = http.server.HTTPServer 
Protocol     = "HTTP/1.0"
if sys.argv[1:]: 
    port = int(sys.argv[1]) 
else: 
    port = 8000
server_address = ('127.0.0.1', port) 
HandlerClass.protocol_version = Protocol 
http = ServerClass(server_address, HandlerClass) 
sa = http.socket.getsockname() 
print("Serving HTTP on", sa[0], "port", sa[1], "...") 
http.serve_forever()