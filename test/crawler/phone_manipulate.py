import uiautomator2 as u2
import time

# 连接手机
from pytz import reference

d = u2.connect()

# 1. 录屏功能
# 开始录制，默认帧率为20
d.screenrecord('test.mp4') [reference:10]

# 执行你的自动化操作
d.click(500, 1000) # 点击
time.sleep(2)
d.swipe(100, 500, 900, 500) # 滑动

# 停止录制
# 注意：uiautomator2的screenrecord需要在with语句或手动停止
# 更推荐的方式是：
d.screenrecord.stop()

# 2. 定时执行 (例如：5分钟后执行)
print("等待5分钟...")
time.sleep(300)
print("开始执行任务...")
# ... 你的录屏和操作代码 ...