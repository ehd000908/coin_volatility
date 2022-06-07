import time
import pyupbit
import datetime

# 업비트 로그인 키
access = "xHYYr6HSk8sJq9ZiLYXCYIpxQHLJGkOvxM4XmqsJ"
secret = "NVV5Wtdfi20gRG1snftDgPFLKz9Z6JpZjgxiROm6"


# 함수 목록
#########################################################################################


# 변동성 돌파 전략으로 매수 목표가 조회
def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

# 시작 시간 조회
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


# 잔고 조회
def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

# 현재가 조회
def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


#########################################################################################


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")



# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-CHZ")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=60):
            target_price = get_target_price("KRW-", 0.1) # 매수목표가 설정
            current_price = get_current_price("KRW-DOGE") # 현재가

            if target_price < current_price:
                krw = get_balance("KRW")
                upbit.buy_market_order("KRW-DOGE", krw*0.9995)

        elif now > end_time - datetime.timedelta(seconds=60):
            doge = get_balance("DOGE")
            
            if doge > 0:
                upbit.sell_market_order("KRW-DOGE", doge*0.9995)
                
        time.sleep(1)



    except Exception as e:
        print(e)
        time.sleep(1)