import psycopg2
import os
from os.path import join, dirname
from dotenv import load_dotenv

class clientPsql():
  def __init__(self,db_name='postgres') -> None:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    self.host = os.environ.get('HOST')
    self.user = os.environ.get('USER')
    self.password = os.environ.get('PASSWORD')
    self.db_name = db_name

  def connect(fnc):
    def wrapper(self,**kwargs):
      try:
        connector = psycopg2.connect(
          host=self.host,
          user=self.user,
          password=self.password,
          database=self.db_name
          )
        fnc(self,connector,**kwargs)
      
      except (Exception, psycopg2.DatabaseError) as e:
        print (e)
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
  def create_table(self,connector, **kwargs):
    # dataTypes: https://www.w3schools.com/sql/sql_datatypes.asp
    query= f"""CREATE TABLE "{kwargs['schema']}"."{kwargs['interval']}" (
      "Open_time" bigint not null ,
      "Open" numeric ,
      "High" numeric ,
      "Low" numeric ,
      "Close" numeric ,
      "Volume" numeric ,
      "Close_time" bigint not null,
      "Quote_assets_volume" numeric ,
      "Number_of_trades" int ,
      "Taker_buy_base_asset_volume" numeric ,
      "Taker_buy_quote_asset_volume" numeric ,
      "Ignore" numeric ,
      primary key ("Open_time")
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
  
  @connect
  def insert_data(self,connector):
    pass

  @connect
  def extract_data(self,connector):
    pass
