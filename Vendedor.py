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
	contador=int(0)
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
			contador+=1

		if contador>2:
			
			print("Servidor indisponivel assumindo Host")
			serverReserva()











tamanho=1024
padrao=("utf-8")
opc_sair="!SAIR"

def conexao( conexao, enderecoCliente):

    print(f"[NOVO USUARIO CONECTADO] {enderecoCliente} conectou.")
    conectado=True
    status=""
    opcao=""
    while conectado:
        try:
            msg=conexao.recv(tamanho).decode(padrao)
            if msg =="gerente":
                conexao.sendall("\n\n     [Painel de Gerencia] \n Escolha uma das Funções Abaixo: \n 1 - Listar Vendas \n 2 - Listar Vendedores\n 3 - Vendas de Vendedor Especifico ".encode("utf-8"))
                status=msg
                opcao=conexao.recv(tamanho).decode(padrao)
                if opcao=='1':
                    conexao.send('opcao 1'.encode(padrao))
                elif opcao=='2':
                    conexao.send('opcao 2'.encode(padrao))
                elif opcao=='3':
                    conexao.send('opcao 3'.encode(padrao))
                else:
                    conexao.send('opcao invalida'.encode(padrao))
            elif msg=="vendedor":
                conexao.send("[Painel de Vendas] \n Escolha uma das Funções Abaixo: \n 1 - Registrar Venda \n 2 - Listar Vendas\n 3 - Vendas de Vendedor Especifico ".encode("utf-8"))
                status=msg
                opcao=conexao.recv(tamanho).decode(padrao)
                if opcao=='1':
                    Vendedor_CadastrarVenda( conexao)
                elif opcao=='2':
                    Vendedor_ListarVenda(conexao)
                elif opcao=='3':
                    conexao.send('opcao 3'.encode(padrao))
                else:
                    conexao.send('opcao invalida'.encode(padrao))

           
        except:
            next
            conectado=False
           

    conexao.close()
    

def serverReserva():


    print("[INICIANDO] O Servidor está Iniciando...")
    ip_local = socket.gethostbyname(socket.gethostname())
    print(f'IP Local: {ip_local}')
    print('seu ip local será usado para ancoragem do servidor atual')
    SetarIP('primary','0.0.0.0','inativo')
    SetarIP('secondary',ip_local,'ativo')
    print(ConsultarIps())

    HOST = ip_local        # Endereco IP do Servidor
    PORT = 9999            # Porta que o Servidor esta
    servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    servidor.bind((HOST,PORT))
    servidor.listen(1)
    print(f"[ATIVO] O Servidor está Ativo no: {ip_local}:{PORT}")

    while(True):
        conn, endereco=servidor.accept()
        thread=threading.Thread(target=conexao, args=( conn, endereco) )
        thread.start()
        print(f"usuarios ativos {threading.active_count()-1} ")































if __name__ == "__main__":
    main()








		