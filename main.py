from fastapi import FastAPI
from pydantic import BaseModel

from pybit import usdt_perpetual
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta
from tradingview_ta import TA_Handler, Interval

app = FastAPI()

class Msg(BaseModel):
    msg: str

config = {
  "type": "service_account",
  "project_id": "tradingview-ta",
  "private_key_id": "87264596c1d9b69a1c8ae2e6404df888304c6c89",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDW/P/n2YYYA34b\nqOHIm8kYyCX9jUyuBbmdVu6AL8SVYTTzDXyqfB3L5JuKS5RPpQ7Spt4d/18qsNJZ\nvukKrGF5B4GO2gBc9KxeOXSjtI5E2MvpfF0V+V2WyeQi8l/6dWkzbFgNdsKhbxR7\nKSBA8Sf/yKK1Wr4sn//End7B2Em1MQEy6KAvUBeFMAWyHQfR+srf7+5giJ05GDT3\nAYc6U0gX6Ta47bnctZy6Cx23tYEYSU2X7aMTt27U0V3+Cr1BPQFhwlCksFtdvPfU\n2bcvlGhN7cfoJKZvUBb/WwlyKY55j9k6wNBUvciByaq02bmt6yH5Kh6g0G+bMSQB\nQcVcEo2PAgMBAAECggEABWE/ZiXjXSZ5OWf4fnSni582lCm9CX3LL0zFmx+W48YS\n9SIZRIrmk/uciNFrXLLctBjI5idF0mOqX+SPIF0/8y9k5pY9/BWDWrhFWvNhvAdQ\n0v7xtWMQHH3g358BF9toTokfiva12CRXdt2ImRdv0M7Mg41JxQQb+meY83DeJ1KO\n3UPiMgxFhkiaft5c/FjBYsS94mprqf+fvdzvjpySxsWFkMi/YMQNvRWBdRldWlcO\nhDfs0I+uUHDS+bDS4sSWe8oQECKv2uT6GMPvtMqSGZPXdpnDhb+MWBUZ6ZDEAqaO\nkKMGedhyFd1aVp/ybmk4hVvdb132/Em669PH/PgeAQKBgQDzbEupBpKGiwlbDbR4\nppZxHEeiwb1DpMvPkq+D1PfIGr75B+m+vbhB4uZrj50wwlNjBo4Dfe6pZ1Vb+rXU\ngnKnt09lglmsntVhp4+/JpJGBaFug7mjAgIkXZF5W5vLN5V7aLq9T6LEffm6fToa\nXsASlW8BcghhjagDMZ3BCsj9oQKBgQDiGJqNVe+VkstiS5xoCMdbtjaN7+regk1f\nik1rvWBHRYw3tkYkGDXIjjUoYljeHlNw7MccYyGcMu0dF/fI9xFV3FCZnsmSZrxZ\nVs5EGOMWZVds/dOUXJdMmhGuRFcx3azAmZSS4k7Z0fLfXLruPR19gQRbHgRA5rY1\nLEDEgzjdLwKBgQCGRITTPcnSppxJehzCs/ileVjWIJE534t/+kQProfh+0a9bCz1\nRgZ9aR950uR8gaOnKnVo3ayoClReAMMM7cs6UXVc43J9Mbs3O0qhwC/MqcxqfgQG\nMtRlpKraSrp7dDRittjSFTwNsALwZ6SF6R9+4KgzHugajx1Oba67TSyiIQKBgAMb\nvXw18z5GL1+hlHvlqv/6yFM5Oixm9DNdDmVtzBYOwbe+XMaAQrUIJ3jvqTMcjZ8e\n0jn0rvCbzqC4xKJRqz5X8g+6nCDUIsDDrcBH609Sg1ovPypp/3aBI78Wl3BLEOXw\n9pbyX40lEsa5WqSN2IryLCIojnxp75VZj2ZkO3LnAoGASsKcFXrT6ZMmOksChJbJ\nLHy+mPXFtmSesdLI1z5cmzT4grFOpwj0DYBt+UKXNxUS4louYOnlqL3BSHFZi1Fy\n/NBTwVF8y6ab+gxN132rtX+Ymw7HqQAAR4h8bDle6sJBAMTnVeE89QsVt5PccYNh\nUjJ0FLrx2jaIz6oAkJDPOJA=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-ve142@tradingview-ta.iam.gserviceaccount.com",
  "client_id": "110504407709270842010",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ve142%40tradingview-ta.iam.gserviceaccount.com"
}


cred = credentials.Certificate(config)
try:
  firebase_admin.initialize_app(cred)
except:
  pass
db = firestore.client()

session = usdt_perpetual.HTTP(
    endpoint='https://api-testnet.bybit.com', 
    api_key='PRolvgqOeFK0hgRX9U',
    api_secret='3pbo67HXceEB1hJ3qjqPFuFtL58sPa4bz54e'
)

itvs = [Interval.INTERVAL_15_MINUTES,Interval.INTERVAL_30_MINUTES,Interval.INTERVAL_1_HOUR,Interval.INTERVAL_4_HOURS,Interval.INTERVAL_1_DAY]


@app.get("/")
async def root():
    #BTC_data = session.latest_information_for_symbol(symbol='BTCUSDT')
    #time = str(datetime.utcfromtimestamp(int(float(BTC_data['time_now']))))
    #price = BTC_data['result'][0]['last_price']
    ts = int(datetime.timestamp(datetime.now()-timedelta(minutes=1)))
    kline = session.query_kline( symbol="BTCUSDT",interval=1,from_time=ts)
    price = kline['result'][0]['close']
    time = str(datetime.fromtimestamp(int(float(kline['time_now']))))

    for i in itvs:
        db.collection(f'BTC{str(i)}').document(time).set({'price': price,'start_timestamp': time}, merge=True)

  #TRADINGVIEW INDICATORS

    for i in itvs:  
        BTC = TA_Handler(symbol="BTCUSDT.P",screener="CRYPTO",exchange="BYBIT",interval=i)

        indicators = {}

        all_indicators = BTC.get_indicators()
        all_indicatorsnot = [
            'Recommend.Other', 'Recommend.All', 'Recommend.MA', 'close', 'open',
            'volume', 'change', 'low', 'high'
        ]

        for k, v in all_indicators.items():
            if (k not in all_indicatorsnot) and (k[-3:] != '[1]') and (k[-3:] != '[2]') and (k[:3] != 'Rec'):
                indicators[k] = v

        for k, v in indicators.items():
            index = list(indicators).index(k)
            if index > 14:
                indicators[k] = float(price) - v

        Pivots = {}
        for k,v in indicators.items():
            if k[:5] == 'Pivot':
                Pivots[k]=v

        moving_averages_ta = {}
        for k,v in indicators.items():
            if (k[:3] == 'EMA')  or (k[:3] == 'SMA') or (k[:3] == 'VWM') or (k[:3] == 'Ich') or (k[:3] == 'Hul'):
                moving_averages_ta[k]=v

        oscillators_ta = {}
        for k,v in indicators.items():
            if (k[:3] != 'EMA')  and (k[:3] != 'SMA') and (k[:3] != 'VWM') and (k[:3] != 'Ich') and (k[:3] != 'Hul') and (k[:5] != 'Pivot'):
                oscillators_ta[k]=v

        #FIRESTORE SET PRICE TIME AND INDICATORS
        db.collection(f'BTC{str(i)}').document(time).set({'moving_averages_ta': moving_averages_ta,'pivots':Pivots,'oscillators_ta':oscillators_ta}, merge=True)
                                                    
        #BNS
        bns_oscillators = {}
        bns_ma = {}
        oscillators = BTC.get_analysis().oscillators
        for k, v in oscillators['COMPUTE'].items():
            bns_oscillators[k] = v

        moving_averages = BTC.get_analysis().moving_averages
        for k, v in moving_averages['COMPUTE'].items():
            bns_ma[k] = v

        db.collection(f'BTC{str(i)}').document(time).set({'oscillators_bns': bns_oscillators,'moving_averages_bns':bns_ma}, merge=True)

    return 'Database Actualizado'



@app.get("/results")
async def root():

    docs = db.collection('BTC1d').get()

    now = datetime.now()
    onehourago = now - timedelta(hours=1)
    onehourago = int(onehourago.timestamp())
    klines = session.query_kline( symbol="BTCUSDT",interval=1,from_time=onehourago)
    klines = klines['result']
    timeframes = ['BTC15m','BTC30m','BTC1h','BTC4h','BTC1d']


    for i in docs:
            if 'result' in i.to_dict():
                pass
            else:
                id = i.id
                price = float(i.to_dict()['price'])
                tp = price *1.01
                sl = price*.99
                for k in klines:
                    if k['high']>=tp:
                        et = str(datetime.utcfromtimestamp(int(float(k['open_time']))))
                        for t in timeframes:
                            db.collection(t).document(id).set({'result':'BUY','end_time':et},merge=True)
                        break
                    elif k['low']<=sl:
                        et = str(datetime.utcfromtimestamp(int(float(k['open_time']))))
                        for t in timeframes:
                            db.collection(t).document(id).set({'result':'SELL','end_time':et},merge=True)
                        break
                    else:
                        pass
                    
    return 'Resultados Actualizados'