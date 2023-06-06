import socket
import time
import random
import socket
import threading
from banco import *
import time
from funcoes import *




tamanho = 1024
padrao = "utf-8"
opc_sair = "!SAIR"




def IniciarEleicao():
    print("Iniciando eleição de servidores")
    #carregar ips
    NumPCs = 'NumPCs.txt'
    ipRede='IpRede.txt'

    with open(ipRede, 'r') as arquivo:
        ip = arquivo.read()

    with open(NumPCs, 'r') as arquivo:
        qtd = int(arquivo.read())

    print(qtd)
    
    #gerar base do servidor
    try:
        redes = ConsultarIps()
        print(redes[0][3])
        HOST = redes[0][1]
        PORT =  int(redes[0][2])
    except:
        HOST=ip
        PORT=9998
    # indicacao=int((random.randint(1, 100)*random.randint(1, 100))/random.randint(1, 100))
    indicacao=10
    global trava
    trava=PORT+1
    first=True
    isHost=False
    conectado=True
    for i in range(qtd-1):
        if not conectado:
            break
            
        print(i)
        global msg
        PORT+=  1
        endereco_destino = (HOST, PORT)  # Endereço do próximo nó
        print(endereco_destino)
       
        try:
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.bind(endereco_destino)
            servidor.listen()
            print('Estou ancorado')
            while conectado:
                print('AINDA CONECTADO')
                
                if PORT==trava and first:
                    print('sou o primeiro vou mandar meu voto')
                    first=False
                    enviar_mensagem((HOST,PORT+1), indicacao+2,qtd)
                    # thread = threading.Thread(target=enviar_mensagem, args=((HOST,PORT+1), indicacao,qtd))
                    # thread.start()
                    indicacao+=2
                if i== qtd:
                    PORT-(qtd+1)
                print(PORT)
                
                conn, endereco = servidor.accept()
                print(endereco)
                msg = conn.recv(tamanho).decode(padrao)
                conn.sendall('ok'.encode(padrao))
                # if not first and msg<indicacao:
                #     enviar_mensagem((HOST,PORT+1), indicacao,qtd)
                #     # thread = threading.Thread(target=enviar_mensagem, args=((HOST,PORT+1), indicacao,qtd))
                #     # thread.start()
                try:
                    if  int(msg)<indicacao:
                        enviar_mensagem((HOST,PORT+1), indicacao,qtd)
                    elif int(msg)==indicacao:
                        enviar_aviso(endereco_destino,qtd)
                        ip,port=endereco_destino
                        SetarIP('secondary',ip,str(port),'ativo')
                        conectado=False
                        isHost=True
                        break
                    else:
                        enviar_mensagem((HOST,PORT+1), msg,qtd)
                        # thread = threading.Thread(target=enviar_mensagem, args=((HOST,PORT+1), indicacao,qtd))
                        # thread.start()
                except:
                    print("eleicao encerrada")
                    print('Caminho do novo servidor', msg)
                    msg=msg.replace("(", "").replace(")", "")
                    NewServer=msg.split(',')
                    print(NewServer)
                    ip,host=NewServer
                    SetarIP('secondary',str(ip),str(host),'ativo')
                    print('Conectando ao novo Servidor')
                   
                    break
                
                    
        except:
            next
            time.sleep(1)
    if isHost:
        serverReserva(ip,port)
    else:
        main()
    #transmitir mensagem

    #aguardar mensagem

    #verificar id

    #se for o meu id iniciar servidor

    #se nao for meu id agardar e logar de novo



def enviar_mensagem(no_destino, mensagem,pcs):
    margem=int(no_destino[1])-(trava+1)
    time.sleep(3)
    for i in range (pcs-1):
        
        print(no_destino[1])
        try:
            endereco_destino = (no_destino)  # Endereço do próximo nó
            mensagem_serializada = str(mensagem)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(endereco_destino)
                print('Conectei')
                s.sendall(mensagem_serializada.encode(padrao))
                print('Enviei')
                resposta=s.recv(1024).decode(padrao)
                if resposta=="ok":
                    print("AAAAAAA")
                    break
        except:
       
            if i==(pcs-(margem+1)):
                PORT=no_destino[1]
                PORT-=(pcs-1)
                no_destino=no_destino[0], PORT
            else:
                PORT=no_destino[1]
                PORT+=1
                no_destino=no_destino[0], PORT
                print('erro sem retorno')
            next

def enviar_aviso(servidor,pcs):
    margem=int(servidor[1])-(trava+1)
    HOST,PORT=servidor
    time.sleep(10)
    Vencedor=HOST,PORT
    servidor= HOST,(PORT+1)
    for i in range (pcs-1):
        
        print(servidor[1])
        try:
            endereco_destino = (servidor)  # Endereço do próximo nó
            mensagem_serializada = str(Vencedor)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(endereco_destino)
                print('Conectei para enviar o aviso')
                s.sendall(mensagem_serializada.encode(padrao))
                print('Enviei o aviso')
                resposta=s.recv(1024).decode(padrao)
                if resposta=="ok":
                    print("aviso enviado")
                    break
        except:
       
            if i==(pcs-(margem+1)):
                PORT=servidor[1]
                PORT-=(pcs-1)
                servidor=servidor[0], PORT
            else:
                PORT=servidor[1]
                PORT+=1
                servidor=servidor[0], PORT
                print('erro sem retorno')
            next












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
    

def serverReserva(ip,port):


    print("[INICIANDO] O Servidor está Iniciando...")

    print(f'IP Local: {ip}')
    print('seu ip local será usado para ancoragem do servidor atual')
    SetarIP('primary','0.0.0.0','9998','inativo')
    print(ConsultarIps())

    HOST = ip        # Endereco IP do Servidor
    PORT = str(port)            # Porta que o Servidor esta
    servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    servidor.bind((HOST,PORT))
    servidor.listen(1)
    print(f"[ATIVO] O Servidor está Ativo no: {ip}:{PORT}")

    while(True):
        conn, endereco=servidor.accept()
        thread=threading.Thread(target=conexao, args=( conn, endereco) )
        thread.start()
        print(f"usuarios ativos {threading.active_count()-1} ")



def main():
    contador = 0
    while True:
        

        try:
            redes = ConsultarIps()
            print(redes[0][3])
            HOST = redes[0][1]
            PORT = int(redes[0][2])
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((HOST, PORT))
            mensagem = ""
            primeira = True

            while mensagem != "fim":
                
                if primeira:
                    print("...Iniciando interação com o Servidor")
                    cliente.sendall("vendedor".encode("utf-8"))
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
                        cliente.sendall(mensagem.encode("utf-8"))
                        resposta = cliente.recv(1024)
                  
                
            print("Encerrando o cliente")
            cliente.close()

        except:
            print('Servidor indisponível')
            print('Tentando novamente em alguns segundos')
            time.sleep(5)
            contador += 1

        if contador > 2:
            print("Servidor indisponível, iniciando eleição")
            IniciarEleicao()





if __name__ == "__main__":
    main()











