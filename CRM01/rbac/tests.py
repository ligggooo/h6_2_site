from django.test import TestCase

# Create your tests here.


# spider
from bs4 import BeautifulSoup
import requests

url = 'http://fontawesome.dashgame.com/'

# res = requests.get(url)
# with open('data','w',encoding='utf-8') as f:
#     f.write(res.text)
with open('data', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

lis = soup.select('div.fontawesome-icon-list')[1].select('i')

ICON = []
for li in lis:
    cls = li.attrs['class']
    for c in cls:
        if c != 'fa':
            ICON.append(c)
            print("['%s', '<i class=\"fa %s\" aria-hidden=\"true\"></i>'],"%(c,c))




