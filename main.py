# Libs
import requests
from bs4 import BeautifulSoup
import pandas

# Constants
from constants.variables import url, excel

# Get html, check request
def getHTML():
  getHTML = requests.get(url)

  if getHTML.status_code == 200:
    return getHTML
  print('Error with get ' + url)


# Get all items and map them
def getItems():
  htmlData = BeautifulSoup(getHTML().text, features = 'html.parser')
  
  items = htmlData.find_all('section', class_= 'ticket-item')

  parseArrayOfItems = []

  for item in items:
    parseArrayOfItems.append(parseItem(item))


  putToExcel(parseArrayOfItems)


# Parse one item
def parseItem(item):
  title = item.find('div', class_ = "item ticket-title").getText().strip()
  link = item.find('a', class_ = 'address').get('href')
  priceUAH = item.find('span', attrs={"data-currency": "UAH"}).getText() + 'grn'
  priceUSD = item.find('span', attrs={"data-currency": "USD"}).getText() + '$'
  city = item.find('li', class_ = 'view-location').getText()

  return {
    "title": title,
    "link": link,
    "price-UAH(grn)": priceUAH,
    "price-USD($)": priceUSD,
    "city": city
  }

# Get result, convert and put to excel
def putToExcel(result):
  data = pandas.DataFrame(result)
  writer = pandas.ExcelWriter(excel, engine='xlsxwriter')
  data.to_excel(writer, sheet_name = 'Sheet1')
  writer.save()

getItems()
