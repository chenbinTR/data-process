#!/usr/bin/env python
# -*- conding: utf-8 -*-
import pyodbc
import xlrd


def find_in_excel(path, word):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows  # excel总行数
    ncols = table.ncols  # excel总列数
    # print(nrows,ncols)
    for r in range(nrows):
        for c in range(ncols):
            cell = table.cell(r, c).value
            if (isinstance(cell, float) or isinstance(cell, int)):
                cell = str(int(cell))
            if (cell == u"旧编码"):
                old_code_col = c
            elif (cell == u"新编码"):
                new_code_col = c
            elif (cell == word):
                print("cell = %s" % cell)
                if (old_code_col == c):
                    new_code = table.cell(r, c + 1).value
                    if (isinstance(new_code, float) or isinstance(new_code, int)):
                        new_code = str(int(new_code))
                    return (0, new_code)  # 若是旧编码，则直接返回新编码
                elif (new_code_col == c):
                    # print("new_code_col = %d" %new_code_col)
                    return (1, cell)  # 若是新编码，则返回新编码
    return (-1, -1)


if __name__ == "__main__":
    tables = ['BJT',
              'Capacity', 'Connector', 'Diode', 'ForBOM',
              'IC', 'Inductor', 'Mechanical', 'MOSFET',
              'NoPartNumber', 'Other', 'Resistor']
    tables = ['Table_BJT', 'Table_Capacitor']
    print(len(tables))

    for table in tables:
        mdb = 'Driver={Microsoft Access Driver (*.mdb,*.accdb)};DBQ=C:\\Users\\liyua\\Desktop\\1.mdb'
        conn = pyodbc.win_connect_mdb(mdb)
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

        for row in range(0, total_rows):
            sql = "SELECT [Part Number] FROM " + table  # 带空格时必须用[]包括
            cur = conn.cursor()
            cur.execute(sql)

            Part_Numbers = cur.fetchall()
            PartNumber = Part_Numbers[row][0]

            if (isinstance(PartNumber, float) or isinstance(PartNumber, int)):
                PartNumber = str(int(PartNumber))

            result = find_in_excel(r"C:\Users\liyua\Desktop\1.xlsx", PartNumber)
            if (result[0] == 0):
                print("\"表:%s\"中%s为旧编码,对应的新编码为:%s" % (table, PartNumber, result[1]))
                sql = "Update [" + table + "] Set [Part Number] = '" + result[
                    1] + "' where " + "[Part Number]" + " = " + "'" + PartNumber + "'"
                print(sql)
                cur.execute(sql)
                conn.commit()
                cur.close()

            elif (result[0] == 1):
                print("error！%s已经为新编码" % result[1])
                continue
            elif (result[0] == (-1)):
                print("warning！未在excel中找到\"表:%s\"中的编码：%s" % (table, PartNumber))
                continue

        print("****************End processing\"表:%s\"****************" % table)
        conn.close()
    print("****************所有表处理完毕****************")