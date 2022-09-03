import math
import pandas as pd

data = pd.read_csv('./dataset.csv')
data.drop(['지점', '지점명'], axis=1, inplace=True)

height = int(input('산의 고도를 입력하세요: '))

print('\n일시\t\t\t기온\t이슬점\t상승응결고도\t가능성')

for idx, row in data.iterrows():
    datetime = row[0]
    temp = row[1]
    dewp = row[2]
    lcl = math.floor(125 * (temp - dewp))
    
    psblt = ''

    if lcl <= height:
        psblt = '🟢 높음'
    else:
        psblt = '🔴 낮음'

    print(f'{datetime}\t{temp}\t{dewp}\t{lcl}\t\t{psblt}')