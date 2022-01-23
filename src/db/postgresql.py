import psycopg2
import os
from os.path import join, dirname
from dotenv import load_dotenv

class clientPsql():
  def __init__(self,db_name='postgres') -> None:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    self.__host = os.environ.get('HOST')
    self.__user = os.environ.get('USER')
    self.__password = os.environ.get('PASSWORD')
    self.db_name = db_name
    self.columns = ['open_time','open_price','high_price','low_price','close_price','volume','close_time','quote_assets_volume','number_of_trades','taker_buy_base_asset_volume','taker_buy_quote_asset_volume','ignore']

  def connect(fnc):
    def wrapper(self,**kwargs):
      try:
        connector = psycopg2.connect(
          host=self.__host,
          user=self.__user,
          password=self.__password,
          database=self.db_name
          )
        fnc(self,connector,**kwargs)
      
      except (Exception, psycopg2.DatabaseError) as e:
        print ('connect..',e)
        connector=None
      
      finally:
        if connector is not None:
          connector.close()
    
    return wrapper

  @connect
  def test_connection(self,connector):
    cur = connector.cursor()
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(db_version)
    cur.close()

  def create_schema(self,connector,schema):
    try:
      cur = connector.cursor()
      query = f"""CREATE SCHEMA {schema}
      AUTHORIZATION {self.user};
      """
      cur.execute(query)
      connector.commit()
    except Exception as e:
      print('create schema...', e)
    
  def schema_exist(self,connector,schema):
    try:
      cur = connector.cursor()
      cur.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema}';")
      if cur.fetchone() is not None:
        connector.commit()
        cur.close()
        return True
      else:
        return False
      
    except Exception as e:
      print('schema exist?', e)

  @connect
  def create_table(self,connector,**kwargs):
    # dataTypes: https://www.w3schools.com/sql/sql_datatypes.asp
    query= f"""CREATE TABLE {kwargs['schema']}._{kwargs['table_name']} (
      "open_time" bigint not null ,
      "open_price" numeric ,
      "high_price" numeric ,
      "low_price" numeric ,
      "close_price" numeric ,
      "volume" numeric ,
      "close_time" bigint not null,
      "quote_assets_volume" numeric ,
      "number_of_trades" int ,
      "taker_buy_base_asset_volume" numeric ,
      "taker_buy_quote_asset_volume" numeric ,
      "ignore" numeric ,
      primary key ("open_time")
      );
    """
    try:
      if not self.schema_exist(connector,schema=kwargs['schema']):
        self.create_schema(connector,kwargs['schema'])
      cur = connector.cursor()
      cur.execute(query)
      connector.commit()
      cur.close()
    except Exception as e:
      print('create table ...',e)

  def table_exist(self,connector,schema, table_name):
    try:
      cur = connector.cursor()
      cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = {schema} AND TABLE_NAME = _{table_name};")
      if cur.fetchone() is not None:
        connector.commit()
        cur.close()
        return True
      else:
        return False
      
    except Exception as e:
      print('schema exist?', e)
    pass

  @connect
  def insert_data(self,connector, **kwargs):
    initial_query = f""" INSERT INTO {kwargs['schema']}._{kwargs['table_name']} 
    ({",".join(self.columns)})
    VALUES
    """
    values_query = ','.join([f"({','.join(values)})" for values in kwargs['data']])+';'

    query = initial_query + values_query

    try:
      if not self.table_exist(connector,kwargs['schema'],kwargs['table_name']):
        self.create_table(connector,**kwargs)
      cur = connector.cursor()
      cur.execute(query)
      connector.commit()
      cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
      print('insert data ...',e)
    

  @connect
  def extract_data(self,connector):
    pass


if __name__=='__main__':
  clientPsql(db_name='Binance').create_table(schema='btc_usdt',table_name='1d')