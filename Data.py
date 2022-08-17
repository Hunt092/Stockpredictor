import numpy as np
import pandas_datareader as web
from keras.models import load_model
import pickle
import datetime
from datetime import date
from sklearn.preprocessing import MinMaxScaler

scaler= MinMaxScaler(feature_range=(0,1))
model = load_model('Models\LSTMmodel.h5')
#scaler= pickle.load(open('Models\scaler1.sav','rb'))

def get_stock(value):
  if value.upper() =='HDFC':
    return 'HDFCBANK.NS'
  elif value.upper() == 'INFOSYS':
    return 'INFY.NS'
  elif value.upper() == 'NIFTY':
    return '^NSEI'
  elif value.upper() == 'SENSEX':
    return '^BSESN'
  elif value.upper() == 'HUL':
    return 'HINDUNILVR.NS'
  elif value.upper() == 'RELIANCE':
    return 'RELIANCE.NS'
  elif value.upper() == 'TCS':
    return 'TCS.NS'


def get_data(stock):
  start = date.today() - datetime.timedelta(days=84)
  end = date.today()
  data = web.DataReader( stock,"yahoo", start, end)
  df1 = data.reset_index()['Adj Close']
  df1 = scaler.fit_transform(np.array(df1).reshape(-1,1))
  test_data = df1[-50:,:]
  a_input=test_data[len(test_data) - 50:].reshape(1,-1)
  t_input=list(a_input)
  t_input=a_input[0].tolist()
  return a_input, t_input


def predict(a_input, t_input):
  output=[]
  steps=50
  i=0
  while(i<10):
    if(len(t_input)>50):
        a_input=np.array(t_input[1:])
        a_input=a_input.reshape(1,-1)
        a_input = a_input.reshape((1, steps, 1))
        yhat = model.predict(a_input, verbose=0)
        t_input.extend(yhat[0].tolist())
        t_input=t_input[1:]
        output.extend(yhat.tolist())
        i=i+1
    else:
        a_input = a_input.reshape((1, steps,1))
        yhat = model.predict(a_input, verbose=0)
        t_input.extend(yhat[0].tolist())
        output.extend(yhat.tolist())
        i=i+1
  output=np.array(output)
  output=scaler.inverse_transform(output)
  output= output.tolist()
  return output