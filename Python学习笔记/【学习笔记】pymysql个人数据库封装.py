import pymysql

DB_CONF = {
    'host': '42.193.126.153',
    'port': 3307,
    'user': 'root',
    'password': '123456',
    'db': 'ssjmysql',
    'charset': 'utf8'
}

class DB():
    def __init__(self,db_conf=DB_CONF):
        self.conn=pymysql.connect(**db_conf, autocommit=True)
        self.cur=self.conn.cursor(pymysql.cursors.DictCursor)


    def query(self,tb,*awgs):
        sql=f"select {','.join(awgs)} from {tb};"
        self.cur.execute(sql)
        data=self.cur.fetchall()
        print(f'查询语句：{sql}，查询结果：{data}')
        return data


    def update(self,sql):
        result=self.cur.execute(sql)
        print(f'更新语句：{sql}，影响行数：{result}')


    def deltable(self,tb):
        sql=f'drop table {tb};'
        result=self.cur.execute(sql)
        print(f'删除语句：{sql}，影响行数：{result}')


    def close(self):
        print("关闭数据库连接")
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    a=DB()
    sql1="""
    create table demotable(
        id INT(11),
        name VARCHAR(40) NOT NULL,
        age INT(11) NOT NULL,
        borndate DATE);
    """
    sql2="""
    insert into demotable(id,name,age,borndate) values(3,'小花',31,'1996-09-01');
    """

    sql3='select * from demotable where ;'

    a.update(sql2)
    a.query('demotable','*')
    a.deltable('demotable')
    a.close()

