#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author ChenOT
@desc 
@date 2021/4/1
"""
# import pyodbc
import pypyodbc

if __name__ == "__main__":
    tables = ['Content']
    print(len(tables))

    for table in tables:
        # mdb = 'Driver={Microsoft Access Driver (*.mdb)};DBQ=E:\\DICT_DATA\\294\\SpiderResult.mdb'
        mdb = 'Driver={SQL Server};DBQ=E:\\DICT_DATA\\294\\SpiderResult.mdb'
        conn = pypyodbc.win_connect_mdb(mdb)
        cur = conn.cursor()
        sql = "SELECT * FROM " + table
        print(sql)
        cur.execute(sql)
        alldata = cur.fetchall()
        total_rows = len(alldata)
        total_cols = len(alldata[0])
        print("****************Begin to process\"表:%s\"****************" % table)
        print("\"表:%s\"总行数 = %d" % (table, total_rows))
        print("\"表:%s\"总列数 = %d" % (table, total_cols))
        #
        # for row in range(0, total_rows):
        #

        conn.close()
    print("****************所有表处理完毕****************")
