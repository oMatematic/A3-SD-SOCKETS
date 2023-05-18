# -------------------
# Servidor Socket UDP
# -------------------

# importando a biblioteca
import socket
import time
print("Eu sou o SERVIDOR UDP!")

# definindo ip e porta
HOST = '10.190.32.155'       # Substituir pelo endereco IP do Servidor
PORT = 9000          # Porta que o Servidor ficará escutando


# criando o socket e associando ao endereço e porta
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((HOST, PORT))


print("Aguardando cliente...")

while (True):
	print("-----")
	# cliente conectou - recuperando informações do cliente
	msg, enderecoCliente = servidor.recvfrom(9000)
	print(f"Cliente {enderecoCliente} enviou mensagem")
	
	mensagem = msg.decode("utf-8")
	print(f"Mensagem enviada pelo cliente: {mensagem}")
	print(f"Este servidor vai devolver a mensagem ao cliente {enderecoCliente}")
	mensagem="mensagem enviada padrão"
	
	servidor.sendto(mensagem.encode("utf-8"), enderecoCliente)


print("Encerrando o servidor...")
servidor.close()
