from docx import Document
import os

cwd = os.getcwd()
file = open(cwd + '/production_sheets/Mash_Log-converted.docx', 'rb')
document = Document(file)

info_table = document.tables[0]
grain_table = document.tables[1]
print(info_table)
print(grain_table)

for (row,info) in zip(info_table.rows,["date","type","mash #"]):
    for cell in row.cells:
        for paragraph in cell.paragraphs:
            paragraph.text = info

for (row,gr_list) in zip(grain_table.rows,[["corn","500","16167"],["rye","200","16167"],["malt","125","1100"]]):
    for (cell,num) in zip(row.cells,range(3)):
        for para in cell.paragraphs:
            para.text = gr_list[num]

document.save(cwd + "/production_sheets/Mash_Log_1.docx")
