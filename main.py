from src import clientBNB

if __name__=='__main__':
  clientBNB().klines(interval='1w',limit=1000)