import socket
import threading
from banco import *
import time
from funcoes import *
print("Eu sou um Gerente")

# importando a biblioteca

# definindo ip e porta
HOST = '192.168.20.105'
PORT = 9999



def main():
	while(True):
		try:
			redes=ConsultarIps()


			print(redes[0][2])
			HOST = redes[0][1]
			PORT = 9999



			cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			cliente.connect((HOST, PORT))
			mensagem=""
			primeira=True
			while (mensagem != "fim"):
					# Enviando mensagem ao servidorf
				if primeira:
					cliente.sendall("gerente".encode("utf-8"))
					primeira=False
				print("... Vou manda uma mensagem para o servidor")
				resposta = cliente.recv(1024)
				print("... >>> O servidor me respondeu:", resposta.decode("utf-8"))
				mensagem = input("Mensagem > ")
				cliente.sendall(mensagem.encode("utf-8"))

					# Recebendo resposta do servidor
				resposta = cliente.recv(1024)

					# exibindo resposta
				
				

			print("Encerrando o cliente")
			cliente.close()

		except:
			print('Servidor indisponível')
			print('Tentando novamente em alguns segundos')
			time.sleep(5)

if __name__ == "__main__":
    main()