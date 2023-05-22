from banco import *
import re
def Vendedor_CadastrarVenda(con):
    con.send("Informe Seu nome".encode("utf-8"))
    nome=str(con.recv(1024));
    print(type(nome))
    nome=nome[1:]
    nome=re.sub("[']",'',nome)

    print(nome)
    naoNum=True
    con.send("Informe Valor da Venda".encode("utf-8"))
    while (naoNum):
        
        try:
            valor=float(con.recv(1024));
            naoNum=False
            print(valor)
        except:
             con.send("Erro! insira uma configuração de moeda válida. Ex: 19.00".encode("utf-8"))
    CadastrarVenda(nome,valor)
    con.send("Venda Salva com Sucesso!".encode("utf-8"))