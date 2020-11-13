# Libs
import requests

# Constants
from constants.variables import url, html, excel

getHTML = requests.get(url)

with open(html, 'w') as output_html:
  output_html.write(getHTML.text)

