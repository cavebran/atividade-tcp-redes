import pickle
import socket
import os

PORT = 9000
HOST = 'localhost'

BUFFER_SIZE = 1024
INT_SIZE = 4

def upload(conection, header): # header = [upload, fileName, fileSize]
    fileName = header[1]
    fileSize = int(header [2])
    fileContent = b''
    
    while True:
        tempFile = conection.recv(BUFFER_SIZE)
        fileContent += tempFile
        if len(fileContent) >= fileSize:
            break

    fileContent = pickle.loads(fileContent)

    with open(f'arquivos\\{fileName}', 'wb') as file:
        file.write(fileContent)

    print('Arquivo salvo')


def list(conection):
    fileList = pickle.dumps(os.listdir('arquivos'))
    listSize = len(fileList)

    conection.sendall(listSize.to_bytes(INT_SIZE, 'big'))

    conection.sendall(fileList)
    return


def download(conection, header): # header = [download, fileName]
    fileName = header[1]
    
    # verificamos se o arquivo se encontra no diretório
    for file in os.listdir('arquivos'):
        if fileName == file:
            print(f'<{file}>')

            with open(fileName, 'rb') as file:
                fileContent = file.read()
                # serializamos o conteúdo
                fileContent = pickle.dumps(fileContent)
                # enviamos o tamnho do arquivo para o cliente
                fileSize = len(fileContent).to_bytes(INT_SIZE, 'big')
                conection.sendall(fileSize)
                conection.sendall(fileContent)
                
                print('Arquivo enviado')
                return

    print('Arquivo nao encontrado')

    conection.sendall((0).to_bytes(INT_SIZE, 'big'))
    return

def startServer(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    
    print('Servidor Iniciado\n')

    while True:
        try:
            # recebemos a conexão com o cliente
            conection, clientAddress = server.accept()
            print(f'Conectado a {clientAddress}')
            
            while True:
                cmd = conection.recv(BUFFER_SIZE)
                if(cmd):
                    cmd = cmd.decode('utf-8').split('|')
                    
                    match cmd[0]:
                        case 'upload':
                            upload(conection, cmd)
                        case 'list':
                            list(conection, cmd)
                        case 'download':
                            download(conection, cmd)
                        case _:
                            print('Comando não reconhecido')
                else:
                    break
        finally:
            conection.close()

startServer(HOST, PORT)