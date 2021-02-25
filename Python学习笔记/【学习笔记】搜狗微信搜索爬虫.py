import xlrd
excel = xlrd.open_workbook('C:\\Users\Sogou-SunShijiang\Desktop\贵州党政项目授权信息表.xlsx')
sheet=excel.sheets()[0]
nrows=sheet.nrows
for i in range(nrows):
    print(sheet.row_values(i)[0])
    
print(sheet.col_values(0))