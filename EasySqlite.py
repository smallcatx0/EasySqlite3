class EasySqlite:
    """sqlite数据库操作工具类
    """
    _connection = None  # sqlite 连接句柄
    _cursor = None     # sqlite 操作数据游程
    jointSql = {   # 传入的sql片段
        'field': '*'
    }
    errorMsg = ''  # 错误信息
    lastSql = ''   # 最后一条sql
    lastId = None
    def __init__(self, database):
        '''sqlite数据库操作工具类

        @param database [str] 数据库地址
        @author Tan<smallcatx0@gmail.com>
        '''
        import sqlite3
        self._connection = sqlite3.connect(database)
        self._cursor = self._connection.cursor()

    def exec(self, sql):
        '''执行一条sql语句

        @param sql [str]
        @author Tan<smallcatx0@gmail.com>
        '''
        self.lastSql = sql
        try:
            self._cursor.execute(sql)
        except Exception as e:
            self.errorMsg = e
            return False
        return self._cursor

    def execm(self, sql):
        '''执行多条sql语句（建表、备份）

        @param sql [str] sql语句
        @author Tan<smallcatx0@gmail.com>
        '''
        self.lastSql = sql
        try:
            self._cursor.executescript(sql)
        except Exception as e:
            self.errorMsg = e
            return False
        return self._cursor

    def execSqlScript(self, sqlPath):
        '''执行sql脚本文件

        @param filePath [str] sql脚本文件的位置
        @author Tan<smallcatx0@gmail.com>
        '''
        with open(sqlPath, 'r', encoding='utf-8') as fp:
            sqlCon = fp.read()
        return self.execm(sqlCon)

    def table(self, table):
        '''切换要操作的数据表表

        @param table [str] 表名
        @author Tan<smallcatx0@gmail.com>
        '''
        self.jointSql = {}  # 切换表就清除sql拼接缓存
        self.jointSql['field'] = '*'
        self.jointSql['table'] = table
        return self

    def where(self, wh, rel='AND'):
        '''sql语句where条件

        @param wh  [str|list] sql语句的where条件支持原生字符串或者数组
        @param rel [str] 连接符，默认为 and
        @author Tan<smallcatx0@gmail.com>
        '''
        if isinstance(wh, (str, int)):
            self.jointSql['where'] = wh
        else:
            rel = " %s " % rel
            self.jointSql['where'] = rel.join(wh)
        return self

    def field(self, fields):
        '''选择查询字段

        @param fields [str|list] 选择查询字段支持原生字符串或者数组
        @author Tan<smallcatx0@gmail.com>
        '''
        if isinstance(fields, str):
            self.jointSql['field'] = fields
        else:
            self.jointSql['field'] = ','.join(fields)
        return self

    def limit(self, limit, offset=0):
        '''选择查询字段

        @param fields [str|list] 选择查询字段支持原生字符串或者数组
        @param offset [int] 偏移量
        @author Tan<smallcatx0@gmail.com>
        '''
        self.jointSql['limit'] = limit
        if offset != 0:
            self.jointSql['offset'] = offset
        return self

    def order(self, order):
        '''排序

        @param order [str] 排序字段
        @author Tan<smallcatx0@gmail.com>
        '''
        self.jointSql['order'] = order
        return self

    def _select_sql(self):
        '''拼接查询语句 私有方法
        @return [str] 拼接的sql语句
        '''
        fields = self.jointSql['field']
        if 'table' not in self.jointSql:
            self.errorMsg = "There is No table!"
            return False
        else:
            table = self.jointSql['table']
        if 'where' not in self.jointSql:
            where = '1'
        else:
            where = self.jointSql['where']
        sql = "SELECT %s FROM %s WHERE %s " % (fields, table, where)
        if 'order' in self.jointSql:
            sql += "ORDER BY %s " % self.jointSql['order']
        if 'limit' in self.jointSql:
            sql += "LIMIT %d " % self.jointSql['limit']
        if 'offset' in self.jointSql:
            sql += "OFFSET %d " % self.jointSql['offset']
        return sql

    def select(self, fetchSql=False):
        '''查询语句

        @param fetchSql [bool] 只返回拼接的sql 不运行
        @return [tuple|bool] 成功返回查询的结果，失败返回False
        @author Tan<smallcatx0@gmail.com>
        '''
        sql = self._select_sql()
        res = self.exec(sql)
        if res:
            if fetchSql:
                return self.lastSql
            return res.fetchall()
        else:
            return False

    def find(self):
        '''查询一条结果

        @return [tuple|bool] 成功返回查询的结果，失败返回False
        @author Tan<smallcatx0@gmail.com>
        '''
        self.jointSql['limit'] = 1
        sql = self._select_sql()
        res = self.exec(sql)
        if res:
            data = res.fetchone()
            return data
        else:
            return False

    def value(self, field):
        '''获取一个字段的值
        @param field [str] 字段名
        @return [int|str|bool] 成功返回查询的结果，失败返回False
        @author Tan<smallcatx0@gmail.com>
        '''
        self.jointSql['limit'] = 1
        self.jointSql['field'] = field
        res = self.find()
        if res:
            return res[0]
        else:
            return False

    def insert(self, data):
        '''插入一条数据
        @param data [dict] 新增的数据 字典格式 k：字段名 v：插入的值
        @return [int] 此条数据的id
        @author Tan<smallcatx0@gmail.com>
        '''
        if 'table' not in self.jointSql:
            self.errorMsg = 'There is no Table!'
            return False
        sql = "INSERT INTO %s " % self.jointSql['table']
        tmpK = '('
        tmpV = '('
        for one in data:
            tmpK += '"%s",' % one
            tmpV += '"%s",' % str(data[one])
        tmpK = tmpK[:-1] + ')'
        tmpV = tmpV[:-1] + ')'
        sql += tmpK + ' VALUES ' + tmpV
        res = self.exec(sql)
        if res:
            self.lastId = res.lastrowid
            return self.lastId
        else:
            return False

    def getLastId(self):
        return self.lastId
        
    def insertAll(self, data):
        '''插入多条数据

        @param data [list] 新增的数据
        @return [int] 最后一个数据的id
        @author Tan<smallcatx0@gmail.com>
        '''
        for one in data:
            res = self.insert(one)
            if res is False:
                return False
        return self

    def update(self, data):
        '''更新操作

        @param data [dict] 更新的数据k-v格式
        @author Tan<smallcatx0@gmail.com>
        '''
        if 'table' not in self.jointSql:
            self.errorMsg = 'There is no Table!'
            return False
        if 'where' not in self.jointSql:
            self.errorMsg = '更新操作必须指定条件'
            return False
        sql = "UPDATE %s " % self.jointSql['table']
        setSql = 'SET'
        for one in data:
            setSql += ' "%s"="%s",' % (one, data[one])
        setSql = setSql[:-1]
        sql += setSql + " WHERE (%s)" % self.jointSql['where']
        res = self.exec(sql)
        if res:
            return self
        else:
            return False

    def delete(self):
        '''删除操作 必须搭配where条件

        @author Tan<smallcatx0@gmail.com>
        '''
        if 'where' not in self.jointSql:
            self.errorMsg = '删除操作必须指定条件'
            return False
        if 'table' not in self.jointSql:
            self.errorMsg = 'There is no Table!'
            return False
        sql = 'DELETE FROM %s WHERE (%s)' % (self.jointSql['table'], self.jointSql['where'])
        res = self.exec(sql)
        if res:
            return self
        else:
            return False

    def count(self):
        '''聚合函数 统计结果集数据量
        @return [int|bool] 成功返回数量 失败返回False
        @author Tan<smallcatx0@gmail.com>
        '''
        if 'table' not in self.jointSql:
            self.errorMsg = '没有表名可不行'
            return False
        if 'where' not in self.jointSql:
            where = '1'
        else:
            where = self.jointSql['where']
        sql = "SELECT COUNT(*) FROM %s WHERE %s" % (self.jointSql['table'], where)
        res = self.exec(sql)
        if res:
            return res.fetchone()[0]
        else:
            return False

    def clear(self):
        '''清除上次sql拼接的缓存
        '''
        oldJointSql = self.jointSql
        self.jointSql = {   # 传入的sql片段
            'field': '*'
        }
        if 'table' in oldJointSql:
            self.jointSql['table'] = oldJointSql['table']

        return self

    def commit(self):
        '''提交事务
        '''
        self._connection.commit()

    def close(self):
        '''关闭连接
        '''
        self._cursor.close()
        self._connection.close()

    def __del__(self):
        self.close()


if __name__ == '__main__':
    pass
