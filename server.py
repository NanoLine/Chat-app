from socket import *
from threading import *
import time

users = []

network = socket(AF_INET, SOCK_STREAM)

ip = '25.38.47.91'

port = 1111

network.bind((ip, port))

network.listen(4)

is_changed = [False]

clients=[]

def client_accept():
    while True:
        client, addr=network.accept()
        clients.append(client)
        if len(users)>0:
            for i in users:
                clients[len(clients)-1].send(bytes(i, 'utf-8'))
                time.sleep(0.1)
        is_changed[0]=True
def send_to(a):
    for i in clients:
        i.send(bytes(a, "utf-8"))
def special_send(a):
    a = a.split('|')
    name = '$Nano'+a[0]+'Line$'
    clients[users.index(name)].send(bytes("$Nano"+a[1]+"Direct$", 'utf-8'))

def read():
    while True:
      if is_changed[0]==True:  
          def mesaj_al_xususi():
              a = clients[len(clients)-1]
              while True:
                  msg = a.recv(100).decode("utf-8")
                  if '$' in msg and 'Nano' in msg and 'Line' in msg:
                      users.append(msg)
                      send_to(users[len(users)-1])
                  else:
                      if 'Everyone|' in msg:
                          send_to(msg[9:])
                      else:
                          special_send(msg)
          t = Thread(target=mesaj_al_xususi)
          t.start()
          is_changed[0] = False

t1 = Thread(target=read)
t2 = Thread(target=client_accept)
t1.start()
t2.start()
