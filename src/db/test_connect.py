import psycopg2
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

connection=None
try: 
  connection = psycopg2.connect(
    host=os.environ.get('HOST'),
    user=os.environ.get('USER'),
    password=os.environ.get('PASSWORD'),
    database='postgres'
  )
  print ('conexion exitosa')
  cur = connection.cursor()
  cur.execute('SELECT version()')

  # display the PostgreSQL database server version
  db_version = cur.fetchone()
  print(db_version)
  
  # close the communication with the PostgreSQL
  cur.close()

except Exception as e:
  print(e)

finally:
  if connection is not None:
    connection.close()
    print('conexion finalizada')