import openpyxl

filename = 'stat_104102.xlsx'
book = openpyxl.load_workbook(filename)
sheet = book.worksheets[0]

data = []
for row in sheet.rows:
    data.append([
        row[0].value,
        row[9].value
    ])

del data[0:4]
del data[len(data)-2:]

data = sorted(data, key=lambda x: int(x[1].replace(',', '')))

for i, a in enumerate(data):
    if i >= 5:
        break
    print(i+1, a[0], a[1])
