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
    contador = 0
    while True:
        redes = ConsultarIps()
        print(redes[0][3])
        HOST = redes[0][1]
        PORT = int(redes[0][2])

        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((HOST, PORT))
            mensagem = ""
            primeira = True

            while mensagem != "fim":
                
                if primeira:
                    print("...Iniciando interação com o Servidor")
                    cliente.sendall("gerente".encode("utf-8"))
                    primeira = False
                    resposta = cliente.recv(1024)
                else:
                    if resposta.decode("utf-8")[-3:] == "" or resposta.decode("utf-8")[-3:] == "fim" :
                        print("... >>> O servidor me respondeu:", resposta.decode("utf-8")[:-3])
                        time.sleep(3)
                        mensagem = "fim"
                    elif resposta.decode("utf-8") == 'Opção inválida':
                        print("... >>> O servidor me respondeu:", resposta.decode("utf-8"))
                        cliente.sendall("vendedor".encode("utf-8"))
                        resposta = cliente.recv(1024)
                    else:
                        
                        print("... >>> O servidor me respondeu:", resposta.decode("utf-8"))
                        mensagem = input("Mensagem > ")
                        if mensagem=="":
                            mensagem="invalido"
                        cliente.sendall(mensagem.encode("utf-8"))
                        resposta = cliente.recv(1024)
                  
                
            print("Encerrando o cliente")
            cliente.close()

        except:
            print('Servidor indisponível')
            print('Tentando novamente em alguns segundos')
            
            contador += 1

        if contador > 2:
            print("Servidor indisponível, assumindo Host")
           

tamanho = 1024
padrao = "utf-8"
opc_sair = "!SAIR"

if __name__ == "__main__":
    main()