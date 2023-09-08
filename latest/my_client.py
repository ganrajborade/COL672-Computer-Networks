from socket import *
import threading
import time
lock = threading.Lock()
count = [0]
lst = ['']*1000
my_peeraddr = '10.194.55.66'
my_peerport = 12001


def my_client():
  start = time.time() 
  serverName = 'vayu.iitd.ac.in'
  serverPort = 9801
  my_peer = socket(AF_INET,SOCK_STREAM)
  while(True):
    try :
      my_peer.connect((my_peeraddr,my_peerport))
      break
    except :
      {}
  
  clientSocket = socket(AF_INET, SOCK_STREAM)

  clientSocket.connect((serverName, serverPort))
  sendLine = "SENDLINE\n"
 
  while True:
    if(count[0]==1000):
      break
    clientSocket.send(sendLine.encode())
    message = clientSocket.recv(2048)
    sentence = message.decode()
    senstr = sentence
    if (sentence[0]=='-'):
      continue
    temp = sentence.split('\n',maxsplit = 1)
    index = int(temp[0])
    sentence = temp[1]
    # if(lst[index] != ''):
    #   while(True):
    #     if(sentence[len(sentence)-1]=='\n'):
    #       break
    #     message = clientSocket.recv(2048)
    #     sentence = message.decode()
    if(lst[index] == ''):
      lock.acquire()        
      count[0]+=1
      print(count[0])
      while True :
        lst[index]+=sentence
        try:
          my_peer.send(senstr.encode())
          # why send everytime sentence partially, why not send after complete sentence
        except:
          print(end = '')
        if(sentence[len(sentence)-1]=='\n'):
          break
        message = clientSocket.recv(2048)
        sentence = message.decode()
        senstr = sentence
      lock.release()

  
  end = time.time() 
  print(end - start)

  submit = "SUBMIT\n"
  team = "2023MCS2478@dags\n"
  # clientSocket = socket(AF_INET, SOCK_STREAM)
  # clientSocket.connect(("vayu.iitd.ac.in",9801))
  clientSocket.send(submit.encode())
  clientSocket.send(team.encode())
  clientSocket.send('1000\n'.encode())

  for i in range(1000):
    if(lst[i]==''):
      continue
    s = str(i)
    s +='\n'
    s+=lst[i]
    clientSocket.send(s.encode())
    try :
      my_peer.send(s.encode())
    except :
      print(end='')

  message = clientSocket.recv(2048)
  sentence = message.decode()
  print(sentence)
  clientSocket.close()
  my_peer.close()