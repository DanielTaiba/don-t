from .utils import query
import pandas as pd
import numpy as np 

class clientBNB(object):
  def __init__(self) -> None:
    self.url = 'https://api.binance.com'
    self.init_timestamp = 1502668800000

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
    
    columns = ['Open_time','Open','High','Low','Close','Volume','Close_Time','Quote_assets_volume','Number_of_trades','Taker_buy_base_asset_volume','Taker_buy_quote_asset_volume','Ignore']
    pd.DataFrame(columns=columns,data=np.array(response.json())).to_csv(f'info/csv/{interval}.csv',index=False)