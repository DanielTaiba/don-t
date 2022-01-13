import psycopg2
import os
from os.path import join, dirname
from dotenv import load_dotenv


class clientPsql():
  def __init__(self) -> None:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    try:
      self.connector = psycopg2.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database='postgres'
        )
    except Exception as e:
      print (e)
    
    

def create_table(Schemas,interval):
  query= f"""CREATE TABLE "{Schemas}"."{interval}" (
    "Open_time" _int8 NOT NULL ,
    "Open" _float4 NOT NULL,
    "High" _float4 NOT NULL,
    "How" _float4 NOT NULL,
    "Close" _float4 NOT NULL,
    "Volume" _float4 NOT NULL,
    "Close_time" _int8 NOT NULL,
    "Quote_assets_volume" _float8 NOT NULL,
    "Number_of_trades" _int4 NOT NULL,
    "Taker_buy_base_asset_volume" _float4 NOT NULL,
    "Taker_buy_quote_asset_volume" _float4 NOT NULL,
    "Ignore" _float4 NULL,
    primary key ("Open_time")
    );
  """
