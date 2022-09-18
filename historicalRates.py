from requests import get
from functools import reduce
from csv import writer
from datetime import datetime
import json


fixedResponse = get(
    'https://www.ratehub.ca/api/charts?callback=rh.Chart.jsonpDispatch&id=Chart_9EXxi&series=boc.5y-fixed-posted')
variableResponse = get(
    'https://www.ratehub.ca/api/charts?callback=rh.Chart.jsonpDispatch&id=Chart_zAHkl&series=best.5y-variable')

fixedData = json.loads(fixedResponse.text[23:-2])
variableData = json.loads(variableResponse.text[23:-2])

fixedDates = fixedData['date']
variableDates = variableData['date']

fixedRate = fixedData['boc-5y-fixed-posted']
variableRate = variableData['best-5y-variable']

rates = {}


# with open('rates.csv', 'w') as csv_file:
#   csv_writer = writer(csv_file)
#   headers = ['Date', 'Fixed', 'Variable']
#   csv_writer.writerow(headers)

for fixDate in fixedDates:
    fixedIndex = fixedDates.index(fixDate)
    convertFixDate = datetime.fromtimestamp(fixDate/1000).strftime('%Y-%m')
    if convertFixDate not in rates:
        rates[convertFixDate] = {'fixed': fixedRate[fixedIndex - 1]}
    elif 'fixed' not in rates[convertFixDate]:
        rates[convertFixDate]['fixed'] = fixedRate[fixedIndex - 1]
    else:
        rates[convertFixDate]['fixed'] = (
            rates[convertFixDate]['fixed'] + fixedRate[fixedIndex - 1]) / 2

for varDate in variableDates:
    varIndex = variableDates.index(varDate)
    convertVarDate = datetime.fromtimestamp(varDate/1000).strftime('%Y-%m')

    if convertVarDate not in rates:
        rates[convertVarDate] = {'variable': variableRate[varIndex - 1]}
    elif 'variable' not in rates[convertVarDate]:
        rates[convertVarDate]['variable'] = variableRate[varIndex - 1]
    else:
        rates[convertVarDate]['variable'] = (
            rates[convertVarDate]['variable'] + variableRate[varIndex - 1]) / 2


print(rates)
