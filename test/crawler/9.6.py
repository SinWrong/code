#特殊:csv传导redis数据库
import redis
import json
import csv
import os

def import_csv_to_redis(csv_file, redis_host='localhost', redis_port=6379,password='123456', redis_db=0, clear_before=False):
    """
    将 CSV 文件中的元数据导入 Redis
    :param csv_file: CSV 文件路径
    :param redis_host: Redis 主机
    :param redis_port: Redis 端口
    :param redis_db: Redis 数据库编号
    :param clear_before: 是否清空之前所有相关数据（慎用）
    """
    if not os.path.exists(csv_file):
        print(f"CSV 文件 {csv_file} 不存在，跳过导入")
        return

    # 连接 Redis
    r = redis.Redis(host=redis_host, port=redis_port,password=password, db=redis_db)
    print(f"已连接 Redis: {redis_host}:{redis_port}/{redis_db}")

    # 如果清空，则删除所有 image: 开头的键（谨慎）
    if clear_before:
        keys = r.keys("image:*")
        if keys:
            r.delete(*keys)
            print(f"清除了 {len(keys)} 个旧记录")

    # 读取 CSV
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"共读取 {len(rows)} 条记录")

    count = 0
    for row in rows:
        keyword = row['keyword']
        filename = row['filename']
        # 构造键名
        key = f"image:{keyword}:{filename}"
        # 将整行数据转为 JSON 字符串
        value = json.dumps(row, ensure_ascii=False)
        # 存储 Hash（也可直接用 set 存储字符串）
        r.set(key, value)          # 简单 key-value 存储
        # 将键名加入集合，便于列举所有记录
        r.sadd("image:all_keys", key)
        count += 1

    print(f"成功导入 {count} 条记录到 Redis")
if __name__ == "__main__":
    import_csv_to_redis("image_metadata.csv", clear_before=False)