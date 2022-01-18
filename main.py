from src import clientPsql
from src import marketBNB

if __name__=='__main__':
  #psql = clientPsql(db_name = 'Binance')
  #psql.test_connection()
  #psql.create_table(schema='btc_usdt',interval='1d')
  marketBNB().retype()