
from postgresql import clientPsql
import requests

class marketBNB(object):
  def __init__(self) -> None:
    self.url = 'https://api.binance.com'
    self.init_timestamp = 1502668800000
    self.db_name = 'Binance'
    self.columns = ['open_time','open_price','high_price','low_price','close_price','volume','close_time','quote_assets_volume','number_of_trades','taker_buy_base_asset_volume','taker_buy_quote_asset_volume','ignore']

  def query(self,endpoint = '', parameters = {} ):
    """
    HTTP Return Codes

    HTTP 4XX return codes are used for malformed requests; the issue is on the sender's side.
    HTTP 403 return code is used when the WAF Limit (Web Application Firewall) has been violated.
    HTTP 429 return code is used when breaking a request rate limit.
    HTTP 418 return code is used when an IP has been auto-banned for continuing to send requests after receiving 429 codes.
    HTTP 5XX return codes are used for internal errors; the issue is on Binance's side. It is important to NOT treat this as a failure operation; the execution status is UNKNOWN and could have been a success.

    """
    header={
      'Accepts': 'application/json',
    }

    response = requests.get(url=endpoint,headers=header,params=parameters)

    if response.status_code == 200:
      return response
    else:
      print("HTTP Return Codes\n\n\
            HTTP 4XX return codes are used for malformed requests; the issue is on the sender's side.\n\
            HTTP 403 return code is used when the WAF Limit (Web Application Firewall) has been violated.\n\
            HTTP 429 return code is used when breaking a request rate limit.\n\
            HTTP 418 return code is used when an IP has been auto-banned for continuing to send requests after receiving 429 codes.\n\
            HTTP 5XX return codes are used for internal errors; the issue is on Binance's side. It is important to NOT treat this as a failure operation; the execution status is UNKNOWN and could have been a success."
            )
      print (f'error: {response.status_code}')
      exit()

  def exchange_info(self):
    endpoint = '/api/v3/exchangeInfo'
    response = self.query(endpoint=self.url+endpoint)
    print(response.json())
    #writeResponses(response,fileName='ExchangeInfo')

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

    response = self.query(endpoint=self.url+endpoint,parameters=parameters)
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
      'data':data,
      'db_name':self.db_name,
      'columns': self.columns
    }
    clientPsql().insert_data(**kwargs)


if __name__=='__main__':
  #psql = clientPsql(db_name = 'Binance')
  #psql.test_connection()
  #psql.create_table(schema='btc_usdt',interval='1d')
  marketBNB().save_klines(base_asset='btc',quote_asset='usdt',interval='1w')
  #marketBNB().exchange_info()
