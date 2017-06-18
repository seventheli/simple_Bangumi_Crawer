from  bs4 import BeautifulSoup

from Crawler import AsySpider


class crawler_for_names(AsySpider):
    def __init__(self, urls, concurrency=10, **kwargs):
        super().__init__(urls=urls, concurrency=concurrency)
        self.items = {}
        try:
            self.staff = kwargs.get('staff')
        except:
            self.staff = False

    def run(self):
        super().run()
        return self.items

    def handle_page(self, html, url):
        soup = BeautifulSoup(html, 'lxml')
        h1 = soup.find('h1', {'class': 'nameSingle'})
        try:
            CN_name = h1.find('a')['title']
            JP_name = h1.find('a').text
            if CN_name and CN_name != JP_name:
                if self.staff:
                    staffs = soup.find('ul', {'class':'browserList'}).find_all('span', {'class': 'badge_job'})
                    all_staffs = []
                    for each in staffs:
                        all_staffs.append(each.text)
                    for each in all_staffs:
                        if each in self.staff:
                            self.items[JP_name] = CN_name
                            print('saved %s' % url)
                            break
                        else:
                            if each == all_staffs[-1]:
                                print('skipped %s' % url)
                else:
                    self.items[JP_name] = CN_name
                print('saved %s' % url)
        except:
            print('error found in %s' % url)