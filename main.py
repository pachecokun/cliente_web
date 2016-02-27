import socket
import math
from _codecs import decode



print("Introduzca la URL: ",end="")

url = input()

"""Validación de protocolo"""
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
"""Obtención de host/puerto"""
if "/" in url:
    host = url.split("/")[0]
    url = "/"+url.split("/")[1]
elif "?" in url:
    host = url.split("?")[0]
    url = "/?"+url.split("?")[1]
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

"""Obtención de parámetros"""
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

"""Entrada de método"""
while True:
    try:
        print("\nIntroduzca el método(1:GET 2:POST 3:OPTIONS): ",end="")
        i = int(input())-1
        break
    except:
        pass

str_par = ""

"""Formación de petición"""
for p in parametros:
    if len(str_par) > 0:
        str_par = str_par+"&"
    str_par = str_par+p[0]+"="+p[1]

if i == 0:
    request = "GET "+recurso
    if len(str_par) > 0:
        request = request+"?"+str_par
    request = request+" HTTP/1.1\nHost: "+host+":"+str(port)+"\n\n"
elif i == 1:
    request = "POST "+recurso+" HTTP/1.1\nHost: "+host+":"+str(port)
    request = request+"\nContent-Type: application/x-www-form-urlencoded\nContent-Length: "+str(len(str_par))+"\n\n"
    request = request+str_par+"\n\n"
else:
    print("NOTA: Options no envía parámetros ni recurso al servidor")
    request = "OPTIONS * HTTP/1.1\nHost: "+host+":"+str(port)+"\n\n"

print("\n----------Petición")
print(request)

"""Conexión a servidor"""
s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((host, port))
except:
    print("Servidor incorrecto no disponible.")
    exit()
    
"""Envío de petición"""
s.send(bytes(request,"UTF-8"))

print("Recibiendo respuesta...")

"""Se recibe respuesta"""
lineas = []
linea = ""
while True:
    try:
        c = str(decode(s.recv(1),"latin-1"))
        s.settimeout(0.3)
        if c == "\n":
            linea = linea.replace("\r", "")
            lineas.insert(len(lineas), linea)
            linea = ""
        else:
            linea = linea +c
    except:
        break
    
"""Se procesa y muestra respuesta"""
print("\n----------Respuesta") 

try:
    print("Versión de http: "+lineas[0].split(" ")[0].replace("HTTP/",""))
    print("Código de respuesta: "+lineas[0].split(" ")[1])
    print("Mensaje de respuesta: "+lineas[0].split(" ",2)[2])
    
    print("\n--Headers de respuesta:")
    
    s = 0
    i = 1
    b = 1
    nb = 0
    
    for l in lineas[1:]:
        if s==0:
            if len(l) == 0:
                s = 1
            else:
                s = 0
                print(l)
            i = i+1
        elif s==1:
            s = 3
            nb = math.ceil((len(lineas)-i)/20)
            print("\n--Presione enter para mostrar el contenido de la página")
            input()
            print("\n--Cuerpo de respuesta:")
        else:
            print(l)
            if(i==20): #se divide contenido en bloques de 20 lineas
                i = 0
                print("\n--Presione enter para visualizar el siguiente bloque de la pagina ["+str(b)+"/"+str(nb)+"]")
                b = b+1
                input()
                
            i = i+1
            
    print("------Fin de programa")
            
except:
    print("Respuesta inválida")