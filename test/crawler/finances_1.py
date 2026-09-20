import ccxt
import pandas as pd
import pandas_ta as ta
import time
import logging

# ============ 配置 ============
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1m'  # 1分钟K线
LIMIT = 30  # 获取30根K线（足够计算12日RSI）
INTERVAL = 60  # 每60秒更新一次

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# ============ 连接交易所 ============
exchange = ccxt.binance({
    'sandbox': True,  # 测试环境，正式交易改为 False
})


def fetch_and_calculate_rsi():
    """获取最新K线，计算6日和12日RSI"""
    # 获取K线数据
    ohlcv = exchange.fetch_ohlcv(SYMBOL, TIMEFRAME, limit=LIMIT)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    # 计算RSI
    df['rsi_6'] = ta.rsi(df['close'], length=6)
    df['rsi_12'] = ta.rsi(df['close'], length=12)

    # 最新值
    latest_rsi_6 = df['rsi_6'].iloc[-1]
    latest_rsi_12 = df['rsi_12'].iloc[-1]

    return latest_rsi_6, latest_rsi_12


# ============ 主循环：实时更新 ============
print(f"开始监控 {SYMBOL}，每 {INTERVAL} 秒更新一次...\n")

while True:
    try:
        rsi_6, rsi_12 = fetch_and_calculate_rsi()
        logging.info(f"RSI6: {rsi_6:.2f} | RSI12: {rsi_12:.2f} | 差值: {rsi_6 - rsi_12:.2f}")

        # 在这里可以加入交易逻辑，例如：
        # if rsi_6 < 30 and rsi_12 < 30: print("超卖信号！")
        # elif rsi_6 > 70 and rsi_12 > 70: print("超买信号！")

    except Exception as e:
        logging.error(f"错误: {e}")

    time.sleep(INTERVAL)  # 等待60秒后再次执行