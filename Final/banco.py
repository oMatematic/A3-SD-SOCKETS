import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "referencias.db")


def __init__():
    try:

        banco = sqlite3.connect(db_path)
        cursor = banco.cursor()

        cursor.execute("""
            CREATE TABLE loja (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                cep TEXT,
                numero INTEGER,
                cidade TEXT,
                estado TEXT
                    )
                """)

        cursor.execute("""
            CREATE TABLE vendedor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo TEXT,
                cpf text,
                data_contratacao DATE,
                id_loja INTEGER,
                FOREIGN KEY (id_loja) REFERENCES lojas(id)
                    )
                """)
        cursor.execute("""
                CREATE TABLE vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_vendedor INTEGER,
                    valor DECIMAL,
                    data DATETIME,
                    id_loja INTEGER,
                    FOREIGN KEY (id_vendedor) REFERENCES vendedor(id),
                    FOREIGN KEY (id_loja) REFERENCES loja(id)
                )
            """)
        cursor.execute(
            "CREATE TABLE conexao (tipo text, ip text,port text, status text)")
        cursor.execute(
            "INSERT INTO conexao VALUES('primary','0.0.0.0','9998', 'inativo')")
        cursor.execute(
            "INSERT INTO conexao VALUES('secondary','1.1.1.1','0000','inativo')")
        banco.commit()
        cursor.close()
        banco.close()
    except:
        next


def SetarIP(tipo, ip, port, status):

    banco = sqlite3.connect(db_path)
    cursor = banco.cursor()
    cursor.execute("UPDATE conexao SET ip ='"+ip+"' , port= '" +
                   port+"' , status= '"+status+"' where tipo='"+tipo+"' ")
    banco.commit()
    cursor.close()
    banco.close()


def ConsultarIps():
    ips = []

    banco = sqlite3.connect(db_path)
    cursor = banco.cursor()
    cursor.execute("select * from conexao where status ='ativo' ")
    row = cursor.fetchone()
    ips.append(row)
    banco.commit()
    cursor.close()
    banco.close()
    return ips


def CadastrarVenda(vendedor, valor, idloja, data):
    try:

        banco = sqlite3.connect(db_path)
        cursor = banco.cursor()
        cursor.execute(
            "INSERT INTO vendas (id_vendedor, valor, id_loja, data) VALUES (?, ?, ?, ?)", (vendedor, valor, idloja, data))

        banco.commit()
        cursor.close()
        banco.close()

        return "Venda Salva com sucesso! fim"
    except Exception as erro:

        return "Falha ao Salvar venda! fim"


def ListarVendas(vendedor):
    vendas = 'Vendedor não encontrado'
    banco = sqlite3.connect(db_path)
    cursor = banco.cursor()
    cursor.execute(
        "select SUM(valor) from vendas where vendedor ='"+vendedor+"' ")
    vendas = cursor.fetchone()
    banco.commit()
    cursor.close()
    banco.close()
    return vendas


def cadastrarLoja(nome, cep, numero, cidade, estado):
    try:
        banco = sqlite3.connect(db_path)
        cursor = banco.cursor()
        cursor.execute("""
            INSERT INTO loja (nome, cep,numero, cidade, estado)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, cep, numero, cidade, estado))
        banco.commit()
        cursor.close()
        banco.close()
        return True
    except Exception as e:
        return False


def cadastrarFuncionario(nome, cpf, data_contratacao, id_loja):
    try:
        banco = sqlite3.connect(db_path)
        cursor = banco.cursor()
        cursor.execute("""
            INSERT INTO vendedor (nome_completo, cpf,data_contratacao, id_loja)
            VALUES (?, ?, ?, ?)
        """, (nome, cpf, data_contratacao, id_loja))
        banco.commit()
        cursor.close()
        banco.close()
        return True
    except Exception as e:
        print(e)
        return False


def buscarLoja(nome, cep, numero):
    banco = sqlite3.connect(db_path)
    cursor = banco.cursor()
    cursor.execute("""
        SELECT * FROM loja
        WHERE nome = ? AND cep = ? AND numero = ?
    """, (nome, cep, numero))
    resultados = cursor.fetchone()
    banco.commit()
    cursor.close()
    banco.close()

    return resultados


def listarTodasLojas():

    banco = sqlite3.connect(db_path)
    cursor = banco.cursor()
    cursor.execute("""
    SELECT * FROM loja
""")
    lojas = cursor.fetchall()
    banco.commit()
    cursor.close()
    banco.close()

    return lojas


def buscarVendedor(cpf):

    banco = sqlite3.connect(db_path)
    cursor = banco.cursor()
    cursor.execute("""
        SELECT * FROM vendedor
        WHERE cpf = ? """, (cpf,))
    resultado = cursor.fetchone()
    banco.commit()
    cursor.close()
    banco.close()

    return resultado


def ListarVendasUmaLoja(id):
    vendas = 'A loja não possui Vendas'
    banco = sqlite3.connect(db_path)
    cursor = banco.cursor()
    cursor.execute(
        "select SUM(valor) from vendas where id_loja ='"+id+"' ")
    vendas = cursor.fetchone()
    cursor.execute(
        "select nome from loja where id ='"+id+"' ")
    nome = cursor.fetchone()
    banco.commit()
    cursor.close()
    banco.close()
    return vendas, nome


def buscarPorPeriodo(id_loja, inicio, fim):
    banco = sqlite3.connect(db_path)
    cursor = banco.cursor()
    cursor.execute("""
        SELECT SUM(valor) AS total_vendas
        FROM vendas
        WHERE id_loja = ? AND strftime('%Y-%m-%d', data) BETWEEN ? AND ?""", (id_loja, inicio, fim))

    resultado = cursor.fetchone()
    total_vendas = resultado[0] if resultado else 0
    return total_vendas


def buscarMelhorVendedor():
    try:
        banco = sqlite3.connect(db_path)
        cursor = banco.cursor()
        cursor.execute("""
            SELECT vendedor.nome_completo, SUM(vendas.valor) AS total_vendas
                FROM vendas
                INNER JOIN vendedor ON vendas.id_vendedor = vendedor.id
                GROUP BY vendas.id_vendedor
                ORDER BY total_vendas DESC
                LIMIT 1""")
        resultado = cursor.fetchone()
        total_vendas = resultado[1] if resultado else 0
        nome = resultado[0]
        return total_vendas, nome

    except Exception as e:
        total_vendas = None
        nome = None
        return total_vendas, nome


def buscarMelhorLoja():
    try:
        banco = sqlite3.connect(db_path)
        cursor = banco.cursor()
        cursor.execute("""
            SELECT loja.nome, SUM(vendas.valor) AS total_vendas
                FROM vendas
                INNER JOIN loja ON vendas.id_loja = loja.id
                GROUP BY vendas.id_loja
                ORDER BY total_vendas DESC
                LIMIT 1""")
        resultado = cursor.fetchone()
        total_vendas = resultado[1] if resultado else 0
        nome = resultado[0]
        return total_vendas, nome

    except Exception as e:
        total_vendas = None
        nome = None
        return total_vendas, nome


__init__()
