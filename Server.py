# -------------------
# Servidor Socket UDP
# -------------------

# importando a biblioteca
import socket
import time
import csv
print("Eu sou o SERVIDOR UDP!")

# definindo ip e porta
HOST = '10.190.32.155'       # Substituir pelo endereco IP do Servidor
PORT = 9000          # Porta que o Servidor ficará escutando


# criando o socket e associando ao endereço e porta
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((HOST, PORT))


 
def lerTxt():
    file = open("resd.txt","r") 
    Counter = 0
    Content = file.read() 
    CoList = Content.split("\n") 
    
    for i in CoList: 
        if i: 
            Counter += 1

    return Counter



def lerTxt():
    with open('resd.txt', 'r') as f:
        return f.read()
a=2
while a > 1:
    print("-----")
    # cliente conectou - recuperando informações do cliente
    msg, enderecoCliente = servidor.recvfrom(9000)
    print(f"Cliente {enderecoCliente} enviou mensagem")

    mensagem = msg.decode("utf-8")
    teste = mensagem[0]
    print(teste)
    if teste == '2':
        with open('resd.txt', 'a') as f:
            f.write(mensagem + "\n")
        resposta = "salvo com sucesso"
        servidor.sendto(resposta.encode("utf-8"), enderecoCliente)

    else:
        servidor.sendto(lerTxt().encode("utf-8"), enderecoCliente)

print("Encerrando o servidor...")
servidor.close()
