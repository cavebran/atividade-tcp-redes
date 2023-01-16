import os
import pickle
import socket
from _thread import *

PORT = 9000
HOST = 'localhost'
BUFFER_SIZE = 1024
INT_SIZE = 4
DIRECTORY = 'files'

def startServer(host, port):
    # inicialização do servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((host, port))
    except socket.error as e:
        print(str(e))
        
    server.listen(5)
    print('Servidor Iniciado')
    
    try:
        while True:
            conection, clientAddress = server.accept() # estabelece conexão com o cliente
            # https://www.positronx.io/create-socket-server-with-multiple-clients-in-python/
            start_new_thread(multiThreadClient, (conection, clientAddress)) # inicia um novo thread para cada conexão
        conection.close()
    except KeyboardInterrupt:
        exit()

def multiThreadClient(conection, clientAddress):
    print(f'Conectado a {clientAddress}\n')
    
    try:
        while True:
                cmd = conection.recv(BUFFER_SIZE) # recebe a instrução
                
                if(cmd):
                    cmd = cmd.decode('utf-8')
                    
                    match cmd:
                        case 'upload':
                            upload(conection)
                        case 'list':
                            list(conection)
                        case 'download':
                            download(conection)
                        case _:
                            print('Comando não reconhecido')
                else:
                    break
    except KeyboardInterrupt:
        exit()

def upload(conection): 
    # fileInfo = [<filename>, <filesize>]
    fileInfo = conection.recv(BUFFER_SIZE).decode('utf-8').split('|') # recebe metadados do upload
    
    fileName = fileInfo[0]
    fileSize = int(fileInfo[1])
    fileContent = b''
    
    while True:
        tempFile = conection.recv(BUFFER_SIZE) # recebe o arquivo
        fileContent += tempFile
        if len(fileContent) >= fileSize:
            break

    fileContent = pickle.loads(fileContent)

    with open(f'{DIRECTORY}\\{fileName}', 'wb') as file: # grava o arquivo no servidor
        file.write(fileContent)

    print('Arquivo salvo')

def list(conection):
    fileList = pickle.dumps(os.listdir(DIRECTORY)) # obtem a lista de arquivos do servidor
    listSize = len(fileList)

    conection.sendall(listSize.to_bytes(INT_SIZE, 'big')) # envia o tamanho da lista
    conection.sendall(fileList) # envia a lista
    
    return

def download(conection, fileName):    
    fileName = conection.recv(BUFFER_SIZE).decode('utf-8') # recebe o nome do arquivo
    
    for file in os.listdir(DIRECTORY): # procura o arquivo
        if fileName == file:
            print(f'<{file}>')

            with open(f'{DIRECTORY}\\{fileName}', 'rb') as file:
                fileContent = file.read() # lê o arquivo
                fileContent = pickle.dumps(fileContent)
                fileSize = len(fileContent).to_bytes(INT_SIZE, 'big')
                
                conection.sendall(fileSize) # envia o tamanho do arquivo
                conection.sendall(fileContent) # envia o arquivo
                
                print('Arquivo enviado')
                return

    print('Arquivo nao encontrado')
    conection.sendall((0).to_bytes(INT_SIZE, 'big'))
    
    return

startServer(HOST, PORT)