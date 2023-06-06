from banco import *
import re


def Vendedor_CadastrarVenda(con):
    con.send("Informe Seu nome".encode("utf-8"))
    nome = str(con.recv(1024))
    print(type(nome))
    nome = nome[1:]
    nome = re.sub("[']", '', nome)

    print(nome)
    naoNum = True
    con.send("Informe Valor da Venda".encode("utf-8"))
    while (naoNum):

        try:
            valor = float(con.recv(1024))
            naoNum = False
            print(valor)
        except:
            con.send(
                "Erro! insira uma configuração de moeda válida. Ex: 19.00".encode("utf-8"))
    resposta = CadastrarVenda(nome, valor)
    con.send(resposta.encode("utf-8"))


def Vendedor_ListarVenda(con):
    con.send("Informe Seu nome".encode("utf-8"))
    nome = str(con.recv(1024))
    print(type(nome))
    nome = nome[1:]
    nome = re.sub("[']", '', nome)

    print(nome)
    vendas = ListarVendas(nome)
    if vendas[0]==None:
        resposta="Vendedor encontrado!"
    else:
        resposta = f"O valor total de vendas de {nome} foi de R$ {vendas:.2f}"
    con.send(resposta.encode("utf-8"))
    con.send('fim'.encode("utf-8"))
