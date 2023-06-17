import socket
import threading
from banco import *
import time
from funcoes import *


tamanho = 1024
padrao = ("utf-8")
opc_sair = "!SAIR"


def conexao(conexao, enderecoCliente):

    print(f"[NOVO USUARIO CONECTADO] {enderecoCliente} conectou.")
    conectado = True
    status = ""
    opcao = ""
    while conectado:
        try:
            msg = conexao.recv(tamanho).decode(padrao)
            if msg == "gerente":
                conexao.sendall(
                    """[Painel de Gerencia] \n Escolha uma das Funções Abaixo:
                      \n    1 - Cadastrar Vendedores 
                      \n    2 - Cadastrar Lojas
                      \n    3 - Listar Vendas Por Nome
                      \n    4 - Listar Vendas Por CPF
                      \n    5 - Vendas de uma Loja
                      \n    6 - Vendas Por Periodo
                      \n    7 - Melhor Vendedor
                      \n    8 - Melhor Loja """.encode(padrao))
                opcao = conexao.recv(tamanho).decode(padrao)
                if opcao=='1':
                    CadastrarVendedor(conexao)
                elif opcao=='2':
                    cadastroDeLoja(conexao)
                elif opcao=='3':
                    vendasDeUmaLoja(conexao)
                elif opcao=='4':
                    cadastroDeLoja(conexao)
                elif opcao=='5':
                    vendasDeUmaLoja(conexao)
                elif opcao=="6":
                    vendasPorPeriodo(conexao)
                elif opcao=="7":
                    melhorVendedor(conexao)
                elif opcao=="8":
                    melhorLoja(conexao)
                else:
                    conexao.send('opcao invalida'.encode(padrao))
            elif msg == "vendedor":
                conexao.send(
                    "\n [       Painel de Vendas       ] \n Escolha uma das Funções Abaixo: \n 1 - Registrar Venda \n 2 - Listar Vendas".encode("utf-8"))
                status = msg
                opcao = conexao.recv(tamanho).decode(padrao)
                if opcao == '1':
                    Vendedor_CadastrarVenda(conexao)
                elif opcao == '2':
                    Vendedor_ListarVenda(conexao)
                else:
                    conexao.send('Opção inválida'.encode(padrao))

        except:
            next
            conectado = False
        finally:
            conexao.close()
    

def enviar_ordem(host,port):
     
    try:
        endereco_destino = ((host,port))  # Endereço do próximo nó
        mensagem_serializada = 'voltei'
        for i in range(2):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(endereco_destino)
                print('Conectei para enviar o aviso')
                s.sendall(mensagem_serializada.encode(padrao))
                print('Enviei o aviso')
                
    except:
        next
        SetarIP('secondary', '0.0.0.0','0000', 'inativo')
        
            
def main():

    redes =ConsultarIps()
    try:
        if  redes[0][0] == 'secondary':
            print(redes[0][3])
            HOST = redes[0][1]
            PORT = int(redes[0][2])
            print(ConsultarIps())
            enviar_ordem(HOST,PORT)
            SetarIP('primary', ip_local,'9998', 'ativo')
    except:
        next

    print("[INICIANDO] O Servidor está Iniciando...")
    ip_local = socket.gethostbyname(socket.gethostname())
    print(f'IP Local: {ip_local}')
    print('seu ip local será usado para ancoragem do servidor atual')
    SetarIP('primary', ip_local,'9998', 'ativo')
    print(ConsultarIps())

    HOST = ip_local        # Endereco IP do Servidor
    PORT = 9998            # Porta que o Servidor esta
    
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(1)
    print(f"[ATIVO] O Servidor está Ativo no: {ip_local}:{PORT}")

    while (True):
        try:
            if  redes[0][0] == 'secondary':
                print(redes[0][3])
                HOST = redes[0][1]
                PORT = int(redes[0][2])
                enviar_ordem(HOST,PORT)
        except:
            next
        conn, endereco = servidor.accept()
        thread = threading.Thread(target=conexao, args=(conn, endereco))
        thread.start()
        print(f"usuarios ativos {threading.active_count()-1} ")


if __name__ == "__main__":
    main()
