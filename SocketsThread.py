import socket
import threading
from banco import *
import time
from funcoes import *

time.sleep(5)

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
                    conexao.send('opcao 2'.encode(padrao))
                elif opcao=='3':
                    conexao.send('opcao 3'.encode(padrao))
                else:
                    conexao.send('opcao invalida'.encode(padrao))

           
        except:
            next
            conectado=False
           

    conexao.close()
    

def main():


    print("[INICIANDO] O Servidor está Iniciando...")
    ip_local = socket.gethostbyname(socket.gethostname())
    print(f'IP Local: {ip_local}')
    print('seu ip local será usado para ancoragem do servidor atual')
    SetarIP('primary',ip_local,'ativo')
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




# import socket
# import _thread
# from banco import *
# import time

# time.sleep(5)


# print("Eu sou o SERVIDOR TCP!")
# ip_local = socket.gethostbyname(socket.gethostname())
# print(f'IP Local: {ip_local}')
# print('seu ip local será usado para ancoragem do servidor atual')
# SetarIP('primary',ip_local,'ativo')
# print(ConsultarIps())

# HOST = ip_local        # Endereco IP do Servidor
# PORT = 5000            # Porta que o Servidor esta


# def Funcoes_disponiveis(num):
#     match num:
#         case 0:
#             return "zero"
#         case 1:
#             return "one"
#         case 2:
#             return "two"
#         case default:
#             return "something"
# def Vendedor_CadastrarVenda(con,conexaoCliente):
#     conexaoCliente.sendall("Informe Seu nome".encode("utf-8"))
#     nome=con.recv(1024);
#     print(nome)
#     naoNum=True
#     while (naoNum):
#         conexaoCliente.sendall("Informe Valor da Venda".encode("utf-8"))
#         try:
#             valor=float(con.recv(1024));
#             naoNum=False
#             print(valor)
#         except:
#              conexaoCliente.sendall("Erro! insira uma configuração de moeda válida. Ex: 19.00".encode("utf-8"))
            


# def conectado(con, cliente):
#     print ('Conectado por', cliente)
#     i=0
#     while True:
#         conexaoCliente.sendall("Bem vindo ao caixa tem".encode("utf-8"))
#         conexaoCliente.sendall("escolha uma das opções 1 2".encode("utf-8"))
#         msg = con.recv(1024)
        
#         if not msg: break
#         if int(msg)==1:  
#             Vendedor_CadastrarVenda(con,conexaoCliente)
    

#     print ('Finalizando conexao do cliente'), cliente
#     con.close()
#     _thread.exit()

# servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# servidor.bind((HOST,PORT))
# servidor.listen(1)
# print("Aguardando cliente...")

# while (True):
#     conexaoCliente, enderecoCliente = servidor.accept()
#     _thread.start_new_thread(conectado, tuple([conexaoCliente, enderecoCliente]))



# # mensagem de encerramento
# print("Servidor encerrado.")

