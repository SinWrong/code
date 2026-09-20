import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ccxt
import pandas as pd
import pandas_ta as ta
from datetime import datetime

SYMBOL = 'BTC/USDT'
TIMEFRAME = '1m'
LIMIT = 60
exchange = ccxt.binance()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# ---------- 预创建空白线条（先画空数据） ----------
line_price, = ax1.plot([], [], color='black', linewidth=1.5, label='价格')
line_rsi6, = ax2.plot([], [], color='#DC143C', linewidth=2, label='RSI6')
line_rsi12, = ax2.plot([], [], color='#1f77b4', linewidth=2, linestyle='--', label='RSI12')

# 预先画好水平参考线（只画一次，不用每帧重画）
ax2.axhline(y=50, color='gray', linestyle='-', alpha=0.6)
ax2.axhline(y=70, color='orange', linestyle=':', alpha=0.5)
ax2.axhline(y=30, color='green', linestyle=':', alpha=0.5)
ax2.set_ylim(0, 100)
ax1.grid(True, alpha=0.3)
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper left')


def init():
    """初始化空白"""
    line_price.set_data([], [])
    line_rsi6.set_data([], [])
    line_rsi12.set_data([], [])
    return line_price, line_rsi6, line_rsi12


def update(frame):
    """更新帧"""
    ohlcv = exchange.fetch_ohlcv(SYMBOL, TIMEFRAME, limit=LIMIT)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'o', 'h', 'l', 'c', 'v'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    df['rsi6'] = ta.rsi(df['c'], length=6)
    df['rsi12'] = ta.rsi(df['c'], length=12)

    # 更新线条数据
    x_vals = df.index
    line_price.set_data(x_vals, df['c'])
    line_rsi6.set_data(x_vals, df['rsi6'])
    line_rsi12.set_data(x_vals, df['rsi12'])

    # 动态调整X轴范围（显示最新数据）
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view(scaley=False)  # 只自动调整X轴，Y轴固定0~100

    # 更新图表标题（显示最新价格和时间）
    ax1.set_title(f'最新价: {df["c"].iloc[-1]:.2f}  更新时间: {datetime.now().strftime("%H:%M:%S")}')

    return line_price, line_rsi6, line_rsi12


ani = animation.FuncAnimation(fig, update, init_func=init, interval=5000, blit=True)
plt.tight_layout()
plt.show()