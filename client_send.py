
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
host = '127.0.0.1'
port = 999
FILESIZE = 4000000
import logging
from rich.logging import RichHandler
import socket, sys, threading,os
from time import daylight, sleep
sys.stdout = Unbuffered(sys.stdout)
Folder_Path = os.path.dirname(os.path.realpath(__file__))
FORMAT = "%(message)s"
logging.basicConfig(

    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")
class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn):
      threading.Thread.__init__(self)
      self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
       mode = 'none'
       while 1:
          message_recu = self.connexion.recv(FILESIZE)
          if mode == 'ftp' :
             data = message_recu
             with open(path , 'wb') as f:
                log.info('file openned')
                log.info('receiving data...')
                f.write(data)
                log.info('All is done , file is closed')
             mode = 'none'
          else :
           UDecode = message_recu.decode('Utf8')
           if UDecode[0:3] == 'ft:' :
                 filename = UDecode[3:FILESIZE]                 
                 path = os.path.join(Folder_Path, "files",filename)
                 log.info("processing PATH.................", path)
                 log.info('receiving data...')
                 mode = 'ftp'
           else :
            print(message_recu.decode('Utf8'))
            if message_recu =='' or message_recu.upper() == "FIN":
                 break
        # Le thread <réception> se termine ici.
        # On force la fermeture du thread <émission> :
       th_E._Thread__stop()
       log.fatal("Client arrêté. Connexion interrompue.")
       self.connexion.close()
    
class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
        print(Folder_Path)
        file_tansfer_mode = False
        while 1:
          #Transfer du fichier identifié
          if file_tansfer_mode == True :
                 f = open(file,'rb')
                 log.info("File opened.....")
                 l = f.read(FILESIZE)
                 log.info('Reading file...................')
                 data_send = l
                 message_emis = data_send
                 log.info("Message envoyé ...............................................")
                 file_tansfer_mode = False
          else :
            message_emis = input('>')
            ident = message_emis[0:3]
            message_emis = message_emis.encode('Utf8')
            #Identification de la demande de file transfer
            if ident == "ft:":
                 filename = input("Entrez le nom du fichier à transférer : ")
                 file = os.path.join(Folder_Path,filename)
                 message_emis = ident + filename
                 file_tansfer_mode = True
                 message_emis = message_emis.encode('Utf8')
                 
          
          self.connexion.send(message_emis)

# Programme principal - Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    connexion.connect((host, port))
except socket.error:
    log.error("La connexion a échoué.")
    sys.exit()    
log.debug("Connexion établie avec le serveur.")
connexion.send("dbg".encode('Utf8'))
id = input("entrez votre identifiant : ")
password = input("entrez le mot de passe de la salle : ")
password = "ss:" + password
id = "id:" + id
connexion.send(id.encode('Utf8'))  
connexion.send(password.encode('Utf8'))  
a = 1
b = 1
log.info("authentification en cours")
sleep(1)
while a != 50:   
     
    print(".", end='')
    a += b
    sleep(0.01) 

print(".")
log.info("authentification terminée")
connexion.send("co:".encode('Utf8'))  

# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :
th_E = ThreadEmission(connexion)
th_R = ThreadReception(connexion)
th_E.start()
th_R.start()
