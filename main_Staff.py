import json
import re

import requests
from bs4 import BeautifulSoup

from Crawler_all_links import crawler_for_links
from Crawler_all_names import crawler_for_names

running_pages = int(input('Enter a integer to show how many pages read in the same time: \n'))
default_page = requests.get('http://bangumi.tv/person?type=3').content.decode('utf8')
soup = BeautifulSoup(default_page, 'lxml')
total_page = soup.find('span', {'class': 'p_edge'})
total_page = int(re.search('\d+', re.search('/.+?\d+', total_page.prettify()).group(0)).group(0))
url = 'http://bangumi.tv/person?type=3&page={page}'
pages = []
for i in range(1, total_page + 1):
    url_to_search = url.format(page=i)
    pages.append(url_to_search)
crawler_1 = crawler_for_links(urls=pages, concurrency=running_pages)
items = crawler_1.run()
total_href = set()
for each in items:
    total_href.add('http://bangumi.tv' + each)
print('total %s found' % str(len(total_href)))
with open('staff input.txt', 'r', encoding='utf8') as f:
    staff = f.read().split('、')
crawler_2 = crawler_for_names(urls=total_href, concurrency=running_pages, staff=staff)
items = crawler_2.run()
group = []
text = ''
for each in items:
    text += (each + ':' + items[each] + ',')
    value = {
        "name": "",
        "urls": [],
        "substitutions": [
            {
                "input": each,
                "inputType": "text",
                "output": items[each],
                "caseSensitive": False
            }
        ],
        "html": "none",
        "enabled": True
    }
    group.append(value)
result = {
    'version': '0.15',
    "group": group
}

with open('result.json', 'w', encoding='utf8') as f:
    json.dump(result, f, ensure_ascii=False)

with open('result.text', 'w', encoding='utf8') as f:
    f.write(text)