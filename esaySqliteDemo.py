from __init__ import EasySqlite

initSql = '''
    DROP TABLE IF EXISTS "main"."grade";
    CREATE TABLE "grade" (
    "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "stu_id"  INTEGER,
    "math"  INTEGER,
    "english"  INTEGER,
    "chinese"  TEXT
    );
    DROP TABLE IF EXISTS "main"."stu";
    CREATE TABLE "stu" (
    "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name"  TEXT,
    "age"  INTEGER,
    "sex"  INTEGER
    );
'''
# 连接数据
db = EasySqlite('test.db')

# 1 执行建表语句--A 传入要运行的sql语句1
# res = db.execm(initSql)
# 1.1 执行建表语句--B 直接运行sql脚本文件
# res = db.execSqlScript('createSQL.sql')
# --------------------------------------

# 2 插入数据
# res1 = db.table('stu').insert({'name': '狗蛋', 'age': 18, 'sex': 1})
# print(db.lastSql)  # INSERT INTO stu ("name","age","sex") VALUES ("狗蛋","18","1")

# res2 = db.insert({'name': '李狗蛋', 'age': 19, 'sex': 1})
# print(db.lastSql)  # INSERT INTO stu ("name","age","sex") VALUES ("李狗蛋","19","1")

# 2.2 批量插入
# insertData = [
#     {'name': "王花花", 'age': 16, 'sex': 2},
#     {'name': "小明", 'age': 17, 'sex': 1},
#     {'name': "小丽", 'age': 17, 'sex': 2},
# ]
# res3 = db.table('stu').insertAll(insertData)
# db.commit()
# --------------------------------------------------

# # 3 查询数据 链式操作
# res = db.table('stu').select()  # SELECT * FROM stu WHERE 1
# res1 = db.where('id>3').select()  # SELECT * FROM stu WHERE id>3
# res2 = db.where(['id>3', 'sex=1']).select()  # SELECT * FROM stu WHERE id>3 AND sex=1
# res3 = db.where('sex=1').field(['name', 'age']).select()  # SELECT name,age FROM stu WHERE sex=1
# res4 = db.field(['name', 'age']).limit(5).select()  # SELECT name,age FROM stu WHERE sex=1 LIMIT 5
# res5 = db.where('sex=2').field(['name', 'age']).find()  # SELECT name,age FROM stu WHERE sex=2 LIMIT 1
# res6 = db.where(1).field(['name', 'age']).limit(5).order('age ASC').select()  # SELECT name,age FROM stu WHERE 1 ORDER BY age ASC LIMIT 5
# # 如果不切换数据名【使用table()方法】sql拼接会有缓存
# res7 = db.select()  # SELECT name,age FROM stu WHERE 1 ORDER BY age ASC LIMIT 5
# # clear()方法用于清除sql缓存，但是必须放在链式操作的链首
# res8 = db.clear().select()  # SELECT * FROM stu WHERE 1
# res9 = db.table('stu').where('id=5').value('name')  # SELECT name FROM stu WHERE id=5 LIMIT 1

# 4 修改数据
# res = db.table('stu').where('id=4').update({'name': '王小明', 'age': 19})  # UPDATE stu SET "name"="王小明", "age"="19" WHERE (id=4)
# db.commit()

# 5 删除数据
# res = db.table('stu').where('id=3').delete()  # DELETE FROM stu WHERE (id=3)
# db.commit()
