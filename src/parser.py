from bs4 import BeautifulSoup
from pandas import ExcelWriter, DataFrame
from requests import get

from constants.constants import excel, url


# Get html, check request
def get_html():
    get_html_data = get(url)

    if get_html_data.status_code == 200:
        return get_html_data
    print('Error with get ' + url)


# Get all items and map them
def get_items():
    html_data = BeautifulSoup(get_html().text, features='html.parser')

    items = html_data.find_all('section', class_='ticket-item')

    parse_array_of_items = []

    for item in items:
        parse_array_of_items.append(parse_item(item))

    put_to_excel(parse_array_of_items)


# Parse one item
def parse_item(item):
    title = item.find('div', class_="item ticket-title").getText().strip()
    link = item.find('a', class_='address').get('href')
    price_uah = item.find('span', attrs={"data-currency": "UAH"}).getText() + 'grn'
    price_usd = item.find('span', attrs={"data-currency": "USD"}).getText() + '$'
    city = item.find('li', class_='view-location').getText()

    return {
        "title": title,
        "link": link,
        "price-UAH(grn)": price_uah,
        "price-USD($)": price_usd,
        "city": city
    }


# Get result, convert and put to excel
def put_to_excel(result):
    data = DataFrame(result)
    writer = ExcelWriter(excel, engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Sheet1')
    writer.save()


get_items()
