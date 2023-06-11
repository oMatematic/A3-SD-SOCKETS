import socket
import time
import random
import socket
import threading
from banco import *
import time
from funcoes import *
import re



tamanho = 1024
padrao = "utf-8"
opc_sair = "!SAIR"
global sinal
sinal=False
global stop



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
    global inicio
    global ProxNo 
    unico=False
    ProxNo=""
    inicio=PORT+1
    first=True
    isHost=False
    conectado=True

    for i in range(qtd-1):
        if not conectado:
            break
            
        print(i)
        global msg
        
        if (PORT+1)!=inicio:
            PORT=inicio+qtd-i
        else:
            PORT+=1
        endereco_destino = (HOST, PORT)  # Endereço do próximo nó
        print(endereco_destino)
       
        try:
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.bind(endereco_destino)
            servidor.listen()
            
            print('Estou ancorado')
            while conectado:
                try:
                    print('AINDA CONECTADO')
                    
                    if PORT==inicio and first:
                        print('sou o primeiro vou mandar meu voto')
                        first=False
                        ProxNo=enviar_mensagem((HOST,PORT+1), indicacao+2,qtd,inicio,1,PORT)
                        # thread = threading.Thread(target=enviar_mensagem, args=((HOST,PORT+1), indicacao,qtd))
                        # thread.start()
                        
                        indicacao+=2
                    if PORT != inicio:
                        servidor.settimeout(300)

                    if i== qtd:
                        PORT-(qtd+1)
                    
                    if ProxNo == endereco_destino[1]:
                        print("[AVISO] Sou o unico na eleição")
                        ip,port=endereco_destino
                        SetarIP('secondary',ip,str(port),'ativo')
                        conectado=False
                        isHost=True
                        servidor.close()
                        break
                    else:
                        conn, endereco = servidor.accept()
                        print(endereco)
                        msg = conn.recv(tamanho).decode(padrao)
                        conn.sendall('ok'.encode(padrao))
                    
            

                    try:
                        if  int(msg)<indicacao:
                            if ProxNo=="":
                                print("meu numero é maior")
                                ProxNo=enviar_mensagem((HOST,inicio+1), indicacao,qtd,inicio,1,PORT)
                            else:
                                print("meu numero é maior")
                                enviar_mensagem((HOST,int(ProxNo)), indicacao,qtd,inicio,2,PORT)
                        elif int(msg)==indicacao:

                            enviar_aviso(endereco_destino,qtd,ProxNo,PORT)
                            ip,port=endereco_destino
                            SetarIP('secondary',ip,str(port),'ativo')
                            conectado=False
                            isHost=True
                            conn.close()
                            servidor.close()
                            break
                        else:
                            if ProxNo=="": 
                                print("meu numero é menor")
                                ProxNo=enviar_mensagem((HOST,inicio+1), msg,qtd,inicio,1,PORT)
                            # thread = threading.Thread(target=enviar_mensagem, args=((HOST,PORT+1), indicacao,qtd))
                            # thread.start()
                            else:
                                print("meu numero é menor")
                                enviar_mensagem((HOST,ProxNo), msg,qtd,inicio,2,PORT)
                    except:
                        conn.close()
                       
                        
                        print("eleicao encerrada")
                        print('Caminho do novo servidor', msg)
                        msg = re.sub(r"[\'\(\)]", "", msg)
                        NewServer=msg.split(',')
                        print(NewServer)
                        ip,port=NewServer
                        enviar_aviso(NewServer,qtd,ProxNo,PORT)
                        servidor.close()
                        print('Conectando ao novo Servidor')
                        conectado=False
                        break
                except socket.timeout:
                    print("Tempo limite de 30 segundos atingido. Nenhuma conexão foi aceita.")
                    conectado=False
                    print("não consegui participar da eleição")
                    servidor.close()

                    
                    
        except:
            next
            time.sleep(1)
    if isHost:
        serverReserva(ip,port)
    else:
        if port=="":
            main()
        else:
         main(ip,port)
    #transmitir mensagem

    #aguardar mensagem

    #verificar id

    #se for o meu id iniciar servidor

    #se nao for meu id agardar e logar de novo



def enviar_mensagem(no_destino, mensagem,pcs,PortIinicial,operacao, myPort):
    PORT=myPort+1
    no_destino=no_destino[0], PORT
    contador=0
    if operacao==1:
        
     
        for i in range (pcs-1):
            if myPort==(inicio+pcs-1):
                no_destino=no_destino[0], inicio
                PORT=inicio
            if PORT==myPort:
                if i== (pcs-2):
                    no_destino=no_destino[0], inicio
                    PORT=inicio
                else:
                    PORT=no_destino[1]
                    PORT+=1
                    no_destino=no_destino[0], PORT
           
            while contador<3:
                try:
                    endereco_destino = (no_destino)  # Endereço do próximo nó
                    mensagem_serializada = str(mensagem)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        print("[Conectando] Tentando Ancoragem")
                        s.connect(endereco_destino)
                        print('[Conectado] Ancorado, vou enviar meu voto')
                        s.sendall(mensagem_serializada.encode(padrao))
                        print('[Enviado] Voto enviado com sucesso!')
                        resposta=s.recv(1024).decode(padrao)
                        if resposta=="ok":
                            print("Confirmação de voto recebida")
                            return PORT
                except:
                    time.sleep(1)
                    print(f"[ERRO] Porta {no_destino[1]} sem resposta, tentando Novamente")

                    contador+=1
            
        
            
            if PORT==(PortIinicial+(pcs-1)):
                print(f'[SEM CONEXÃO] Porta  {no_destino[1]} sem Retorno, tentando em outra porta')
                PORT=no_destino[1]
                PORT-=(pcs-1)
                no_destino=no_destino[0], PORT
                contador=0
            
            else:
                contador=0
                print(f"[SEM CONEXÃO] Porta {no_destino[1]} sem retorno, tentando em outra porta")
                PORT=no_destino[1]
                PORT+=1
                no_destino=no_destino[0], PORT
     
    else:
        

        while contador<3:
                try:
                    endereco_destino = (no_destino)  # Endereço do próximo nó
                    mensagem_serializada = str(mensagem)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        print("[Conectando] Tentando Ancoragem")
                        s.connect(endereco_destino)
                        print('[Conectado] Ancorado, vou enviar meu voto')
                        s.sendall(mensagem_serializada.encode(padrao))
                        print('[Enviado] Voto enviado com sucesso!')
                        resposta=s.recv(1024).decode(padrao)
                        if resposta=="ok":
                            print("Confirmação de voto recebida")
                            return PORT
                except:
                    time.sleep(1)
                    print(f"[ERRO] Porta {no_destino[1]} sem resposta, tentando Novamente")

                    contador+=1    
        print("[Erro] Sem retorno, voltaremos a varredura ")
        enviar_mensagem(no_destino, mensagem,pcs,1,)   
    
    return PORT

def enviar_aviso(servidor,pcs,proxNo,myport):
    
    HOST,PORT=servidor
    PORT=int(PORT)
    time.sleep(1)
    Vencedor=HOST,PORT
    servidor= HOST,proxNo
    for i in range (pcs-1):
        
         
        
        if servidor[1]==myport:
            if i== (pcs-2):
                servidor= HOST,(inicio)
            else:
                servidor= HOST,(inicio+1)
        if PORT==servidor[1]:
            servidor= HOST,(inicio+1)
        
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
            print(F'erro sem retorno NA PORT {servidor[1]}')
            if servidor[1]==(inicio+pcs-1):
                servidor= HOST,(inicio)
                
            else:
               port=servidor[1]
               servidor= HOST,(port+1) 
                    
            
            next












def conexao( conexao, enderecoCliente):

    print(f"[NOVO USUARIO CONECTADO] {enderecoCliente} conectou.")
    conectado=True
    status=""
    opcao=""
    global sinal

    while conectado and not sinal:
        try:
            msg=conexao.recv(tamanho).decode(padrao)
            if msg=="voltei":
                
                conectado=False
                conexao.close()
               
                sinal=True
            
                break
            if msg =="gerente" and not sinal:
                conexao.sendall("\n\n     [Painel de Gerencia] \n Escolha uma das Funções Abaixo: \n 1 - Listar Vendas \n 2 - Listar Vendedores\n 3 - Vendas de Vendedor Especifico ".encode("utf-8"))
                status=msg
                opcao=conexao.recv(tamanho).decode(padrao)
                if opcao=='1' and not sinal:
                    conexao.send('opcao 1'.encode(padrao))
                elif opcao=='2' and not sinal:
                    conexao.send('opcao 2'.encode(padrao))
                else:
                    conexao.send('opcao invalida'.encode(padrao))
            elif msg=="vendedor" and not sinal:
                conexao.send("[Painel de Vendas] \n Escolha uma das Funções Abaixo: \n 1 - Registrar Venda \n 2 - Listar Vendas".encode("utf-8"))
                status=msg
                opcao=conexao.recv(tamanho).decode(padrao)
                if opcao=='1' and not sinal:
                    Vendedor_CadastrarVenda( conexao)
                elif opcao=='2' and not sinal:
                    Vendedor_ListarVenda(conexao)
                elif opcao=='3' and not sinal:
                    conexao.send('opcao 3'.encode(padrao))
                else:
                    conexao.send('opcao invalida'.encode(padrao))

        
        except:
            next
            conectado=False
            conexao.close()

      
        if stop:
            break     

    conexao.close()
    

def serverReserva(ip,port):
    global sinal
    global stop
    sinal=False
    ativo=True
    stop = False
    print("[INICIANDO] O Servidor está Iniciando...")

    print(f'IP Local: {ip}')
    print('seu ip local será usado para ancoragem do servidor atual')
    SetarIP('primary','0.0.0.0','9998','inativo')
    print(ConsultarIps())

    HOST = ip        # Endereco IP do Servidor
    PORT = port          # Porta que o Servidor esta
    servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    a=0
    while a==0: 
        try:
            servidor.bind((HOST,PORT))
            servidor.listen()
            print(f"[ATIVO] O Servidor está Ativo no: {ip}:{PORT}")
            
            a=1
        except:
            next

    while ativo:
        if  sinal:
            SetarIP('secondary', '0.0.0.0','0000', 'inativo')
            ativo=False
            stop=True
            servidor.close()
            parar_todas_as_threads()
            break
        conn, endereco=servidor.accept()
        thread=threading.Thread(target=conexao, args=( conn, endereco) )
        thread.start()
        print(thread)
        
        print(f"usuarios ativos {threading.active_count()-1} ")
        
        if  sinal:
            ativo=False
            SetarIP('secondary', '0.0.0.0','0000', 'inativo')
            print("[AVISO] O servidor principal está no ar")
            print("Entrando em modo cliente")
            stop=True
            thread.join()
            servidor.close()
            parar_todas_as_threads()
            break

def parar_todas_as_threads():
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()

def main(ip=None,port=0):
    
    contador = 0
    while True:
        

        try:
            if not ip ==None :
                ip.replace("(", "").replace(")", "")
                HOST=ip.replace("'", "").replace(")", "")
                PORT=int(port)
            else:
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
            time.sleep(1.5)
            contador += 1

        if contador > 2:
          
            print("Servidor indisponível, iniciando eleição")
            IniciarEleicao()
            if sinal:
                contador=0




if __name__ == "__main__":
    main()











