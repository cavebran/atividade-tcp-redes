import os
import pickle
import socket
import threading

PORT = 9000
HOST = 'localhost'
BUFFER_SIZE = 1024
INT_SIZE = 4
DIRECTORY = 'files'
FORMAT = 'utf-8'

def startServer(host, port):
    # inicialização do servidor
    print("[STARTING] Servidor está inicializando...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((host, port))
    except socket.error as e:
        print(str(e))
        
    server.listen(5)
    print(f"[LISTENING] Servidor está escutando em {host}:{port}\n")
    
    while True:
        try:
            conection, address = server.accept() # estabelece conexão com o cliente
            thread = threading.Thread(target=handleClient, args=(conection, address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] Conexões: {threading.active_count() - 1}")
        except KeyboardInterrupt:
            exit()

def handleClient(conection, address):
    print(f"[NEW CONNECTION] {address} conectado.")
    
    conected = True
    while conected:
        cmd = conection.recv(BUFFER_SIZE) # recebe a instrução
        
        if(cmd):
            cmd = cmd.decode(FORMAT)
            
            match cmd:
                case 'upload':
                    upload(conection)
                case 'list':
                    list(conection)
                case 'download':
                    download(conection)
                case 'close':
                    conected = False
                case _:
                    print(f'[ERROR] Comando \'{cmd}\' não reconhecido.')
        else:
            break
    
    conection.close()
    print(f"[CLOSED CONNECTION] {address} desconectado.")
    
def upload(conection): 
    # fileInfo = [<filename>, <filesize>]
    fileInfo = conection.recv(BUFFER_SIZE).decode(FORMAT).split('|') # recebe metadados do upload
    print(f'[METADATA] Informações: {fileInfo}')
    
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

    print(f'[SUCCESS] Arquivo \'{fileName}\' salvo.')

def list(conection):
    fileList = pickle.dumps(os.listdir(DIRECTORY)) # obtem a lista de arquivos do servidor
    listSize = len(fileList)

    conection.sendall(listSize.to_bytes(INT_SIZE, 'big')) # envia o tamanho da lista
    conection.sendall(fileList) # envia a lista
    
    return

def download(conection):    
    fileName = conection.recv(BUFFER_SIZE).decode(FORMAT) # recebe o nome do arquivo
    
    for file in os.listdir(DIRECTORY): # procura o arquivo
        if fileName == file:
            with open(f'{DIRECTORY}\\{fileName}', 'rb') as file:
                fileContent = file.read() # lê o arquivo
                fileContent = pickle.dumps(fileContent)
                fileSize = len(fileContent).to_bytes(INT_SIZE, 'big')
                
                conection.sendall(fileSize) # envia o tamanho do arquivo
                conection.sendall(fileContent) # envia o arquivo
                
                print(f'[SUCCESS] Arquivo \'{fileName}\' enviado.')
                return

    print(f'[ERROR] Arquivo \'{fileName}\' não encontrado.')
    conection.sendall((0).to_bytes(INT_SIZE, 'big'))
    
    return

startServer(HOST, PORT)