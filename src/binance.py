from .utils import query,writeResponses
import pandas as pd
import numpy as np 
from .db import clientPsql

class marketBNB(object):
  def __init__(self) -> None:
    self.url = 'https://api.binance.com'
    self.init_timestamp = 1502668800000
    self.db_name = 'Binance'

  def klines(self,symbol = 'BTCUSDT', interval = '1d' ,**kwargs):
    endpoint = '/api/v3/klines'
    """
    https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
    https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-streams
    **kwargs:
      - startTime: LONG int-> is start timestamp
      - endTime: LONG int -> is end timestamp
      - limit: INT -> default 500, max 1000 items returned
    """
    parameters = {
      'symbol':symbol,
      'interval': interval,
      **kwargs,

    }
    response = query(endpoint=self.url+endpoint,parameters=parameters)
    #writeResponses(response,fileName='btc_usdt_1d')
    self.write_db(interval,response,'btc_usdt')
    
  def retype(self,data = list()):
    columns = ['Open_time','Open','High','Low','Close','Volume','Close_Time','Quote_assets_volume','Number_of_trades','Taker_buy_base_asset_volume','Taker_buy_quote_asset_volume','Ignore']
    df = pd.DataFrame(columns=columns,data=np.array(data))
    df.astype({
      'Open':'float64',
      'High':'float64',
      'Low':'float64',
      'Close':'float64',
      'Volume':'float64',
      'Quote_assets_volume':'float64',
      'Taker_buy_base_asset_volume':'float64',
      'Taker_buy_quote_asset_volume':'float64',
      'Ignore':'int32'
      })
    #values_query = ','.join([ f"({','.join(rows.values)})" for _,rows in df.iterrows()])
    #print(values_query)
    return df
  
  def write_db(self,interval,response,schema):
    df = self.retype(response)
    psql = clientPsql(db_name='Binance')
    psql.insert_data(schema = schema, table_name=interval,df = df)


