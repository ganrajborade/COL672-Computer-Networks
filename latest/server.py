from socket import *
import threading
import time
import matplotlib.pyplot as plt

start = [0]
timing_data = []
lock = threading.Lock()
count = [0]
lst = ['']*1000
#sock1addr = '10.194.33.144'
sock2addr = '10.184.42.213'
#sock1port = 12002
sock2port = 12001
buff_size = 8192
def client_process(connectionSocket, addr):
  print("hello")
  while count[0] < 1000:
    message = connectionSocket.recv(buff_size)
    if(not message):
      continue
    sentence = message.decode()
    if (sentence[0]=='-'):
      continue
    temp = sentence.split('\n',maxsplit = 1)
    index = int(temp[0])
    sentence = temp[1]
    if(lst[index] != ''):
      while(True):
        if(sentence[len(sentence)-1]=='\n'):
          break
        message = connectionSocket.recv(buff_size)
        sentence = message.decode()
    else:
      lock.acquire()   
      count[0]+=1
      elapsed_time = time.time() - start[0]
      timing_data.append((count[0],elapsed_time))     
      # print(count[0])
      #print(sentence,end='')
      while True :
        lst[index]+=sentence
        if(sentence[len(sentence)-1]=='\n'):
          break
        message = connectionSocket.recv(buff_size)
        sentence = message.decode()
      lock.release()
  connectionSocket.close()


def my_client():
  start[0] = time.time() 
  serverName = 'vayu.iitd.ac.in'
  serverPort = 9801
  #sock1 = socket(AF_INET,SOCK_STREAM)
  sock2 = socket(AF_INET,SOCK_STREAM)
  # while True:
  #   try:
  #     sock1.connect((sock1addr,sock1port))
  #     break
  #   except:
  #     {}
  while True:
    try:
      sock2.connect((sock2addr,sock2port))
      break
    except:
      {print("trying")}

  clientSocket = socket(AF_INET, SOCK_STREAM)
  clientSocket.connect((serverName, serverPort))
  sendLine = "SENDLINE\n"
  while count[0] < 1000:
    clientSocket.send(sendLine.encode())
    message = clientSocket.recv(buff_size)
    sentence = message.decode()
    if (sentence[0]=='-'):
      continue
    temp = sentence.split('\n',maxsplit = 1)
    index = int(temp[0])
    sentence = temp[1]
    if(lst[index] != ''):
      while(True):
        if(sentence[len(sentence)-1]=='\n'):
          break
        message = clientSocket.recv(buff_size)
        sentence = message.decode()
    else:
      lock.acquire() 
      count[0]+=1
      elapsed_time = time.time() - start[0]
      timing_data.append((count[0],elapsed_time))
      #print(count[0])
      while True :
        lst[index]+=sentence
        if(sentence[len(sentence)-1]=='\n'):
          break
        message = clientSocket.recv(buff_size)
        sentence = message.decode()
      
      # try:
      #   sock1.send((str(index) + '\n' + lst[index]).encode())
      # except:
      #   {}
      
      try:
        sock2.send((str(index) + '\n' + lst[index]).encode())
      except:
        {}
      lock.release()
  
  end = time.time() 
  print(end - start[0])

  submit = "SUBMIT\n"
  team = "2023MCS2478@dags\n"
  clientSocket.send(submit.encode())
  clientSocket.send(team.encode())
  clientSocket.send('1000\n'.encode())
  for i in range(1000):
    if(lst[i]==''):
      continue
    s = str(i) + '\n'
    s+=lst[i]
    clientSocket.send(s.encode())

  message = clientSocket.recv(buff_size)
  sentence = message.decode()
  print(sentence)
  clientSocket.close()
  #sock1.close()
  sock2.close()
  # Plot the timing data
  x, y = zip(*timing_data)
  plt.plot(x, y, marker='o')
  plt.xlabel("Number of Unique Lines Received")
  plt.ylabel("Time (seconds)")
  plt.title("Time vs. Number of Unique Lines Received")
  plt.grid(True)
  plt.show()



def main():
  threading.Thread(target=my_client).start()
  serverPort = 12003
  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.bind(('10.184.50.108', serverPort))
  serverSocket.listen(15)
  while True:
    connectionSocket, addr = serverSocket.accept()
    client = threading.Thread(target=client_process, args=(connectionSocket,addr))
    client.start()
  
if __name__== "__main__":
  main()
    