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
        sql_d="""
        CREATE TABLE IF NOT EXISTS DESCRICAO(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT,
        valor REAL,
        data TEXT
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
        sql_m="""
        CREATE TABLE IF NOT EXISTS METAS(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meta TEXT,
        valor REAL,
        tempo_inicial REAL,
        tempo REAL,
        valor_mensal REAL,
        valor_inicial REAL
        )"""
        sql_me="""
        CREATE TABLE IF NOT EXISTS MENSAL(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        valor REAL,
        tempo_restante REAL,
        mês TEXT
        )"""
        try:
            self.cursor.execute(sql_s)
            self.cursor.execute(sql_g) 
            self.cursor.execute(sql_d)  
            self.cursor.execute(sql_m)         
            self.cursor.execute(sql_me)         
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
        novo_id=self.cursor.lastrowid
        
        self.cursor.execute("UPDATE SALDO SET saldo = saldo - ? WHERE ID=1",(valor,))
        self.conexão.commit()
        return novo_id
    def inserir_metas(self,meta,valor,tempo_inicial,tempo,valor_mensal,valor_inicial):
        self.cursor.execute("INSERT INTO METAS (meta,valor,tempo_inicial,tempo,valor_mensal,valor_inicial) VALUES(?,?,?,?,?,?)",(meta,valor,tempo_inicial,tempo,valor_mensal,valor_inicial))
        self.conexão.commit()
    def inserir_mensal(self,valor,tempo_restante,mes):
        self.cursor.execute("INSERT INTO MENSAL (valor,tempo_restante,mês) VALUES(?,?,?)",(valor,tempo_restante,mes))
        self.conexão.commit()
    def atualizar_mensal(self,id_meta,tempo):
        self.cursor.execute("UPDATE MENSAL SET tempo_restante = ? WHERE id = ?", (tempo, id_meta))
        self.conexão.commit()
    def buscar_mensal(self):
        self.cursor.execute("SELECT id,valor,tempo_restante,mês FROM MENSAL")
        resultado=self.cursor.fetchall()
        mensal=[]
        for linha in resultado:
            mensal.append({'id':linha[0],
                          'valor':linha[1],
                          'tempo_restante':linha[2],
                          'mes':linha[3]})
        return mensal
    def buscar_metas(self):
        self.cursor.execute("SELECT id,meta,valor,tempo_inicial,tempo,valor_mensal,valor_inicial FROM METAS")
        resultado=self.cursor.fetchall()
        metas=[]
        for linha in resultado:
            metas.append({'id':linha[0],
                          'meta':linha[1],
                          'valor':linha[2],
                          'tempo_inicial':linha[3],
                          'tempo':linha[4],
                          'valor_mensal':linha[5],
                         'valor_inicial':linha[6]})
        return metas
    def atualizar_meta(self,meta_id,novo_valor,tempo):
        self.cursor.execute("UPDATE METAS SET valor = ?, tempo = ? WHERE id = ?", (novo_valor, tempo, meta_id))
        self.conexão.commit()
    def remover_gasto(self,gasto_id):
        self.cursor.execute("SELECT gasto FROM GASTO WHERE id=?",(gasto_id,))
        row=self.cursor.fetchone()
        if not row:
            return
        valor=row[0]
        
        self.cursor.execute("DELETE FROM GASTO WHERE id=?",(gasto_id,))
        self.cursor.execute("UPDATE SALDO SET saldo = saldo + ? WHERE id = 1", (valor,))
        self.conexão.commit()
    def resetar_dados(self):
        self.cursor.execute("DELETE FROM GASTO")
        self.cursor.execute("UPDATE SALDO SET saldo = 0.0, receita = 0.0 WHERE id = 1")
        self.cursor.execute("DELETE FROM METAS")
        self.conexão.commit()
    def inserir_descricao(self,descricao,valor,data):
        self.cursor.execute("INSERT INTO DESCRICAO (descricao,valor,data) VALUES(?,?,?)",(descricao,valor,data))
        self.conexão.commit()
    def buscar_descricao(self):
            sql="SELECT id,descricao,valor,data FROM DESCRICAO "
            self.cursor.execute(sql)
            resultado = self.cursor.fetchall()
            descricao=[]
            for linha in resultado:
                descricao.append({'id':linha[0],
                            'descricao':linha[1],
                              'valor':linha[2],
                              'data':linha[3]})
            return descricao
    def buscar_gastos(self):
        try:
            sql="SELECT id ,gasto,onde,categoria FROM GASTO "
            self.cursor.execute(sql)
            resultado = self.cursor.fetchall()
            gasto=[]
            for linha in resultado:
                gasto.append({'id':linha[0],
                            'valor':linha[1],
                              'onde':linha[2],
                              'categoria':linha[3]})
            return gasto
        except db.Error as erro :
            print(f'erro {erro}')