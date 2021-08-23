
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
host = 'localhost'
port = 9999
input_queue = []
key = 0
filesize = 4096
crypted = False
import simpleaudio as sa
import logging
from rich.logging import RichHandler
import socket, sys, threading,os,time,subprocess
from time import daylight, sleep
sys.stdout = Unbuffered(sys.stdout)
Folder_Path = os.path.dirname(os.path.realpath(__file__))
FORMAT = "%(message)s"
logging.basicConfig(

    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")
def crypt(key,msg) :
    Cmsg = list(msg)
    for i in range(len(key)) :
        for z in range(len(Cmsg)) :
          Cmsg[z] = ord(Cmsg[z]) * int(key[i])
          Cmsg[z] = str(Cmsg[z])
          print(Cmsg)
    
    Fmsg = '¤'.join(Cmsg)
    print(Fmsg)
    return Fmsg 
def décrypt(key,msg) :
    Cmsg = msg.split("¤")
    for i in range(len(key)) :
        for z in range(len(Cmsg)) :
          Cmsg[z] = int(Cmsg[z]) / int(key[i])
          Cmsg[z] = chr(int(Cmsg[z]))
          print(Cmsg)
    Fmsg = ''.join(Cmsg)
    print(Fmsg)
    return Fmsg 
    

def identification() :
    id = input("entrez votre identifiant : ")
    password = input("entrez le mot de passe de la salle : ")
    password = "password:" + password
    id = "id:" + id
    connexion.send(id.encode('Utf8'))  
    connexion.send(password.encode('Utf8'))  
    log.info("authentification en cours")
    sleep(1)
    print("..............................................")
    log.info("authentification terminée")
    connexion.send("co:".encode('Utf8'))
class InputThread(threading.Thread) :
  def __init__(self) :
    threading.Thread.__init__(self)
  def run (self) :
    while 1 :
      global input_queue
      texte = input()
      input_queue.append(texte)
class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn):
      threading.Thread.__init__(self)
      self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
       mode = 'msg'
       global filesize
       global key
       global crypted
       while 1:
          message_recu = self.connexion.recv(filesize)
          if mode == 'ftp' :
            try :
             data = message_recu
             with open(path , 'wb') as f:
                log.info('file openned')
                log.info('receiving data...')
                f.write(data)
                log.info('All is done , file is closed')
             mode = 'msg'
            except FileNotFoundError :
                log.error("Le fichier spécifié n'existe pas")
          elif mode == 'msg' :
            try :
             UDecode = message_recu.decode('Utf8')
             msg_format = UDecode.split(":")
             if msg_format[0] == 'ftp' :
                 filename = msg_format[1]   
                 filesize =  int(msg_format[2]  )  
                 path = os.path.join(Folder_Path, "files",filename)
                 log.info("processing PATH.................")
                 log.info('receiving data...')
                 mode = 'ftp'
             elif msg_format[0] == "key" :
                key =  msg_format[1]
                print(key)
             else :
              print(message_recu.decode('Utf8'))
              if message_recu.decode('Utf8') =='' or message_recu.decode('Utf8').upper() == "FIN":
                log.fatal("Ahhhhh déconection")
                break
            except UnicodeDecodeError :
                pass
        # Le thread <réception> se termine ici.
        # On force la fermeture du thread <émission> :
       log.fatal("Client arrêté. Connexion interrompue.")
       self.connexion.close()
    
class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
        mode = "msg"
        while 1:
          global key
          global input_queue
          global crypted
          if mode == "ftp" :
                 f = open(file,'rb')
                 log.info("File opened.....")
                 log.info("processing filesize.................")
                 l = f.read(filesize)
                 log.info('Reading file...................')
                 data_send = l
                 message_emis = data_send
                 log.info("Message envoyé ...............................................")
                 mode = "msg"
                 mode = 'msg'
          elif mode == "msg" :
           try:
            message_emis = ""
            message_input = input_queue[0]
            input_queue.remove(message_input)
            message_format = message_input.split()
            ident = message_format[0]
            #Identification de la demande de file transfer
            if message_format[0] == "ftp":
              try :
                 try :
                     filename = message_format[1]
                 except :
                    filename = input("Entrez le nom du fichier à transférer : ")
                 if filename[0:2] == 'C:' :
                     file = filename  
                 else :
                     file = os.path.join(Folder_Path,filename)
                 filesize = os.path.getsize(file)
                 filename = os.path.basename(file)
                 message_emis = 'ftp' + ':' + filename + ':' + str(filesize)
                 mode = "ftp"
                 message_emis = message_emis.encode('Utf8')
              except FileNotFoundError :
                  log.error("Le fichier spécifié n' existe pas ! ")
                  message_emis = message_emis.encode('Utf8')
                  pass
            elif message_format[0] == "$" :
              if message_format[1] == "cmd" :
                command = ""
                cmd_path = Folder_Path
                subprocess.run("cd " + cmd_path,shell=True, check=True)
                while command != 'close' :         
                  try :
                     command = input('>')
                     exe = subprocess.Popen(command)
                     exe.poll()
                  except os.error :
                    print("La commande n'existe pas ")
              else :
                message_emis = message_input.replace(" ",":")
            elif ident[0:1] == "!" :
                message_emis = message_input.replace(" ",":")
            else :
                message_emis = 'msg:' + message_input
           except IndexError : 
              filename = ''
          if type(message_emis) is str :
              message_emis = message_emis.encode('Utf8')
              crypt(key,message_emis)
          self.connexion.send(message_emis)
# Programme principal - Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((host, port))

except socket.error:
    log.error("La connexion a échoué.")
    sys.exit()   
# Its cool but it only works with an ide or from terminal so I disabled it ]:
# filename = 'supernova.wav'
# wave_obj = sa.WaveObject.from_wave_file(filename)
# play_obj = wave_obj.play()

log.debug("Connexion établie avec le serveur.")

connexion.send("dbg".encode('Utf8'))
# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :
identification()
th_E = ThreadEmission(connexion)
th_R = ThreadReception(connexion)
th_I = InputThread()
th_I.start()
th_E.start()
th_R.start()
#zone de commande
