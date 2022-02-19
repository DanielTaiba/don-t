from ..data import waiterPsql
import pandas as pd

class df(waiterPsql):

  @waiterPsql.connect
  def extract_data(self,connector,**kwargs):
    query = """
    select * from btc_usdt._1w
    """
    return pd.read_sql(query,connector)

if __name__=='__main__':
  resp = df().extract_data(db_name='Binance')
  print(resp)