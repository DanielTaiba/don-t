from .utils import query, writeResponses
from .postgresql import clientPsql

class marketBNB(object):
  def __init__(self) -> None:
    self.url = 'https://api.binance.com'
    self.init_timestamp = 1502668800000
    self.db_name = 'Binance'

  def exchange_info(self):
    endpoint = '/api/v3/exchangeInfo'
    response = query(endpoint=self.url+endpoint)
    print(response.json())
    writeResponses(response,fileName='ExchangeInfo')

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
    return response.json()

  def save_klines(self,base_asset = str, quote_asset = str, interval = str, **kwargs):
    #getklines
    symbol = base_asset.upper()+quote_asset.upper()
    data = self.klines(symbol=symbol,interval=interval,**kwargs)
    #transform datatypes of klines
    self.change_type(*data)
    #insert data in db
    schema = base_asset.lower()+'_'+quote_asset.lower()
    self.write_db(schema,interval,*data)

  def change_type(self,*args):
    for kline in args:
      kline[:] = map(str,kline[:])

  def write_db(self,schema,table_name,*data):
    kwargs={
      'schema':schema,
      'table_name': table_name,
      'data':data
    }
    psql = clientPsql(db_name=self.db_name)
    psql.insert_data(**kwargs)


if __name__=='__main__':
  #psql = clientPsql(db_name = 'Binance')
  #psql.test_connection()
  #psql.create_table(schema='btc_usdt',interval='1d')
  marketBNB().save_klines(base_asset='btc',quote_asset='usdt',interval='1w')
  #marketBNB().exchange_info()
