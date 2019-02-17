import openpyxl

wb = openpyxl.load_workbook('purchase_orders/blank_po.xlsm')
print(type(wb))

print(wb.get_sheet_names())

sheet = wb.get_sheet_by_name('Purchase Order')

sheet['A17'].value = "Hello"

print(sheet['A17'].value)
