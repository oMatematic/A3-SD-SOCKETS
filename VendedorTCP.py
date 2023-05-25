import socket
import threading
from banco import *
import time
from funcoes import *
print("Eu sou um CLIENTE 2!")

# redes=ConsultarIps()
# print(redes[0][1])
# HOST = redes[0][1]
# PORT = 9999



def main():

	while(True):

		redes=ConsultarIps()


		print(redes[0][3])
		HOST = redes[0][1]
		PORT = int(redes[0][2])


		try:
			cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			cliente.connect((HOST, PORT))
			mensagem=""
			primeira=True
			while (mensagem != "fim"):
					# Enviando mensagem ao servidorf
				if primeira:
					print("...Iniciando interação com o Servidor")
					cliente.sendall("vendedor".encode("utf-8"))
					primeira=False
					resposta = cliente.recv(1024)
					# print("... >>> O servidor me respondeu:", resposta.decode("utf-8"))
				
				print("... >>> O servidor me respondeu:", resposta.decode("utf-8"))
				mensagem = input("Mensagem > ")
				cliente.sendall(mensagem.encode("utf-8"))

					# Recebendo resposta do servidor
				resposta = cliente.recv(1024)
				if resposta.decode("utf-8")=="fim":
					mensagem=resposta
				
			print("Encerrando o cliente")
			cliente.close()

		except:
			print('Servidor indisponível')
			print('Tentando novamente em alguns segundos')
			time.sleep(5)
		

if __name__ == "__main__":
    main()








		