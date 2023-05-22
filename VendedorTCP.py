import socket
import time
print("Eu sou um CLIENTE 2!")

# importando a biblioteca

# definindo ip e porta
HOST = '192.168.20.105'
PORT = 9999



def main():
	while(True):
		try:
			cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			cliente.connect((HOST, PORT))
			print("... Vou manda uma mensagem para o servidor")
			mensagem=""
			while (mensagem != "fim"):
					# Enviando mensagem ao servidorf
				
				mensagem = input("Mensagem > ")
				cliente.sendall(mensagem.encode("utf-8"))

					# Recebendo resposta do servidor
				resposta = cliente.recv(1024)

					# exibindo resposta
				print("... >>> O servidor me respondeu:", resposta.decode("utf-8"))

			print("Encerrando o cliente")
			cliente.close()

		except:
			print('Servidor indisponível')
			print('Tentando novamente em alguns segundos')
			time.sleep(2)

if __name__ == "__main__":
    main()








		