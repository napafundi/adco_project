from tkinter import *
from datetime import datetime
from tkinter import ttk
import sqlite3
import openpyxl
import os
import string
import collections

def create_excel_inv():
    #Populate inventory_template.xlsx with inventory values and save as
    #new workbook.
    #'inv table': 'total column index'
    inventories = (('raw_materials', 4),
                   ('bottles', 5),
                   ('samples', 5),
                   ('grain', 5),
                   ('barrels', None),
                   ('purchase_orders', 6))
    inventories = collections.OrderedDict(inventories)
    excel_file = (os.getcwd() + "/inventory_files/inventory_template.xlsx")
    wb = openpyxl.load_workbook(excel_file)
    sheets = wb.sheetnames
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    for sheet, (inv, tot_col) in zip(sheets, inventories.items()):
        active_sheet = wb[sheet]
        cur.execute("SELECT * " +
                      "FROM " + inv)
        inv_values = cur.fetchall()
        if len(inv_values) > 0:
            for (indx, row) in enumerate(inv_values, 1):
                try:
                    row = list(row)
                    # Strip $, remove commas
                    row[tot_col] = float(row[tot_col][1:].replace(",",""))
                    tot_col += 1    # Change index for excel column
                    active_sheet.cell(indx, tot_col).number_format = '$#,##0.00'
                except TypeError:
                    pass
                active_sheet.append(row)
            last_row = len(inv_values) + 1
            last_col = len(inv_values[0]) - 1
            last_col = string.ascii_uppercase[last_col]
            tbl_ref = "A1:" + str(last_col) + str(last_row)
            tbl = openpyxl.worksheet.table.Table(displayName=inv, ref=tbl_ref)
            style = openpyxl.worksheet.table.TableStyleInfo(
                name="TableStyleMedium9", showFirstColumn=False,
                showLastColumn=False, showRowStripes=True)
            tbl.tableStyleInfo = style
            active_sheet.add_table(tbl)
    new_excel_file = os.getcwd() + "/inventory_files/inventory_1.xlsx"
    wb.save(new_excel_file)
    os.system('start EXCEL.EXE ' + new_excel_file)


create_excel_inv()
