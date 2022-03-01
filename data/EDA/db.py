import os
from os.path import join, dirname
from dotenv import load_dotenv
import psycopg2

class waiterPsql():
  def __init__(self) -> None:
    dotenv_path = join(dirname(__file__), 'psql.env')
    load_dotenv(dotenv_path)

    #self.function = fnc
    self.__host = os.environ.get('HOST')
    self.__user = os.environ.get('USER')
    self.__password = os.environ.get('PASSWORD')
  
  def read(self,**kwargs):
    response = None
    try:
      connector = psycopg2.connect(
        host=self.__host,
        user=self.__user,
        password=self.__password,
        database=kwargs['db_name']
        )
      try:
        cur = connector.cursor()
        cur.execute(kwargs['query'])
        response = cur.fetchall()
        
      except Exception as e:
        print('error read db...', e)
    
    except (Exception, psycopg2.DatabaseError) as e:
      print ('Error connect...',e)
      connector=None
    
    finally:
      if connector is not None:
        connector.close()
      if response is not None:
        return response
  
  def get_conn(self,db_name='Binance'):
    try:
      connector = psycopg2.connect(
        host=self.__host,
        user=self.__user,
        password=self.__password,
        database=db_name
        )
    
    except (Exception, psycopg2.DatabaseError) as e:
      print ('Error connect...',e)
      connector=None
    
    finally:
      return connector
  

