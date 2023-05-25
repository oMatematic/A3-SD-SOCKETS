import sqlite3
import os


def __init__():
    try:

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "referencias.db")
        banco = sqlite3.connect(db_path)
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE vendas (vendedor text,valor decimal)")
        cursor.execute("CREATE TABLE conexao (tipo text, ip text,port text, status text)")
        cursor.execute("INSERT INTO conexao VALUES('primary','0.0.0.0','9998', 'inativo')")
        cursor.execute("INSERT INTO conexao VALUES('secondary','1.1.1.1','9999','inativo')")
        banco.commit()
        cursor.close()
        banco.close()
    except:
        next

def SetarIP(tipo,ip, status):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "referencias.db")
    banco = sqlite3.connect(db_path)
    cursor = banco.cursor()
    cursor.execute("UPDATE conexao SET ip ='"+ip+"' , status= '"+status+"' where tipo='"+tipo+"' ")
    banco.commit()
    cursor.close()
    banco.close()


def ConsultarIps():
    ips=[]
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "referencias.db")
    banco = sqlite3.connect(db_path)
    cursor = banco.cursor()
    cursor.execute("select * from conexao where status ='ativo' ")

    row = cursor.fetchone()
    ips.append(row)

    banco.commit()
    cursor.close()
    banco.close()
    return ips


def CadastrarVenda(vendedor, valor):
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "referencias.db")
        banco = sqlite3.connect(db_path)
        # banco = sqlite3.connect('referencias.db')
        cursor = banco.cursor()
        cursor.execute("INSERT INTO vendas VALUES (?, ?)", (vendedor, valor))
        banco.commit()
        cursor.close()
        banco.close()

        return "Venda Salva com sucesso!"
    except:
        return "Falha ao Salvar venda!"
    
def ListarVendas(vendedor):
    vendas=[]
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "referencias.db")
    banco = sqlite3.connect(db_path)
    cursor = banco.cursor()
    cursor.execute("select SUM(valor) from vendas where vendedor ='"+vendedor+"' ")
    vendas=cursor.fetchone()[0]
    banco.commit()
    cursor.close()
    banco.close()
    return vendas


__init__()
