import pyupbit
import numpy as np


##################################################################################################

coin = "KRW-BTC"

# OHLCV(open, high, low, close, volume) 당일 시가. 고가, 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv(coin, "day")

# 범위값 k
k = 0.7

##################################################################################################3




# 변동성 돌파 기준 범위 계산, (고가 - 저가) * k 값
df['range'] = (df['high'] - df['low']) * k

# target(매수가), range 컬럼을 한 칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

# 매수, 매도시 수수료 0.05% + 임의의 슬리피지 발생 + 0.02%
fee = 0.0012

# ror(수익률), np.where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
# 누적 곱 계산(cumprod) => 누적 수익률
df['hpr'] = df['ror'].cumprod()

# Draw Down(하락폭) 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

#MDD 계산 
print("MDD(%): ", df['dd'].max())

#엑셀로 출력
df.to_excel("backtest_result.xlsx")