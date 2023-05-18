# ------------------
# Cliente Socket UDP GERENTE
# ------------------


print("Eu sou um Gerente")

# Importando a biblioteca
import socket


# Definindo ip e porta
HOST = '10.190.32.155'        # Substituir pelo endereco IP do Servidor
PORT = 9000              # Porta que o Servidor ficará escutando

# Criando o socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define o endereco do servidor (Ip e porta)
enderecoServidor = (HOST, PORT)

print("Vou começar a mandar mensagens para o servidor.")

# Aqui começa a conversa		
print("Entrando com mensagem de texto para enviar")
print("(Para sair digite 'fim')")
mensagem = input("Mensagem > ")
mensagem="2"+mensagem
while (mensagem != "fim"):
	# Enviando mensagem ao servidor
	print("... Vou mandar uma mensagem para o servidor")
	cliente.sendto(mensagem.encode("utf-8"), enderecoServidor)

	# Recebendo resposta do servidor
	msg, endereco = cliente.recvfrom(9000)
	print("... O servidor me respondeu:", msg.decode("utf-8"))

	# Obtendo nova mensagem do usuário
	print("... Entrando com nova mensagem de texto para enviar")
	mensagem = input("Mensagem > ")
	mensagem="2"+mensagem
print("... Encerrando o cliente")
cliente.close()
