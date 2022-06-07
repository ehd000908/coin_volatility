import pyupbit
import time
import datetime

access = "xHYYr6HSk8sJq9ZiLYXCYIpxQHLJGkOvxM4XmqsJ"          
secret = "NVV5Wtdfi20gRG1snftDgPFLKz9Z6JpZjgxiROm6"          
upbit = pyupbit.Upbit(access, secret)

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

now = datetime.datetime.now()
start_time = get_start_time("KRW-BTC")
end_time = start_time + datetime.timedelta(days=1)

print(start_time)
print(end_time)
print(end_time - datetime.timedelta(seconds=10))
print(now)