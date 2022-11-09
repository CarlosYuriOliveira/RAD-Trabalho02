import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2 as conector
import os
from psycopg2 import OperationalError

def centralizarJanela(janela):
    janela.update_idletasks()

    width = janela.winfo_width()
    frm_width = janela.winfo_rootx() - janela.winfo_x()
    win_width = width + 2 * frm_width

    height = janela.winfo_height()
    titlebar_height = janela.winfo_rooty() - janela.winfo_y()
    win_height = height + titlebar_height + frm_width

    x = janela.winfo_screenwidth() // 2 - win_width // 2
    y = janela.winfo_screenheight() // 2 - win_height // 2

    janela.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    janela.deiconify()

def criartabelas(conexao):
    conexao.autocommit = True
    cursor = conexao.cursor()
    #Criando janela CONTA
    try:
        query = """CREATE TABLE conta( 
            Agencia varchar(20),
            Numero varchar(20),
            Saldo float,
            Gerente int,
            Titular int
            )"""
        cursor.execute(query)
        conexao.commit()

        query3 = """create table Banco(
                    Codigo_Banco int,
                    Nome varchar(20),
                    Cidade varchar(20),
                    Estado varchar(20),
                    Nº_Rua Int,
                    Nome_Rua varchar(20)
                    )"""
        cursor.execute(query3)
        conexao.commit()
    #Criando janela PESSOA
        query2 = """create table Pessoa(
            CPF varchar(20),
            Primeiro_Nome varchar(30),
            NomeDoMeio varchar(20),
            Sobrenome varchar(20),
            Idade Int,
            Conta Int,
            Banco Int
            )"""
        cursor.execute(query2)
        conexao.commit()
        messagebox.showinfo(message="Tabelas Criadas com sucesso")
    except OperationalError as e:
        print(f"O erro '{e}' ocorreu")
        messagebox.showinfo(message=f"O erro '{e}' ocorreu")
    cursor.close()

def adicionarArquivos(conexao):
    cursor = conexao.cursor()
    #Adicionando Dados do Arquivos CONTAS
    try:
        arquivo = open("contas.txt", "r")
        for linha in arquivo.readlines():
            agencia = (linha.strip().split()[0])
            num = (linha.strip().split()[1])
            saldo = (linha.strip().split()[2])
            gerente = (linha.strip().split()[3])
            titular = (linha.strip().split()[4])
            query = f"""insert into conta
                values ('{agencia}', '{num}', '{saldo}', '{gerente}', '{titular}')"""
            cursor.execute(query)
            conexao.commit()
        #Adicionando Dados do Arquivo NOMES
        arquivo2 = open("nomes.txt", "r")
        for linha in arquivo2.readlines():
            cpf = (linha.strip().split()[0])
            nom = (linha.strip().split()[1])
            meio = (linha.strip().split()[2])
            sobre = (linha.strip().split()[3])
            idade = (linha.strip().split()[4])
            idconta = (linha.strip().split()[5])
            idbanco = (linha.strip().split()[6])
            query = f"""insert into pessoa
                values ('{cpf}', '{nom}', '{meio}', '{sobre}', '{idade}', '{idconta}', '{idbanco}')"""
            cursor.execute(query)
            conexao.commit()
        arquivo3 =open("bancos.txt", "r")
        for linha in arquivo3.readlines():
            id = (linha.strip().split()[0])
            nome = (linha.strip().split()[1])
            cidade = (linha.strip().split()[2])
            estado = (linha.strip().split()[3])
            num_rua = (linha.strip().split()[4])
            nome_rua = (linha.strip().split()[5])
            query = f"""insert into banco
                values ('{id}', '{nome}', '{cidade}', '{estado}', '{num_rua}', '{nome_rua}')"""
            cursor.execute(query)
            conexao.commit()
        messagebox.showinfo(message="Arquivos Adicionados com Sucesso")
    except OperationalError as e:
        messagebox.showinfo(message=f"O erro '{e} ocorreu'")
    cursor.close()

def consultarRegistro(conexao):
    def consulta(con):
        query = f"""select * from public.pessoa where conta = '{con}'"""
        cursor.execute(query)
        try:
            arquivocv = open("pessoa/nome.csv", "a+")
        except FileNotFoundError as e:
            messagebox.showinfo(message=f"""{e}
Criado Diretorios""")
            os.mkdir("pessoa")
            arquivocv = open("pessoa/nome.csv", "a+")
        linha = cursor.fetchone()
        cod = linha[6]
        arquivocv.writelines(f"""-------------------
CPF: {linha[0]}
Primeiro-Nome: {linha[1]}
Nome-do-Meio: {linha[2]}
Sobrenome: {linha[3]}
Idade: {linha[4]} anos
Id_Conta: {linha[5]}
Codigo_Banco: {linha[6]}
-------------------""")

        query2 = f"""select * from public.conta where titular = '{con}'"""
        cursor.execute(query2)
        try:
            arquivocv2 = open("conta/titular.csv", "a+")
        except FileNotFoundError as e:
            messagebox.showinfo(message=f"""{e}
Criado Diretorios""")
            os.mkdir("conta")
            arquivocv2 = open("conta/titular.csv", "a+")
        linha2 = cursor.fetchone()
        arquivocv2.writelines(f"""-------------------
Id_Titular: {linha2[4]}
Agencia: {linha2[0]}
Numero: {linha2[1]}
Saldo: {linha2[2]}
Gerente: {linha2[3]}
------------------""")

        query3 = f"""select * from public.banco where codigo_banco = '{cod}'"""
        cursor.execute(query3)
        try:
            arquivocv3 = open("banco/banco.csv", "a+")
        except FileNotFoundError as e:
            messagebox.showinfo(message=f"""{e}
        Criado Diretorios""")
            os.mkdir("banco")
            arquivocv3 = open("banco/banco.csv", "a+")
        linha3 = cursor.fetchone()
        arquivocv3.writelines(f"""-------------------
Codigo do Banco: {linha3[0]}
Nome do Banco: {linha3[1]}
Cidade: {linha3[2]}
Estado: {linha3[3]}
Número da Rua: {linha3[4]}º
Nome da Rua/Av.: {linha3[5]}
-------------------""")

        cursor.close()
        messagebox.showinfo(message="Arquivos adicionados")
    janela = tk.Tk()
    centralizarJanela(janela)
    janela.title("Consultando Registros")
    janela.geometry("300x70")
    tk.Label(janela, text="Informe o número da Conta:").grid(row=1, column=1)
    cursor = conexao.cursor()
    conta = tk.Entry(janela)
    conta.grid(row=1, column=2)
    tk.Button(janela, text="Consultar", command=lambda: consulta(conta.get())).grid(row=3, column=1)
    tk.Button(janela, text="Sair", command=lambda: janela.destroy()).grid(row=3, column=2)
    janela.mainloop()

def alterarRegistro(conexao):
    def comitar(tabela, coluna, valornov, conta_titu, coluna2):
        cursor = conexao.cursor()
        query = f"UPDATE {tabela} SET {coluna} = '{valornov}' WHERE {coluna2} = {conta_titu};"
        cursor.execute(query)
        conexao.commit()
        messagebox.showinfo(message="Registro Alterado")
    def alterapessoa():
        janela = tk.Tk()
        centralizarJanela(janela)
        janela.title("PESSOA")
        janela.geometry("300x100")

        tk.Label(janela, text="Qual Coluna").grid(row=1, column=1)
        coluna = ttk.Combobox(janela)
        coluna['values'] = ('cpf', 'primeiro_nome', 'nomedomeio', 'sobrenome', 'idade', 'conta')
        coluna.grid(row=1, column=2)

        tk.Label(janela, text="Qual id da Conta").grid(row=2, column=1)
        conta = tk.Entry(janela)
        conta.grid(row=2, column=2)

        tk.Label(janela, text="Qual o valor novo").grid(row=3, column=1)
        valornov = tk.Entry(janela)
        valornov.grid(row=3, column=2)

        coluna_de_idendificacao="conta"
        tabela = "pessoa"
        tk.Button(janela, text="ALTERAR", command=lambda: comitar(tabela, coluna.get(), valornov.get(), conta.get(), coluna_de_idendificacao)).grid(row=4, column=1)

    def alteraconta():
        janela = tk.Tk()
        centralizarJanela(janela)
        janela.title("CONTA")
        janela.geometry("300x100")
        tk.Label(janela, text="Qual Coluna").grid(row=1, column=1)
        coluna = ttk.Combobox(janela)
        coluna['values'] = ('agencia', 'numero', 'saldo', 'gerente', 'titular')
        coluna.grid(row=1, column=2)

        tk.Label(janela, text="Qual id do Titular").grid(row=2, column=1)
        titu = tk.Entry(janela)
        titu.grid(row=2, column=2)

        tk.Label(janela, text="Qual o valor novo").grid(row=3, column=1)
        valornov = tk.Entry(janela)
        valornov.grid(row=3, column=2)

        coluna_de_identificacao = "titular"
        tabela = "conta"
        tk.Button(janela, text="ALTERAR", command=lambda: comitar(tabela, coluna.get(), valornov.get(), titu.get(), coluna_de_identificacao)).grid(row=4, column=1)

    def alterabanco():
        janela = tk.Tk()
        centralizarJanela(janela)
        janela.title("BANCO")
        janela.geometry("300x100")
        tk.Label(janela, text="Qual Coluna").grid(row=1, column=1)
        coluna = ttk.Combobox(janela)
        coluna['values'] = ('codigo_banco', 'nome', 'cidade', 'estado', 'nº_rua', 'nome_rua')
        coluna.grid(row=1, column=2)

        tk.Label(janela, text="Qual id do Banco").grid(row=2, column=1)
        id = tk.Entry(janela)
        id.grid(row=2, column=2)

        tk.Label(janela, text="Qual o valor novo").grid(row=3, column=1)
        valornov = tk.Entry(janela)
        valornov.grid(row=3, column=2)

        coluna_de_identificacao = "codigo_banco"
        tabela = "banco"
        tk.Button(janela, text="ALTERAR", command=lambda: comitar(tabela, coluna.get(), valornov.get(), id.get(), coluna_de_identificacao)).grid(row=4, column=1)

    janela = tk.Tk()
    centralizarJanela(janela)
    janela.title("Escolha de Tabela")
    janela.geometry("320x70")
    tk.Frame(master=janela, width=68).grid(row=1)
    tk.Button(janela, text="PESSOA", command=lambda: alterapessoa()).grid(row=2, column=1)
    tk.Frame(master=janela, width=20).grid(row=2, column=2)
    tk.Button(janela, text="CONTA", command=lambda: alteraconta()).grid(row=2, column=3)
    tk.Frame(master=janela, width=20).grid(row=2, column=4)
    tk.Button(janela, text="BANCO", command=lambda: alterabanco()).grid(row=2, column=5)
    tk.Frame(master=janela, height=10).grid(row=3, column=2)
    tk.Button(janela, text="SAIR", command=lambda: janela.destroy()).grid(row=4, column=3)
    janela.mainloop()

def removerRegistro(conexao):
    def comitar(conta):
        cursor = conexao.cursor()

        query = f"delete from pessoa where conta = '{conta}'"
        cursor.execute(query)
        conexao.commit()

        query2 = f"delete from conta where Titular = '{conta}'"
        cursor.execute(query2)
        conexao.commit()
        messagebox.showinfo(message="Registro Removido")
    def comitarbanco(cod):
        cursor = conexao.cursor()
        query = f"delete from banco where codigo_banco = '{cod}'"
        cursor.execute(query)
        conexao.commit()
        messagebox.showinfo(message="Registro Removido")

    def janelabanco():
        janela = tk.Tk()
        janela.title("Remover Banco")
        centralizarJanela(janela)
        tk.Label(janela, text="Informe o codigo:").grid(row=1, column=1)
        cod = tk.Entry(janela)
        cod.grid(row=1, column=2)
        tk.Button(janela, text="REMOVER", command=lambda : comitarbanco(cod.get())).grid(row=2, column=1)

    janela = tk.Tk()
    janela.title("Remoção de Registro")
    centralizarJanela(janela)
    janela.geometry("310x120")
    tk.Frame(master=janela, width=15).grid(row=1)
    tk.Label(janela, text="Informe o número da Conta").grid(row=2, column=1)
    conta = tk.Entry(janela)
    conta.grid(row=2, column=2)
    tk.Frame(master=janela, height=20).grid(row=3, column=1)
    tk.Button(janela, text="REMOVER", command=lambda : comitar(conta.get())).grid(row=4, column=1)
    tk.Frame(master=janela, height=15).grid(row=5, column=1)
    tk.Button(janela, text="Remover do Banco", command=lambda: janelabanco()).grid(row=6, column=2)

def criar_conexao(db_name, db_user, db_password, db_host, db_port):
    global conexao
    try:
        conexao = conector.connect(
            database = db_name,
            user = db_user,
            password = db_password,
            host = db_host,
            port = db_port)
        print("Data Base conectado com SUCESSO")
    except OperationalError as e:
        print(f"O erro '{e}' ocorreu")
    janela.destroy()
    janela2 = tk.Tk()
    centralizarJanela(janela2)
    janela2.geometry("260x200")
    janela2.title("Opções de Manipulação")
    tk.Frame(master=janela2, width=265).grid(row=1)
    tk.Frame(master=janela2, height=10).grid(row=1)
    tk.Button(janela2, text="CRIAR TABELAS", command=lambda : criartabelas(conexao)).grid(row=2)
    tk.Frame(master=janela2, height=10).grid(row=3)
    tk.Button(janela2, text="ADICIONAR ARQUIVOS", command=lambda : adicionarArquivos(conexao)).grid(row=4)
    tk.Frame(master=janela2, height=10).grid(row=5)
    tk.Button(janela2, text="CONSULTAR EM ARQUIVOS", command=lambda : consultarRegistro(conexao)).grid(row=6)
    tk.Frame(master=janela2, height=10).grid(row=7)
    tk.Button(janela2, text="ALTERAR REGISTROS", command=lambda : alterarRegistro(conexao)).grid(row=8)
    tk.Frame(master=janela2, height=10).grid(row=9)
    tk.Button(janela2, text="REMOVER REGISTROS", command=lambda : removerRegistro(conexao)).grid(row=10)
    janela2.mainloop()
    conexao.close()

janela = tk.Tk()
centralizarJanela(janela)
janela.title("Conectar ao Banco de Dados")
janela.geometry("340x260")
tk.Frame(master=janela, width=58).grid(row=1)
tk.Frame(master=janela, height=20).grid(row=1)
tk.Label(janela, text="Nome data base: ").grid(row=2, column=1)
name = tk.Entry(janela)
name.grid(row=2, column=2)
tk.Frame(master=janela, height=15).grid(row=3)
tk.Label(janela, text="Nome Usuario: ").grid(row=4, column=1)
usu = tk.Entry(janela)
usu.grid(row=4, column=2)
tk.Frame(master=janela, height=15).grid(row=5)
tk.Label(janela, text="Senha: ").grid(row=6, column=1)
sen = tk.Entry(janela, show="*")
sen.grid(row=6, column=2)
tk.Frame(master=janela, height=15).grid(row=7)
tk.Label(janela, text="Nome HOST: ").grid(row=8, column=1)
ho = tk.Entry(janela)
ho.grid(row=8, column=2)
tk.Frame(master=janela, height=15).grid(row=9)
tk.Label(janela, text="Porta: ").grid(row=10, column=1)
po = tk.Entry(janela)
po.grid(row=10, column=2)
tk.Frame(master=janela, height=15).grid(row=11)

tk.Button(janela, text="Conectar", command=lambda: criar_conexao(f"{name.get()}", f"{usu.get()}", f"{sen.get()}", f"{ho.get()}", f"{po.get()}")).grid(row=12, column=1)

tk.Button(janela, text="Sair", width=10, command=lambda: janela.destroy()).grid(row=12, column=2)

janela.mainloop()
