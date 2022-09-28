import sys 
import http.server 
import socketserver
import requests
'''
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
'''

def get_simples(url):
    r = requests.get(url)
    return r


def get_params(url, p):
    r = requests.get(url, params=p)
    return r
    

def post(url, data):
    # body => json, objeto python -> json=
    # params => parametros visiveis NÃO É SEGURO FAZER ISSO -> params=
    # data => qualquer coisa
    r = requests.post(url, json=data)
    return r


url_get = "http://localhost:5000/olamundo"
url_post = "http://localhost:5000/cadastra/usuario"

data = {
    "nome": "roger",
    "email": "roger@roger.com.br",
    "senha": "roger123"
}

response = post(url_post, data)
print(response.url)
print(response.text)
print(response.json())
