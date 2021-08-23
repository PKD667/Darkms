# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connexions clientes en parallèle.
 
Host = 'localhost'
Port = 9999


style = """
|=========================================================|\n
|========================PKD==============================|\n
***********************************************************\n
"""
import time
import socket, sys, threading,os,random,subprocess
import simpleaudio as sa
filesize = 4096
DiN = {}
Queue,cmd_queue = [],[]
password = "200489"
admin = ['pkd']
Folder_Path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(Folder_Path,"log.log")
def initialisation(self) :
     """Fonction d'initialisation de l'adresse et du port du socket """
     global Host
     global Port
     print("Initialisation du serveur ..........................")
     Host = input("Entrez l'adresse du serveur (Default = localhost) : ")
     Port = input("Entrez le port de service du serveur (Default = 9999) :")
     with open (log_path,"a") as log :
       log.write("[============================Nouvelle session serveur===========================]\n")
class InputThread(threading.Thread) :
  """Objet thread qui gère l'input de l'administrateur"""
  def __init__(self) :
    threading.Thread.__init__(self)
  def run (self) :
    while 1 :
      global cmd_queue
      texte = input()
      cmd_queue.append(texte)
class CommandThread(threading.Thread) :
  def __init__(self) :
    threading.Thread.__init__(self)
  def run (self) :
    commands =  [
    ["close",["conncl"]],
    ["set",["password"]],
    ["debug",["true","false"]],
    ["manage",["admin",["out","add"]]],
    ["help"]
    ]
    while 1 :
      global cmd_queue
      global admin
      admin_input = ''
      global Queue
      global password
      try :
          admin_input = cmd_queue[0]
          cmd_queue.remove(admin_input)
          cmd_queue.sort()
      except IndexError :
          pass
      if admin_input[0:1] == '$' :
        command = admin_input[1:4096]
        cmd = command.split()
        try :
         if cmd[0] == "cmd" :
           cmd_path = Folder_Path
           subprocess.run("cd " + cmd_path,shell=True, check=True)
           command = ""
           while command != 'close' :
            try :
               command = input('>')
               exe = subprocess.Popen(command)
               exe.poll()
            except os.error :
                print("La commande n'existe pas ")
         elif cmd[0] == "close" :
           if cmd[1] == "conncl" :
            Queue.append('break' + ':' + cmd[2] )
         elif cmd[0] == "set":
            if cmd[1] == "password" :
              password = cmd[2]
         elif cmd[0] == 'debug' :
              if cmd[1] == 'true' :
                Queue.append('debug:True')
              if cmd[1] == 'false'  :
                    Queue.append('debug:False')
         elif cmd[0] == "manage":
             if cmd[1] == "admin" :
               if cmd[2] == "out" :
                 admin.remove(cmd[3])
               elif cmd[2] == "add":
                  admin.append(cmd[3])
         elif cmd[0] == "help" :
            print()
        except IndexError :
          pass
      else :
        pass
class ThreadClient(threading.Thread):
  '''dérivation d'un objet thread pour gérer la connexion avec un client'''
  Mode = False 
  def __init__(self, conn):
      threading.Thread.__init__(self)
      self.connexion = conn

  def run(self):
    key = '1234'
    Crypted = False
    cmd = '0'
    Break = False
    Debug = False
    mode = "msg"
    nom = self.getName()
    IdClient = nom
    while 1:
      global DiN
      global password
      global cmd_queue
      global Queue
      global admin 
      global filesize
      if Queue != [] :
       for e in Queue :
         if e == "break:" + IdClient :
          Break = True
          Queue.remove(e)
         elif e == 'debug:True' :
           Debug = True
           Queue = Queue.remove(e)
         elif e == 'debug:False' :
           Debug = False
           Queue = Queue.remove(e)
      if Break == True :
        break
      try :
       filesize = int(filesize)
       msgClient = self.connexion.recv(filesize)

       if mode == "ftp" :
         try :
            data = msgClient
            for cle in conn_client:
	            if cle != nom:	  
	              conn_client[cle].send(data)
            with open(path , 'wb') as f:
               print('file openned')
               print('receiving data...')
               f.write(data)
               print('All is done , file is closed')
            mode = 'msg'
         except FileNotFoundError :
           print("Erreur : Le fichier specifié n'existe pas. ")
       else :
        try :
         UDecode = msgClient.decode('Utf8')
         msg_format = UDecode.split(":")
         IdMode = msg_format[0]
         if Debug == True : 
              print('DEBUG, : UDecode :' , UDecode ,' msg_format : ' , msg_format,'IdMode : ' , IdMode)
         if not msgClient or msgClient.upper() =="FIN":
          break
         elif IdMode == "id" :
           IdClient = msg_format[1]
           DiN[nom] = IdClient
         elif IdMode == "$" :
           for j in admin :
              if j == IdClient :
                cmd_queue.append(UDecode.replace(":"," "))
         elif IdMode =="password":
           print("identification en cours....")
           if msg_format[1] != password:
              break  
           else :
             send = "key" + ":" + key
             conn_client[nom].send(send.encode('Utf8'))
         
         elif IdMode == "ftp" :
           filename = msg_format[1]
           filesize = int(msg_format[2])

           path = os.path.join(Folder_Path, "files",filename)
           print("processing PATH.................", path)
           message = 'ftp' + ':' + filename + ':' + str(filesize)
           for cle in conn_client:
	           if cle != nom:	  
	              conn_client[cle].send(message.encode("Utf8"))
           mode = 'ftp'
         elif IdMode == "co" :
            conn_client[nom].send(style.encode("Utf8"))
         elif IdMode == 'dbg' :
            print("Pour l'instant tout va bien !")
         elif IdMode == '!' :
           perso_msg = msg_format[2:]
           print('msg ',IdClient,' to ',msg_format[1],' : ', perso_msg)
           message = ''.join(perso_msg)
           message = "!%s> %s" % (IdClient, message)
           for cle in conn_client:
              if DiN.get(cle) == msg_format[1] :
	                conn_client[cle].send(message.encode("Utf8"))            
         elif IdMode == 'msg' :
          if msg_format[1] == "FIN" :
                 Break = True
          else : 
            message = "%s> %s" % (IdClient, msg_format[1])
            print(message)
            with open (log_path, "a") as log :
              log.write(message + "\n")
            # Faire suivre le message à tous les autres clients :
            for cle in conn_client:
	            if DiN.get(cle) != IdClient:	  
	              conn_client[cle].send(message.encode("Utf8"))
        except UnicodeDecodeError :
          pass       
      except (ConnectionResetError) :
        print("ALERTE!\nCA MARCHE PAS LES POTES")
        break 
    # Fermeture de la connexion :
    self.connexion.close()
    # supprimer l'entrée du client dans le dictionaire conn_client
    del conn_client[nom]
    # couper la connexion côté serveur
    print("Client %s déconnecté." % nom)
    # Le thread se termine ici
 
# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
  mySocket.bind((Host, Port))
except socket.error:
  print("La liaison du socket à l'adresse choisie a échoué.")
  sys.exit()
# Its cool but it only works with an ide or from terminal so I disabled it ]:
#filename = 'supernova.wav'
#wave_obj = sa.WaveObject.from_wave_file(filename)
#play_obj = wave_obj.play()
print('Serveur en attente de requetes ...............')
mySocket.listen(5)

 
# Attente et prise en charge des connexions demandées par les clients :
conn_client = {}	# dictionnaire des connexions clients
cmd = CommandThread()
inpt = InputThread()
inpt.start()
cmd.start()
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
  with open (log_path, "a") as log :
        log.write("Client %s connecté, adresse IP %s, port %s." %\
     (it, adresse[0], adresse[1]) + "\n")
  # Dialogue avec le client :