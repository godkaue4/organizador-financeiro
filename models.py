import sqlite3 as db
class banco_de_dados():
    def __init__(self,nome_db='organizador finaceiro.db'):
        self.nome_db=nome_db
        self.conexão=None
        self.cursor=None
        self.conectar()
        self.tabelas()
    def conectar(self):
        try:
            self.conexão=db.connect(self.nome_db)
            self.cursor=self.conexão.cursor()
            print('conectado com sucesso ')
        except:
            print('erro ao conectar bd ')
    def tabelas(self):
        sql_s="""
        CREATE TABLE IF NOT EXISTS SALDO(
        id INTEGER PRIMARY KEY,
        saldo REAL DEFAULT 0.0,
        receita REAL 
            )
            """
        sql_g="""
        CREATE TABLE IF NOT EXISTS GASTO( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,   
        gasto REAL DEFAULT 0.0,
        onde TEXT ,
        categoria TEXT
            )
            """
        try:
            self.cursor.execute(sql_s)
            self.cursor.execute(sql_g)            
            self.cursor.execute("SELECT COUNT(*) FROM SALDO")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("INSERT INTO SALDO (id, saldo,receita) VALUES (1, 0.0,0.0)")
            #self.cursor.execute("SELECT COUNT(*) FROM GASTO")
            #if self.cursor.fetchone()[0] == 0:
                #self.cursor.execute("INSERT INTO GASTO (id, gasto,onde,categoria) VALUES (1, 0.0,NULL,NULL)")
            self.conexão.commit()        

        except db.Error as erro:
            print(f"erro ao criar a tabela {erro}")
    def atualizar_receita(self,valor):
        self.cursor.execute("UPDATE SALDO SET receita = receita + ? where id=1", (valor,))
        self.conexão.commit()
    def atualizar_saldo(self,novo_valor):
        self.cursor.execute("UPDATE SALDO SET saldo = saldo + ? WHERE id = 1", (novo_valor,))
        self.conexão.commit()
    def buscar_receita(self):
        self.cursor.execute("SELECT receita FROM SALDO WHERE id=1")
        return self.cursor.fetchone()[0]
    def buscar_saldo(self):
        self.cursor.execute("SELECT saldo FROM SALDO WHERE id=1")
        return self.cursor.fetchone()[0]
    def inserir_gastos(self,onde,valor,categoria):
        self.cursor.execute("INSERT INTO GASTO (gasto,onde,categoria) VALUES(?,?,?)",(valor,onde,categoria))
        self.cursor.execute("UPDATE SALDO SET saldo = saldo - ? WHERE ID=1",(valor,))
        self.conexão.commit()
    def buscar_gastos(self):
        try:
            sql="SELECT gasto,onde,categoria FROM GASTO "
            self.cursor.execute(sql)
            resultado = self.cursor.fetchall()
            gasto=[]
            for linha in resultado:
                gasto.append({'valor':linha[0],
                              'onde':linha[1],
                              'categoria':linha[2]})
            return gasto
        except db.Error as erro :
            print(f'erro {erro}')