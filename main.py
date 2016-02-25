import socket
from _codecs import decode

print("Introduzca la URL: ",end="")

url = input()

if "://" in url and url.index("://")>0:
    protocolo = url.split("://")[0]
    print("protocolo: "+protocolo)
    url = url.split("://")[1]
else:
    print("No se encontró protocolo")
    exit()

if protocolo != "http":
    print("Sólo se acepta protocolo http")
    exit()

if "/" in url:
    host = url.split("/")[0]
    url = "/"+url.split("/")[1]
else:
    host = url
    url = ""

port = 80

if ":" in host:
    try:
        port = int(host.split(":")[1])
        host =  host.split(":")[0]
    except:
        print("Puerto inválido")
        exit()

print("Host: "+host+" , puerto:",port)

recurso = "/"
parametros = []

if len(url)>0:
    if "?" in url:
        recurso = url.split("?")[0]
                
        for par in url.split("?")[1].split("&"):
            if "=" in par:
                parametros.insert(len(parametros), par.split("="))
            else:
                print("Parametros incorrectos")
                exit()
        
    else:
        recurso = url

print("Recurso: "+recurso)
print("Parámetros: "+str(parametros))

while True:
    try:
        print("\nIntroduzca el método(1:GET 2:POST 3:OPTIONS): ",end="")
        i = int(input())
        break
    except:
        pass

metodo = ("GET","POST","OPTIONS")[i]

request = metodo+" "+recurso+" HTTP/1.1\n\nhost: "+host+":"+str(port)+"\n"

print("----------Petición")
print(request)


s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))

s.send(bytes(request,"UTF-8"))

print("----------Respuesta")

print(str(decode(s.recv(100000),"utf-8")))