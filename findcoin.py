import pyupbit
import numpy as py

def get_hpr(ticker):
    try:

        df = pyupbit.get_ohlcv(ticker)
        df = df['2019']

        # 변동성 돌파 기준 범위 계산, (고가 - 저가) * k 값
        df['range'] = (df['high'] - df['low']) * 0.1

        # target(매수가), range 컬럼을 한 칸씩 밑으로 내림(.shift(1))
        df['target'] = df['open'] + df['range'].shift(1)


        fee = 0.0012
        # ror(수익률), np.where(조건문, 참일때 값, 거짓일때 값)
        df['ror'] = np.where(df['high'] > df['target'],
                            df['close'] / df['target'] - fee,
                            1)
        # 누적 곱 계산(cumprod) => 누적 수익률
        df['hpr'] = df['ror'].cumprod()

        # Draw Down(하락폭) 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
        df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
        return df['hpr'][-2]
    except:
        return 1

tickers = pyupbit.get_tickers()

hprs = []
for ticker in tickers:
    hpr = get_hpr(ticker)
    hprs.append((ticker, hpr))

sorted_hprs = sorted(hprs, key=lambda x:x[1], reverse=True)
print(sorted_hprs[:5])