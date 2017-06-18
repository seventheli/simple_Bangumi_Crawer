from  bs4 import BeautifulSoup

from Crawler import AsySpider


class crawler_for_links(AsySpider):
    def __init__(self, urls, concurrency=10):
        super().__init__(urls=urls, concurrency=concurrency)
        self.items = set()

    def run(self):
        super().run()
        return self.items

    def handle_page(self, html, url):
        soup = BeautifulSoup(html, 'lxml')
        divs = soup.find_all('div', {'class': 'light_odd clearit'})
        for each in divs:
            href = each.find('a')['href']
            print(href + ' found')
            self.items.add(href)
