from datetime import datetime
from banco import *
import requests
cep=input()
def consultar_cep(cep):
    url = (f"https://viacep.com.br/ws/{cep}/json/")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
dados=consultar_cep(cep)

print(dados)


agora = datetime.now()
formato = "%Y-%m-%d %H:%M:%S"
data_formatada = agora.strftime(formato)


def cadastroDeLoja(con):

    cadastrarLoja("casas dias", 19, '15', data_formatada)




    con.send("Informe o nome da loja".encode("utf-8"))
    nome = str(con.recv(1024))
    print(type(nome))
    nome = nome[1:]
    nome = re.sub("[']", '', nome)

    print(nome)
    naoNum = True
    con.send("Informe o Cep da Loja".encode("utf-8"))
    dados=None
    while (naoNum):

        try:
            cep = con.recv(1024)
            dados=consultar_cep(cep)
            
            print(dados)
            naoNum = False
        except:
            con.send(
                "CEP inválido! insira uma configuração de CEP válida. Ex: 41305100".encode("utf-8"))