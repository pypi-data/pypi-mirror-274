# coding:utf-8
import re, pymysql, hashlib, sys, random, requests
from pymysql.converters import escape_string
from loguru import logger
from typing import Union, Dict, List
import json
from sshtunnel import SSHTunnelForwarder
from .translate import translate

class MysqlConn:
    """
    连接Mysql数据库
    """
    def __init__(self, database, config:list = []):
        """
       :param database 数据库名
       :param config 数据库配置[host, port, user, password]
       """
        self.config = config
        self.database = database
        self.cursor = None
        self.db = None
        self.server = None

    def __enter__(self):
        if self.config:
            config = {
                'host': self.config[0],
                'port': self.config[1],
                'user': self.config[2],
                'password': self.config[3],
                'db': self.database,
            }
            # 连接数据库
            self.db = pymysql.connect(**config)
            # 创建游标，用于执行SQL语句
            self.cursor = self.db.cursor()
            logger.info("连接数据库成功。")
            return self
        else:
            with open('c:/mysql_config.json', 'r', encoding='utf-8') as f:
                self.mysql_config=json.load(f)
            try:
                self.server = SSHTunnelForwarder(
                    ssh_address_or_host=eval(self.mysql_config["2"]['ssh_address_or_host']),
                    ssh_username='root',
                    ssh_password=self.mysql_config["2"]['ssh_password'],
                    remote_bind_address=eval(self.mysql_config["2"]['remote_bind_address'])
                )
                # 启动隧道服务
                self.server.start()
                self.db = pymysql.connect(host='127.0.0.1', port=self.server.local_bind_port, user=self.mysql_config["2"]['user'],
                                     password=self.mysql_config["2"]['passwd'], database= self.database)
                self.cursor = self.db.cursor()
                logger.success("成功连接到MySQL数据库")
            except Exception as e:
                logger.error(f"连接失败: {translate(str(e))}")
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
        if self.server:
            self.server.close()
        logger.info(f'已断开与MySQL数据库的连接')

    def insert(self, table_name, data_pass: Union[dict, List[dict]]):
        """  mysql插入数据
        :param table_name 表名
        :param data_pass 参数接收字典/列表[字典] 格式
        """
        if not data_pass or not self.cursor:
            logger.error(f'数据列表为空或连接未建立')
            return
        try:
            if isinstance(data_pass, list):
                keys = set().union(*data_pass)
                columns = ', '.join(keys) # 构建SQL语句中的列名部分
                placeholders = ', '.join(['%s'] * len(keys))
                sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                params = [[item.get(key) for key in keys] for item in data_pass]

                if self.cursor.executemany(sql, params):
                    self.db.commit()
                logger.success(f"{self.cursor.rowcount} 条记录插入成功")

            elif isinstance(data_pass, dict):
                keys = ','.join(data_pass.keys())
                values = ','.join(['%s'] * len(data_pass))
                query = 'INSERT INTO {table}({keys}) VALUES({values})'.format(table=table_name, keys=keys, values=values)
                if self.cursor.execute(query, tuple(data_pass.values())):
                    self.db.commit()
                logger.success(f"{self.cursor.rowcount} 条记录插入成功")

        except Exception as e:
            logger.error(f"插入数据时发生错误: {translate(str(e))}")

class PyMySQL:
    def __init__(self, host: str = 'localhost', port=3306, user: str = 'root', password: str = '', database: str = '',
                 auto_add_key=False):
        """
        :param host: 默认本地地址
        :param user: 默认root
        :param password: 数据库密码
        :param database: 数据库
        :param auto_add_key: 自动添加字段默认False
        """
        self.db = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
        logger.info(f'已连接数据库：host={host}, user={user}, password={password}, database={database}')
        self.cursor = self.db.cursor()
        self.hk = []
        self.auto_add_key = auto_add_key

    # 插入数据库
    def insert_into(self, database=None, fields=[], values=[], update_fields={}, SQL=False):
        """
        :param database: 数据表名
        :param fields: 字段名列表
        :param values: 值列表
        :param update_fields: 更新字段字典
        :param SQL: 输出mysql插入语句
        :return: 插入数据库
        """
        self.db.ping()
        if self.auto_add_key:
            if not self.hk:
                self.hk = self.getdatah(database)
            for field in fields:
                if field not in self.hk:
                    self.cursor.execute(f"""ALTER TABLE `{database}` ADD COLUMN `{field}` varchar(255) NULL;""")
                    self.hk.append(field)
        fields_format = ','.join([f'`{field}`' for field in fields])
        values_format = ('"'+'","'.join([escape_string(str(value)) for value in values])+'"').replace('"None"','null')
        fields_update_format = ','.join([f'{key}="{escape_string(value)}"' for key, value in update_fields.items()])
        sql = f"""
            INSERT INTO `{database}`
            ({fields_format})
            VALUES ("{values_format}")
            """
        # if not fields:
        #     sql = f"""
        #         INSERT INTO {database}
        #         VALUES ("{values_format}")
        #         """
        if update_fields:
            sql = f"""
                INSERT INTO `{database}`
                VALUES ({values_format})
                ON DUPLICATE KEY UPDATE
                {fields_update_format}
                """
            if fields:
                sql = f"""
                    INSERT INTO `{database}`
                    ({fields_format})
                    VALUES ({values_format})
                    ON DUPLICATE KEY UPDATE
                    {fields_update_format}
                    """
        else:
            sql = f"""
                INSERT INTO `{database}`
                VALUES ({values_format})
                """
            if fields:
                sql = f"""
                    INSERT INTO `{database}`
                    ({fields_format})
                    VALUES ({values_format})
                    """
        if SQL:
            logger.info(sql)
        VALUES = re.search('VALUES \((.*)\)', sql).group(1)[:250]
        try:
            self.cursor.execute(sql)
            self.db.commit()
            logger.info(VALUES + '\t成功加入数据库！')
        except Exception as e:
            if str(e).startswith('(1062, "Duplicate entry'):
                logger.info(VALUES + '\t数据重复!')
            else:
                self.except_handl(e, sql)
        self.db.rollback()

    # 自定义sql语句
    def custom_sql(self, sql,wrap=''):
        """
        :param sql: 自定义sql语句
        :return: 执行自定义sql语句
        """
        self.db.ping()
        if wrap!='':
            try:
                for s in sql.split(wrap):
                    self.cursor.execute(s.strip())
                    logger.info(s.strip())
                self.db.commit()
            except Exception as e:
                logger.error(str(e) + sql)
                self.db.rollback()
        else:
            try:
                self.cursor.execute(sql)
                self.db.commit()
                logger.info(sql)
            except Exception as e:
                logger.error(str(e) + sql)
                self.db.rollback()

    # 查询数据
    def select(self, sql, fetch='all'):
        """
        :param sql: 查询数据sql
        :return: 查询结果
        """
        self.db.ping()
        self.cursor.execute(sql)
        logger.info(sql)
        if fetch == 'one':
            return self.cursor.fetchone()
        return self.cursor.fetchall()

    # 转义字符格式化
    def escape_string(self, character_string):
        """
        :param character_string: 部分文本中字符影响SQL语句，需要做字符串格式化处理
        :return: 处理好的字符串
        """
        self.db.ping()
        if type(character_string)==str:
            return escape_string(character_string)
        return character_string

    # 获取表头字段
    def getdatah(self, database: str = ''):
        """
        :return: 获取表头字段
        """
        self.db.ping()
        if database != "":
            return [k[0] for k in self.select(
                f"""SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME = '{database}' ORDER BY ORDINAL_POSITION ASC;""")]
        return [a[0] for a in self.cursor.description]

    # 关闭数据库
    def close(self):
        """
        :return: 关闭数据库的所有操作
        """
        self.db.ping()
        self.cursor.close()
        self.db.close()
        logger.info('数据库连接已断开！')

    def except_handl(self, e, sql):
        logger.error(q)
        logger.error(translate(str(e)))
        logger.error(sql)
        sys.exit()