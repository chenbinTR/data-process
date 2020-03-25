# -*- coding: UTF-8 -*-

import MySQLdb


member_id = ""

member_ids = member_id.split("|")

for m in member_ids:
    print(m)

# 打开数据库连接
db = MySQLdb.connect(host="common.backend.mysql.tulingapi.com", port=3308, user="turing_platform", passwd="laQ8MWHFnbIx8zxY", db="turing_platform", charset='utf8')

sql = "select * from tl_robot where member=244407"

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute(sql)

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()
# while data is not None:
print("Database version : %s " % data)

# 关闭数据库连接
db.close()