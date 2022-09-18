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

fixed = {}
variable = {}

for date in fixedDates:
  index = fixedDates.index(date)
  convertedDate = datetime.fromtimestamp(date/1000)
  
  print('LENGTH:', len(fixedDates))
  print('DATE:', convertedDate, 'INDEX:', index)
