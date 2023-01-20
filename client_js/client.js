const net = require('net');
const fs = require('fs');
const { exit } = require('process');
const prompt = require('prompt-sync')({sigint: true});

const PORT = 9000
const HOST = 'localhost'
const BUFFER_SIZE = 1024
const INT_SIZE = 4
const DIRECTORY = 'files'
const FORMAT = 'utf-8'

function startClient(host, port) {
	var client = new net.Socket()

	//connect to the server
	client.connect(port,host, () => {
		console.log(`Conectado ao servidor ${host}:${port}`);

		while(true) {
			let menu = '\n\n============= Opções ============\nupload: Upload de arquivo\nlist: Lista arquivos do servidor\ndownload: Download de arquivo\nclose: Encerra conexão'
			console.log(menu)

			let cmd = prompt('Opção: ');

			switch(cmd) {
				case 'upload':
					let filePath = prompt('Insira o caminho do arquivo: ')
					upload(client, filePath)
					break;
				case 'list':
					console.log('Lista')
					break;
				case 'download':
					let fileName = prompt('Insira o nome do arquivo: ')
					console.log(fileName)
					break;
				case 'close':
					console.log('Close')
					exit()
				default:
					break;
			}
		}
	})

	//handle closed
	client.on('close', function() {
		console.log('server closed connection')
	});
}

function upload(client, filePath) {
	try {
		client.write('upload'); //envia a instrução
		let fileName = filePath.includes('/') ? filePath.split('/').slice(-1)[0] : filePath
		let fileSize = fs.statSync(filePath).size;
		console.log(fileSize)
		let fileInfo = `${fileName}|${fileSize}`

		client.write(fileInfo) // envia metadados do arquivo no formato (<filename>|<filesize>)
		fileContent = fs.readFileSync(filePath)

		let chunks = []
		client.on('data', (fileContent) => {

		})

		
			
		console.log(`${fileName} enviado!`);
	}
	catch(err) {
		console.log(err);
	}

}

startClient(HOST, PORT)