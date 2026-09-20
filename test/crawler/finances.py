import ccxt
import pandas as pd
import pandas_ta as ta
from datetime import datetime

# ============ 1. 连接交易所 ============
# 以币安为例，换成 OKX、火币等只需修改 exchange = ccxt.okx() 或 ccxt.huobi()
exchange = ccxt.okx()

symbol = 'BTC/USDT'      # 交易对
timeframe = '1h'         # K线周期：1m, 5m, 15m, 1h, 4h, 1d 等
limit = 10000              # 获取多少根K线（至少需要30根以上）

# ============ 2. 获取K线数据 ============
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

# ============ 3. 计算RSI（6日和12日） ============
df['rsi_6'] = ta.rsi(df['close'], length=6)    # 6日RSI
df['rsi_12'] = ta.rsi(df['close'], length=12)  # 12日RSI

# ============ 4. 查看最新值 ============
latest_rsi_6 = df['rsi_6'].iloc[-1]
latest_rsi_12 = df['rsi_12'].iloc[-1]

print(f"最新RSI6: {latest_rsi_6:.2f}")
print(f"最新RSI12: {latest_rsi_12:.2f}")
print(f"RSI6 - RSI12 差值: {latest_rsi_6 - latest_rsi_12:.2f}")

# ============ 5. （可选）绘制图表 ============
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# 上图为价格
ax1.plot(df.index, df['close'], label='Close Price', color='black')
ax1.set_title(f'{symbol} Price')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 下图为RSI（两条线）
ax2.plot(df.index, df['rsi_6'], label='RSI6', color='red', linewidth=1.5)
ax2.plot(df.index, df['rsi_12'], label='RSI12', color='blue', linewidth=1.5)
ax2.axhline(y=50, color='green', linestyle='--', alpha=0.7)   # 50水平线
ax2.axhline(y=70, color='gray', linestyle=':', alpha=0.5)    # 超买线
ax2.axhline(y=30, color='gray', linestyle=':', alpha=0.5)    # 超卖线
ax2.set_title('RSI (6 + 12)')
ax2.legend()
ax2.set_ylim(0, 100)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()