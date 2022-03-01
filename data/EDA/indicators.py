import pandas as pd
import numpy as np
import math

def squeeze_momentum(df):
  #https://medium.com/geekculture/implementing-the-most-popular-indicator-on-tradingview-using-python-239d579412ab
  length=20
  mult = 2
  length_KC = 20
  mult_KC =1.5
  # calculate Bollinger Bands
  # moving average
  m_avg = df['close_price'].rolling(window=length).mean()
  # standard deviation
  m_std = df['close_price'].rolling(window=length).std(ddof=0)
  # upper Bollinger Bands
  df['upper_BB'] = m_avg + mult * m_std
  # lower Bollinger Bands 
  df['lower_BB'] = m_avg - mult * m_std

  # calculate Keltner Channel# first we need to calculate True Range
  df['tr0'] = abs(df["high_price"] - df["low_price"])
  df['tr1'] = abs(df["high_price"] - df["close_price"].shift())
  df['tr2'] = abs(df["low_price"] - df["close_price"].shift())
  df['tr'] = df[['tr0', 'tr1', 'tr2']].max(axis=1)# moving average of the TR
  range_ma = df['tr'].rolling(window=length_KC).mean()
  # upper Keltner Channel
  df['upper_KC'] = m_avg + range_ma * mult_KC
  # lower Keltner Channel
  df['lower_KC'] = m_avg - range_ma * mult_KC

  # calculate bar value -> momentum  || gain or lose
  highest = df['high_price'].rolling(window = length_KC).max()
  lowest = df['low_price'].rolling(window = length_KC).min()
  m1 = (highest + lowest)/2
  df['value'] = (df['close_price'] - (m1 + m_avg)/2)
  fit_y = np.array(range(0,length_KC))
  df['value'] = df['value'].rolling(window = length_KC).apply(lambda x: 
                            np.polyfit(fit_y, x, 1)[0] * (length_KC-1) + 
                            np.polyfit(fit_y, x, 1)[1], raw=True)

  # check for 'squeeze' -> measure of volatility
  df['squeeze_on'] = (df['lower_BB'] > df['lower_KC']) & (df['upper_BB'] < df['upper_KC'])
  df['squeeze_off'] = (df['lower_BB'] < df['lower_KC']) & (df['upper_BB'] > df['upper_KC'])

#rely on the standard deviation -> best filtering noise
def bollinger_bands(df,length = 20,mult = 2 ):
  # moving average
  m_avg = df['close_price'].rolling(window=length).mean()
  # standard deviation
  m_std = df['close_price'].rolling(window=length).std(ddof=0)
  # upper Bollinger Bands
  df['upper_BB'] = m_avg + mult * m_std
  # lower Bollinger Bands 
  df['lower_BB'] = m_avg - mult * m_std
  
  return df

def kertnel_channel(df,length_KC=12,mult_KC =1.5):
  # moving average
  m_avg = df['close_price'].rolling(window=length_KC).mean()
  # calculate Keltner Channel# first we need to calculate True Range
  df['tr0'] = abs(df["high_price"] - df["low_price"])
  df['tr1'] = abs(df["high_price"] - df["close_price"].shift())
  df['tr2'] = abs(df["low_price"] - df["close_price"].shift())
  df['tr'] = df[['tr0', 'tr1', 'tr2']].max(axis=1)# moving average of the TR
  range_ma = df['tr'].rolling(window=length_KC).mean()
  # upper Keltner Channel
  df['upper_KC'] = m_avg + range_ma * mult_KC
  # lower Keltner Channel
  df['lower_KC'] = m_avg - range_ma * mult_KC
  


