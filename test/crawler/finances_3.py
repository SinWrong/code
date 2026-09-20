import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ccxt
import pandas as pd
import pandas_ta as ta
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')
# ============ 修复中文显示 ============
plt.rcParams['font.sans-serif'] = ['SimHei']      #  Windows 常用黑体
# 如果 SimHei 无效，可尝试 'Microsoft YaHei' 或 'Arial Unicode MS'（Mac）
plt.rcParams['axes.unicode_minus'] = False         # 解决负号显示为方块
# ============ 配置参数 ============
SYMBOL = 'BTC/USDT'  # 交易对
TIMEFRAME = '1m'  # K线周期（1分钟）
LIMIT = 1000  # 显示最近60根K线
REFRESH_INTERVAL = 3000  # 刷新间隔（毫秒），这里设为5秒

# 初始化交易所（使用币安公开数据，无需API Key）
exchange = ccxt.okx()

# 创建画布（2行1列：上图为价格，下图为RSI）
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
fig.suptitle(f'{SYMBOL} 实时行情 + RSI(6,12)', fontsize=16)


def animate(frame):
    """每一帧执行的更新函数"""
    try:
        # 1. 获取K线数据
        ohlcv = exchange.fetch_ohlcv(SYMBOL, TIMEFRAME, limit=LIMIT)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        # 2. 计算RSI
        df['rsi_6'] = ta.rsi(df['close'], length=6)
        df['rsi_12'] = ta.rsi(df['close'], length=12)

        # 3. 清空旧图表（重绘方式，简单直观）
        ax1.clear()
        ax2.clear()

        # -------- 上图：价格走势 --------
        ax1.plot(df.index, df['close'], color='black', linewidth=1.5, label='价格')
        ax1.set_title(f'最新价: {df["close"].iloc[-1]:.2f}  (更新于 {datetime.now().strftime("%H:%M:%S")})')
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)

        # -------- 下图：RSI（6日+12日） --------
        # 6日线：亮红色（#DC143C），加粗
        ax2.plot(df.index, df['rsi_6'], color='#DC143C', linewidth=2, label='RSI6')
        # 12日线：标准蓝色，虚线辅助区分
        ax2.plot(df.index, df['rsi_12'], color='#1f77b4', linewidth=2, linestyle='--', label='RSI12')

        # 水平参考线
        ax2.axhline(y=50, color='gray', linestyle='-', linewidth=1, alpha=0.6)  # 多空分界
        ax2.axhline(y=70, color='orange', linestyle=':', linewidth=1, alpha=0.5)  # 超买
        ax2.axhline(y=30, color='green', linestyle=':', linewidth=1, alpha=0.5)  # 超卖

        # 填充超买超卖区域（柔和背景）
        ax2.axhspan(70, 100, facecolor='red', alpha=0.05)
        ax2.axhspan(0, 30, facecolor='green', alpha=0.05)

        ax2.set_ylim(0, 100)
        ax2.set_title('RSI (红色=6日敏感线, 蓝色=12日趋势线)')
        ax2.legend(loc='upper left')
        ax2.grid(True, alpha=0.3)

        # 显示最新RSI数值在右上角（可选）
        latest_6 = df['rsi_6'].iloc[-1]
        latest_12 = df['rsi_12'].iloc[-1]
        ax2.text(0.98, 0.95, f'RSI6: {latest_6:.2f}  RSI12: {latest_12:.2f}',
                 transform=ax2.transAxes, ha='right', va='top',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # 自动调整X轴日期显示
        fig.autofmt_xdate()

    except Exception as e:
        print(f"更新出错: {e}")


# 启动动画（interval单位是毫秒）
ani = animation.FuncAnimation(fig, animate, interval=REFRESH_INTERVAL)

plt.tight_layout()
plt.show()