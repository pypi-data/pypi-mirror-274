# pgElephant
PostgreSQL Database Manager

# CREATE ADMIN
bank = PostgreSQL(dbname='my_db',user='my_user',password=my_password)

# CONNECT
bank.connect()

# CHECK
version = bank.version()

# GET ALL VALUES IN ONE TABLE
value_all = bank.get_all(table='users')

# GET A ID
value_single = bank.get_single(id='my_id',table='users')

# GET A SINGLE LINE
value_first = bank.get_first(unique='ryansouza.cwb@gmail.com',table='users',column='email')

# COMMIT
bank.commit()

# DISCONNECT
bank.disconnect()