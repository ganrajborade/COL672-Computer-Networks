from socket import *
import time
serverName = 'vayu.iitd.ac.in'
serverPort = 9801
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
masterSocket = socket(AF_INET, SOCK_STREAM)
masterSocket.connect(('10.194.55.66',12001))

lst = [False]*1000
sendLine = "SENDLINE\n"
try:
  while (True):
    clientSocket.send(sendLine.encode())
    message = clientSocket.recv(2048)
    sentence = message.decode()
    if (sentence[0]=='-'):
      continue
    temp = sentence.split('\n',maxsplit=1)
    index = int(temp[0])
    if(lst[index]== True):
      while(True) :
        if(sentence[len(sentence)-1]=='\n'):
          break
        message = clientSocket.recv(2048)
        sentence = message.decode()
    else:
      lst[index] = True
      while(True) :
        masterSocket.send(sentence.encode())
        if(sentence[len(sentence)-1]=='\n'):
          break
        message = clientSocket.recv(2048)
        sentence = message.decode()
except Exception as e:
  print(e)
  masterSocket.close()
  clientSocket.close()