import sqlite3
from datetime import datetime
path = 'data/main.db'


def select(table_name, columns='*', where=''):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    if where:
        where= 'WHERE ' + where
    c.execute(f"SELECT {columns} FROM {table_name} {where}")
    return c.fetchall()


def insert(table_name, *args):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    q = '?,' * len(args)
    sql_query = f"INSERT INTO {table_name} VALUES ({q[:-1]})"
    c.execute(sql_query, args)
    conn.commit()
    conn.close()


def update(table_name, where, **kwargs):
    conn = sqlite3.connect(path)
    c = conn.cursor()

    edits = ''
    new_data = ()
    for key in kwargs:
        edits += f" {key} = ?,"
        new_data += (kwargs[key],)

    if not where:
        return 'WHERE kiritilmadi, bu yaxshilikka olib kelmasligi mumkin'

    where= 'WHERE ' + where

    sql_query = f"UPDATE {table_name} SET {edits[:-1]} {where}"
    c.execute(sql_query, new_data)
    conn.commit()
    conn.close()


def delete(table_name, where):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f'DELETE FROM {table_name} WHERE {where}')
    conn.commit()


def add_user(user_id, first_name, last_name, username=None, telephone=None, joined_at=datetime.now()):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT * FROM accounts_botuser WHERE user_id = {user_id}")
    if not c.fetchone():
        sql_query = f"INSERT INTO accounts_botuser VALUES (?,?,?,?,?,?)"
        new_data = (user_id, first_name, last_name, username, telephone, joined_at)
        c.execute(sql_query, new_data)
        conn.commit()
    conn.close()




# update(table_name='accounts_botuser', first_name='Jamshidbek', where='user_id = 1036600398')
