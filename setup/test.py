import os, re, openpyxl
import pandas as pd
from datetime import datetime

# iterate through all csv files in a directory
PATHDIR = os.path.join(os.path.dirname(__file__), 'data')

FILES = os.listdir(PATHDIR)
f = '/Users/yellowheart/Desktop/Byte/baseball/setup/data/mlb_odds_2010.xlsx'

def find_yr_string(fn):
    match = re.search(r'(\d{4})', fn).group(1)
    return int(match)

def convert_date(num, yr):
    if type(num) == str:
        return num
    num = str(num)
    try:
        if len(num) == 3:
            date = datetime(year=yr, month=int(num[0:1]), day=int(num[2:4]))
            return date
        elif len(num) == 4:
            date = datetime(year=yr, month=int(num[0:2]), day=int(num[2:4]))
            return date
    except ValueError:
        pass

wb = openpyxl.load_workbook(f)
ws = wb.active
year = find_yr_string(f)
for cell in ws['A']:
    cell.value = convert_date(cell.value, year)

wb.save('/Users/yellowheart/Desktop/Byte/baseball/setup/data/mlb_odds_2010_test.xlsx')



# for i in FILES:
#     with open(i) as f:
#         pass
# data = pd.ExcelFile(f)

# # print(data.parse(sheet_name='Sheet1', skiprows=0).head(10))
# df = data.parse(sheet_name='Sheet1', skiprows=0)
# print(df.info())










# df = pd.read_excel(f)



# ['Date', 'Rot', 'VH', 'Team', 'Pitcher', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', 'Final', 'Open', 'Close', 'Open OU', 'Unnamed: 18', 'Close OU', 'Unnamed: 20']





