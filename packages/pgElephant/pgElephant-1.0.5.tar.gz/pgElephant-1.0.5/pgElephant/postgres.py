import psycopg2


# POSTGRESQL
class PostgreSQL():
    def __init__(self,dbname, user, password, host='localhost', port=5432):
        self._host = host
        self._dbname = dbname
        self._user = user
        self._password = password
        self._port = port
        self._parameters = f"dbname={self._dbname} user={self._user} password={self._password} host={self._host} port={self._port}"

    def connect(self):
        self._conn = psycopg2.connect(self._parameters)
        self._cursor = self._conn.cursor()
        return self._conn
 
    def disconnect(self):
        self._conn.close()
    
    def cursor(self):
        return self._cursor

    def version(self):
        self.execute("SELECT version();")
        return self._cursor.fetchone()
    
    def execute(self, schema: str, vars: tuple = ()):
        self._cursor.execute(schema, vars)

    def commit(self):
        return self._conn.commit()
        
    def deleteTable(self,table:str):
        self.execute(f"""DROP TABLE IF EXISTS {table}""")

    def get_all(self,table:str):
        self.execute(f"""SELECT * FROM {table}""")
        rows = self._cursor.fetchall()

        columns = [column[0] for column in self._cursor.description]

        results = []
        for row in rows:
            result = {}
            for i in range(len(columns)):
                result[columns[i]] = row[i]
            results.append(result)

        return results
    
    def get_single(self, id: str, table: str):
        self.execute(f"SELECT * FROM {table} WHERE id = %s", (id,))
        result = self._cursor.fetchone()

        if result is not None:
            columns = [col[0] for col in self._cursor.description]
            result_dict = {columns[i]: result[i] for i in range(len(columns))}
            return result_dict
        else:
            return None

    def get_first(self, unique: str, table: str, column: str):
        self.execute(f"SELECT * FROM {table} WHERE {column} LIKE %s", ('%' + unique + '%',))
        result = self._cursor.fetchone()

        if result is not None:
            columns = [column[0] for column in self._cursor.description]
            
            result_dict = {}
            for i in range(len(columns)):
                result_dict[columns[i]] = result[i]
            return result_dict
        else:
            return None


