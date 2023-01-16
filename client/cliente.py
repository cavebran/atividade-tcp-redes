import socket
import pickle

PORT = 9000
HOST = 'localhost'
BUFFER_SIZE = 1024
INT_SIZE = 4
DIRECTORY = 'files'

def upload(client, filePath: str):
    client.sendall('upload'.encode('utf-8')) # envia a instrução
    fileName = filePath.split('/')[-1] if filePath.__contains__('/') else filePath

    try:
        with open(filePath, 'rb') as file:
            fileContent = file.read() # abre o arquivo local
            fileContent = pickle.dumps(fileContent)
            fileSize = len(fileContent)
            
            # envia metadados do arquivo no formato (<filename>|<filesize>)
            fileInfo = f'{fileName}|{fileSize}'
            print(fileInfo)
            client.sendall(fileInfo.encode('utf-8')) 
            client.sendall(fileContent) # envia o conteúdo do arquivo
            
            print(f'{fileName} enviado!')
        return
    except:
        print('Arquivo não encontrado no diretório atual')
        return

def list(client):
    client.sendall('list'.encode('utf-8')) # envia a instrução
    listSize = int.from_bytes(client.recv(INT_SIZE), 'big') # recebe o tamanho da lista

    listContent = b''
    while True:
        tempList = client.recv(BUFFER_SIZE) # recebe o conteúdo da lista
        listContent += tempList
        if len(listContent) >= listSize:
            break

    listContent = pickle.loads(listContent)
    print(f'{listContent}')
    
    return

def download(client, fileName):
    client.sendall('download'.encode('utf-8')) # envia a instrução
    client.sendall(fileName.encode('utf-8')) # envia o nome do arquivo a ser baixado

    fileSize = int.from_bytes(client.recv(INT_SIZE), 'big') # recebe o tamanho do arquivo
    
    if fileSize == 0:
        print('Arquivo não encontrado')
        return

    fileContent = b''
    while True:
        tempFile = client.recv(BUFFER_SIZE) # recebe o arquivo
        fileContent += tempFile
        if len(fileContent) >= fileSize:
            break

    fileContent = pickle.loads(fileContent)

    with open(f'{DIRECTORY}\\{fileName}', 'wb') as f: # grava em disco local
        f.write(fileContent)
        print(f'{fileName} baixado!')
    return

def close(client):
    client.close()
    exit()

def startClient(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        print(f'Conectado ao servidor {host}:{port}')

        while True:
            print('\n\n===== Opções =====')
            print('upload: Upload de arquivo')
            print('list: Lista arquivos do servidor')
            print('download: Download de arquivo')
            print('close: Encerra conexão')

            cmd = input()
            
            match cmd.split('|')[0]:
                case 'upload':
                    print('Insira o caminho do arquivo:')
                    filePath = input()
                    upload(client, filePath)
                
                case 'list':
                    list(client)
                    
                case 'download':
                    print('Insira o nome do arquivo:')
                    fileName = input()
                    download(client, fileName)
                    
                case 'close':
                    close(client)
                    
                case _:
                    print('\nComando não reconhecido')
    finally:
        client.close()
        
startClient(HOST, PORT)