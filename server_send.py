# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connexions clientes en parallèle.
 
HOST = '192.168.1.39'
PORT = 999

p1 ="""

 .----------------. 
| .--------------. |
| |   ______     | |
| |  |_   __ \   | |
| |    | |__) |  | |
| |    |  ___/   | |
| |   _| |_      | |
| |  |_____|     | |
| |              | |
| '--------------' |
 '----------------' 

"""
k1 = """

 .----------------. 
| .--------------. |
| |  ___  ____   | |
| | |_  ||_  _|  | |
| |   | |_/ /    | |
| |   |  __'.    | |
| |  _| |  \ \_  | |
| | |____||____| | |
| |              | |
| '--------------' |
 '----------------' 

"""
d1 = """
 .----------------. 
| .--------------. |
| |  ________    | |
| | |_   ___ `.  | |
| |   | |   `. \ | |
| |   | |    | | | |
| |  _| |___.' / | |
| | |________.'  | |
| |              | |
| '--------------' |
 '----------------' 
"""

import socket, sys, threading
from time import sleep
class ThreadClient(threading.Thread):
  '''dérivation d'un objet thread pour gérer la connexion avec un client'''
  Mode = False 
  def __init__(self, conn):
      threading.Thread.__init__(self)
      self.connexion = conn

  def run(self):
      a = 0     
      nom = self.getName()
      while 1:
         msgClient = self.connexion.recv(65536)
         UDecode = msgClient.decode('Utf8')
         IdMode = UDecode[0:3]
         if not msgClient or msgClient.upper() =="FIN":
          break
         elif IdMode == "id:" :
           IdClient = UDecode[3:64]
         elif IdMode =="ss:":
           print("identification en cours....")
           if UDecode[3:9] != "200489":
              break  
         elif IdMode == "ft:" :
           data = msgClient
           for cle in conn_client:
	           if cle != nom:	  
	              conn_client[cle].send(data)
         elif IdMode == "co:" :
            conn_client[nom].send(p1.encode("Utf8"))
            sleep(0.5)
            conn_client[nom].send(k1.encode("Utf8"))
            sleep(0.5)
            conn_client[nom].send(d1.encode("Utf8"))
         else :
          message = "%s> %s" % (IdClient, UDecode)
          print(message)
          # Faire suivre le message à tous les autres clients :
          for cle in conn_client:
	          if cle != nom:	  
	              conn_client[cle].send(message.encode("Utf8"))
 
      # Fermeture de la connexion :
      self.connexion.close()	  # couper la connexion côté serveur
      print("Client %s déconnecté." % nom)
      # Le thread se termine ici
 
# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
  mySocket.bind((HOST, PORT))
except socket.error:
  print("La liaison du socket à l'adresse choisie a échoué.")
  sys.exit()
print("Serveur prêt, en attente de requêtes ...")
mySocket.listen(5)
 
# Attente et prise en charge des connexions demandées par les clients :
conn_client = {}	# dictionnaire des connexions clients
while 1:
  connexion, adresse = mySocket.accept()
  # Créer un nouvel objet thread pour gérer la connexion :
  th = ThreadClient(connexion)
  th.start()
  # Mémoriser la connexion dans le dictionnaire :
  it = th.getName()	  # identifiant du thread
  conn_client[it] = connexion
  print("Client %s connecté, adresse IP %s, port %s." %\
     (it, adresse[0], adresse[1]))
  # Dialogue avec le client :
  msg ="Vous êtes connecté. Envoyez vos messages."
  connexion.send(msg.encode("Utf8"))
