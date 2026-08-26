import sqlite3 as db
class banco_de_dados():
    def __init__(self,nome_db='organizador finaceiro.db'):
        self.nome_db=nome_db
        self.conexão=None
        self.cursor=None
        self.tabelas()
    def tabelas(self):
        sql="""CREATE TABLE IF NOT EXISTS SALDO(
            id INTEGER PRIMARY KEY,
            saldo REAL DEFAULT 0.0,
            )
            CREATE TABLE IF NOT EXISTS GASTOS(
                gasto REAL DEFAULT 0.0,
                onde TEXT NOT NULL,
                categoria TEXT)
                """
    def conectar(self):
        try:
            self.conexão=db.connect(self.nome_db)
            self.cursor=self.conexão.cursor()
            print('conectado com sucesso ')
        except:
            print('erro ao conectar bd ')
            
        