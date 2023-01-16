import socket
import pickle


PORT = 9000
HOST = 'localhost'

BUFFER_SIZE = 1024
INT_SIZE = 4


def not_found():
    print('Operação inserida inválida invalido')
    return


def upload(client, header):
    fileName = header.split('|')[1]

    try:
        with open(fileName, 'rb') as file:
            fileContent = file.read()
            fileContent = pickle.dumps(fileContent)
            fileSize = len(fileContent)
            
            header += f'|{fileSize}'
            client.sendall(header.encode('utf-8'))

            client.sendall(fileContent)
            print(f'{fileName} enviado!')
        return
    except:
        print('Arquivo não encontrado no diretório atual')
        return


def list(client, header):
    client.sendall(header.encode('utf-8'))
    listSize = int.from_bytes(client.recv(INT_SIZE), 'big')

    listContent = b''
    while True:
        tempList = client.recv(BUFFER_SIZE)
        listContent += tempList
        if len(listContent) >= listSize:
            break

    listContent = pickle.loads(listContent)
    print(f'{listContent}\n')
    
    return

def download(client, header):
    client.sendall(header.encode('utf-8'))
    fileName = header.split('|')[1]

    # Recebemos o tamanho do arquivo
    fileSize = int.from_bytes(client.recv(INT_SIZE), 'big')
    if fileSize == 0:
        print('Arquivo não encontrado')
        return

    fileContent = b''
    
    while True:
        tempFile = client.recv(BUFFER_SIZE)
        fileContent += tempFile
        if len(fileContent) >= fileSize:
            break

    fileContent = pickle.loads(fileContent)

    with open(f'arquivos\\{fileName}', 'wb') as f:
        f.write(fileContent)
        print(f'{fileName} baixado!')
    return

def close(client):
    # encerramos as conexão com o servidor
    client.close()
    # fechamos a aplicação
    exit()


def startClient(HOST, PORT):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print(f'Conectado ao servidor {HOST}:{PORT}')

        while True:
            print('\n\n==== Opções ====')
            print('upload|<filepath> - Upload de arquivo')
            print('list - Lista arquivos do servidor')
            print('download|<filename> - Download de arquivo')
            print('close - Encerra conexão')

            cmd = input()
            
            match cmd.split('|')[0]:
                case 'upload':
                    upload(client, cmd)
                case 'list':
                    list(client, cmd)
                case 'download':
                    download(client, cmd)
                case 'close':
                    close(client)
                case _:
                    print('\nComando não reconhecido')
    finally:
        client.close()
        
startClient(HOST, PORT)