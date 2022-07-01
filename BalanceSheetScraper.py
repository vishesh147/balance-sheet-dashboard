from ast import arg
import pandas as pd
import numpy as np
import requests
import os
import xlrd
from bs4 import BeautifulSoup

header = {'User-Agent': 'Mozilla/5.0'}

companyName = "Reliance Industries"
url = 'https://www.investing.com/equities/reliance-industries' + '-balance-sheet'

page = requests.get(url, headers=header)
soup = BeautifulSoup(page.content, "html.parser")
buttonTag = soup.find('a', class_='newBtn toggleButton LightGray')
attrData = buttonTag.attrs
#attrData

dataUrl = "https://www.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=" + attrData['data-pid'] + "&report_type="+ attrData['data-rtype'] + "&period_type=" + attrData['data-ptype']
#dataUrl

balSheetHtml = requests.get(dataUrl, headers=header)
df = pd.read_html(balSheetHtml.text)
raw_data = df.pop(0)

Header = raw_data.iloc[-1].tolist()
for i in range(1, len(Header)):
    Header[i] = Header[i][0:4] + "/" + Header[i][4:]

for d in df:
    d.columns = Header
    d[Header[1:]] = d[Header[1:]].apply(pd.to_numeric, errors='coerce')
    d.fillna(0, inplace=True)

balanceSheet = {
    "currAssets": df[0],
    "nonCurrAssets": df[1],
    "currLiabilities": df[2],
    "nonCurrLiabilities": df[3],
    "equity": df[4],
}

# Total Current Assets
totalCurrAssets = balanceSheet["currAssets"].iloc[[0, 4, 6, 7, 8]].sum().to_frame().T
totalCurrAssets.at[0, 'Period Ending:'] = "Total Current Assets"
balanceSheet["currAssets"] = pd.concat([balanceSheet["currAssets"], totalCurrAssets])

# Total Non-Current Assets
totalNonCurrAssets = balanceSheet["nonCurrAssets"].iloc[[0, 3, 4, 5, 6, 7, 8]].sum().to_frame().T
totalNonCurrAssets.at[0, 'Period Ending:'] = "Total Non-Current Assets"
balanceSheet["nonCurrAssets"] = pd.concat([balanceSheet["nonCurrAssets"], totalNonCurrAssets])

# Total Current Liabilities
totalCurrLiabilities = balanceSheet["currLiabilities"].iloc[0:].sum().to_frame().T
totalCurrLiabilities.at[0, 'Period Ending:'] = "Total Current Liabilities"
balanceSheet["currLiabilities"] = pd.concat([balanceSheet["currLiabilities"], totalCurrLiabilities])

# Total Current Liabilities
totalNonCurrLiabilities = balanceSheet["nonCurrLiabilities"].iloc[[0, 3, 4, 5]].sum().to_frame().T
totalNonCurrLiabilities.at[0, 'Period Ending:'] = "Total Non-Current Liabilities"
balanceSheet["nonCurrLiabilities"] = pd.concat([balanceSheet["nonCurrLiabilities"], totalNonCurrLiabilities])

# Total Equity
totalEquity = balanceSheet["equity"].iloc[0:].sum().to_frame().T
totalEquity.at[0, 'Period Ending:'] = "Total Equity"
balanceSheet["equity"] = pd.concat([balanceSheet["equity"], totalEquity])

# Create important Dataframes

totalAssets = totalCurrAssets.add(totalNonCurrAssets, fill_value=0)
totalAssets.at[0, 'Period Ending:'] = "Total Assets"

totalLiabilities = totalCurrLiabilities.add(totalNonCurrLiabilities, fill_value=0)
totalLiabilities.at[0, 'Period Ending:'] = "Total Liabilities"

totalLiabilitiesEquity = totalLiabilities.add(totalEquity, fill_value=0)
totalLiabilitiesEquity.at[0, 'Period Ending:'] = "Total Liabilities & Equity"

totals = pd.concat([totalAssets, totalLiabilities, totalLiabilitiesEquity], ignore_index=True)
balanceSheet["totals"] = totals

BalanceSheet = pd.DataFrame()
for tdf in balanceSheet.values():
    x = tdf.transpose()
    newheader = x.iloc[0]
    x = x[1:]
    x.columns = newheader
    x.reset_index(drop=True, inplace=True)
    x.columns.name = 'Index'
    BalanceSheet = pd.concat([BalanceSheet, x], axis=1)
year = [y[:4] for y in raw_data.iloc[-1].tolist()[1::]]
BalanceSheet.insert(0, "Year", year)

BalanceSheet = BalanceSheet.loc[::-1].reset_index(drop=True)


BalanceSheet['Working Capital'] = [i-j for i, j in 
    zip(BalanceSheet['Total Current Assets'].to_list(), BalanceSheet['Total Current Liabilities'].to_list())]

# ------- Solvency Ratios ---------

# Current Ratio
BalanceSheet['Current Ratio'] = [i/j for i, j in 
    zip(BalanceSheet["Total Current Assets"].to_list(), BalanceSheet["Total Current Liabilities"].to_list())] 

# Quick Ratio
BalanceSheet['Quick Assets'] = [(ca - i - pe) for ca, i, pe in 
    zip(
        BalanceSheet["Total Current Assets"].to_list(), 
        BalanceSheet["Total Inventory"].to_list(), 
        BalanceSheet["Prepaid Expenses"].to_list(),
    )]
BalanceSheet['Quick Ratio'] = [(qa/cl) for qa, cl in 
    zip(
        BalanceSheet["Quick Assets"].to_list(), 
        BalanceSheet["Total Current Liabilities"].to_list(),
    )]



# ------- Leverage Ratios ---------

# Debt-to-Equity Ratio
BalanceSheet['DE Ratio'] = [i/j for i, j in 
    zip(BalanceSheet['Total Long Term Debt'].to_list(), BalanceSheet['Total Equity'].to_list())]

# Debt-to-Assets Ratio
BalanceSheet['DA Ratio'] = [i/j for i, j in 
    zip(BalanceSheet['Total Long Term Debt'].to_list(), BalanceSheet['Total Assets'].to_list())]

# Debt-to-Capital Ratio
BalanceSheet['DC Ratio'] = [i/(j+i) for i, j in 
    zip(BalanceSheet['Total Long Term Debt'].to_list(), BalanceSheet['Total Equity'].to_list())]
