# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
host = '5.51.214.63'
port = 999
import socket, sys, threading
from time import sleep
sys.stdout = Unbuffered(sys.stdout)
class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn):
      threading.Thread.__init__(self)
      self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
       while 1:
           message_recu = self.connexion.recv(1024)
           print(message_recu.decode('Utf8'))
           if message_recu =='' or message_recu.upper() == "FIN":
                break
        # Le thread <réception> se termine ici.
        # On force la fermeture du thread <émission> :
       th_E._Thread__stop()
       print("Client arrêté. Connexion interrompue.")
       self.connexion.close()
    
class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
        while 1:
            message_emis = input()
            self.connexion.send(message_emis.encode('Utf8'))

# Programme principal - Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((host, port))
except socket.error:
    print ("La connexion a échoué.")
    sys.exit()    
print ("Connexion établie avec le serveur.")
id = input("entrez votre identifiant : ")
password = input("entrez le mot de passe de la salle : ")
password = "ss:" + password
id = "id:" + id
connexion.send(id.encode('Utf8'))  
connexion.send(password.encode('Utf8'))  
a = 1
b = 1
print("authentification en cours")
sleep(1)
while a != 50:   
     
    print(".", end='')
    a += b
    sleep(0.01) 

print(".")
print("authentification terminée")

# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :
th_E = ThreadEmission(connexion)
th_R = ThreadReception(connexion)
th_E.start()
th_R.start()