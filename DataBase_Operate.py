# 用以处理数据库

import mysql.connector
import mysql.connector.errors as DB_EXC
import logging

from datetime import date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def Fuc_make_cxn_cursor(db_name, db_user_name):
    '''
    :param db_name:
    :param db_user_name:
    :return: cxn or None
    '''
    global cxn

    try:
        cxn = mysql.connector.Connect(
            **{'database': db_name, 'user': db_user_name, 'password': '123QQ123qq', 'charset': 'utf8', })
        print('成功连上数据库')
        cur = cxn.cursor()
        return cur
    except DB_EXC.InterfaceError as e:
        logger.info('连接数据库出问题了%s', e)


def create_table(cur, table_name):
    try:
        cur.execute(
            "CREATE TABLE %s (star_name_1 VARCHAR(200), star_name_2 VARCHAR(200), star_name_3 VARCHAR(200), star_name_4 VARCHAR(200), star_English_Name VARCHAR(200), age_group VARCHAR(200), star_rank VARCHAR(100), time_created DATETIME, time_last_update DATETIME) CHARSET=utf8" % table_name)  # TODO
    except DB_EXC.Error as e:
        logger.info('create_table:  %s', e)


def drop_table(cur, table_name):
    try:
        cur.execute("DROP TABLE %s" % table_name)
    except DB_EXC.Error as e:
        logger.info("drop _table 出问题 %s", e)


def insert_into_table(cur, data):
    try:
        cur.executemany("INSERT INTO TestModel_stars(star_name_1, time_created, time_last_update) VALUES (%s, %s, %s)", data)
    except DB_EXC.Error as e:
        logger.info("数据无法插入表中%s", e)
    except:
        logger.info('insert_into_table :DB未曾捕捉的错误')


def delete_from_table(cur, table_name, key_word, value_of_key_word):    # TODO 这里需要写一个批量处理的方法比较好
    try:
        str_a = "DELETE FROM %s WHERE %s = ('%s')" %(table_name, key_word, value_of_key_word)
        cur.execute("%s" %(str_a))
    except DB_EXC as e:
        logger.info('delete: %s', e)


def update_table(cur, table_name, key_word, value_of_key_word, new_value_of_key_word):
    try:
        cur.execute("UPDATE %s SET %s = %s WHERE %s = ('%s')" % (table_name, key_word, new_value_of_key_word, key_word, value_of_key_word))
    except DB_EXC.OperationalError as e:
        logger.info('更新数据有问题: %s', e)
    except:
        logger.info('update_table: DB未曾捕捉的错误')


def select_from_table(cur, table_name, key_word, value_of_key_word, key_word_to_select='*'):
    try:
        cur.execute("SELECT %s FROM %s WHERE %s = ('%s')" % (key_word_to_select, table_name, key_word, value_of_key_word))
    except DB_EXC.OperationalError as e:
        logger.info('select模块出问题了: %s', e)
    except:
        logger.info('select_from_table: DB未曾捕捉的错误')


def main():
    db_name = 'ADP_dataBase'
    db_user_name = 'root'
    table_name = 'TestModel_stars'
    data = [('mm', date.today(), date.today())]

    cur_a = Fuc_make_cxn_cursor(db_name, db_user_name)
    # create_table(cur_a, table_name)
    # print("成功创造表")

    insert_into_table(cur_a, data)
    print('插入完成')

    # delete_from_table(cur_a, table_name, "age", 22)
    # print('删除完成')

    # update_table(cur_a, table_name, "age", '22',  '26')
    # print("删除完成")
    #
    #
    # select_from_table(cur_a, table_name, "name", "HELLO")
    # for name, age, level in cur_a:
    #     print(name, age, level)

    cxn.commit()
    cxn.close()

if __name__ == '__main__':
    main()
