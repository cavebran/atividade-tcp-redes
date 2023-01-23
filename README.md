# Atividade de Redes - Construção de comunicação cliente servidor com TCP

## Clientes

### Python
Para rodar o cliente pyhton, é necessário ter o python instalado previamente, navegar até a pasta ```client_python``` e executar o comando ```py client.py```.

### Javascript (Node)
Para rodar o cliente Node, é necessário ter o npm e o node instalados previamente. Navegar até a pasta ```client_js```, executar o comando ```npm install``` e em seguida ```node client.js```

### Java
Para rodar o cliente Java, uma das formas é ter o Netbeans instalado e executar o projeto através da própria IDE.

## Servidor
Para rodar o servidor, é necessário ter o python instalado previamente, navegar até a pasta ```server_python``` e executar o comando ```py server.py```.

### Observações gerais
O projeto funcionando 100% a comunicação só vale para cliente python com servidor python. O motivo não é por conta do protocolo e sim das dificuldades qur tivemos em desenvolver os métodos de comunicação em algumas lingaugens. Detalhando os problemas:
- Cliente javascript: O único método que conseguimos realizar foi o de upload.
- Cliente java: Há problemas na decodificação das mensagens, não conseguimos fazer o "parse" para UTF-8.