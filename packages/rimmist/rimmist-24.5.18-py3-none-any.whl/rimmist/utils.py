


#
import contextlib
import json
import sqlite3
from typing import Union

import bsddb3  # 6.2.9 + 5.3.27
import pandas as pd  # 1.4.3



#
class BerkeleyDB(object):
    ''''''


    #
    @staticmethod
    def f_write(df: pd.DataFrame, key_name: str, lst_value_name: list[str], path_name: str, table_name: str) -> None:
        '''
        check df[lst_value_name].dtypes are all string in advance?
        '''
        db = bsddb3.db.DB()
        db.open(path_name, table_name, bsddb3.db.DB_HASH, bsddb3.db.DB_CREATE)
        for key, value in zip(df[key_name], df[lst_value_name].values.tolist()):
            db.put(key.encode(), json.dumps(value).encode())
        db.close()

        return None


    #
    @staticmethod
    def f_read(path_name: str, table_name: str) -> list[pd.DataFrame]:
        '''
        read fully not partially
        '''
        db = bsddb3.db.DB()
        db.open(path_name, table_name, bsddb3.db.DB_HASH, bsddb3.db.DB_RDONLY)
        df = pd.DataFrame(db.items(), columns=['key_name', 'json'])
        db.close()

        df.key_name = df.key_name.str.decode('utf-8')
        df.json = df.json.map(json.loads)
        if isinstance(df.json[0], dict):
            return [df, pd.json_normalize(df.json)]
        else:
            return [df, pd.DataFrame(df.json.to_list())]
        


#
class SQLite3(object):
    ''''''


    #
    @staticmethod
    def f_write(df: pd.DataFrame, path_name: str, table_name: Union[int, str]) -> None:
        ''''''
        with contextlib.closing(sqlite3.connect(path_name, check_same_thread=False)) as con:
            df.to_sql(
                table_name,
                con,
                if_exists='replace',
                index=False,
                chunksize=1_000,
                method='multi'
            )

        return None


    #
    @staticmethod
    def f_read(path_name: str, table_name: Union[int, str]) -> pd.DataFrame:
        ''''''
        with contextlib.closing(sqlite3.connect(path_name, check_same_thread=False)) as con:
            df = pd.read_sql(f'select * from "{table_name}";', con)

        return df


    #
    @staticmethod
    def f_check(path_name: str) -> list[tuple[str]]:
        '''
        check all table_name stored in single sqlite3 file
        '''
        with contextlib.closing(sqlite3.connect(path_name, check_same_thread=False)) as con:
            with contextlib.closing(con.cursor()) as cur:
                cur.execute('select name from sqlite_master;')
                output = cur.fetchall()

        return output


