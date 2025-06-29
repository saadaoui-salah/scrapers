import scrapy
from core.utils.utils import read_glob_files, fake_request
from core.utils.cleaning import clean
from furl import furl
from requests import get


class ClutchSpider(scrapy.Spider):
    name = "clutch"
    files = read_glob_files('clutsh/*.html')

    def start_requests(self):
        yield fake_request(callback=self.parse)


    def parse(self, response):
        pro = []
        for res in self.files:
            for item in res.css('#providers__list .provider-list-item'):
                profile = f"https://clutch.co{item.css('.provider__cta-container a:nth-child(1)::attr(href)').get()}"
                website = item.css('.provider__cta-container a:nth-child(2)::attr(href)').get()
                if website:
                    f = furl(website)
                    website = f.args['u']
                else:
                    pid = item.css('[name="bookmark"]::attr(data-provider-id)').get()
                    website = f"https://r.clutch.co/redirect?event_category=visit_website&page_type=profile&pid={pid}"

                try:
                    real = get(website, allow_redirects=False).headers.get('location') or website
                except:
                    real = website

                if profile not in pro:
                    yield {
                        'name': clean(item.css('.provider__title-link::text').get()),
                        'profile': profile,
                        'website': real,
                        'hourly rate': clean(item.xpath('.//div[@data-tooltip-content="<i>Avg. hourly rate</i>"]/text()[2]').get('')),
                        'employees': clean(item.xpath('.//div[@data-tooltip-content="<i>Employees</i>"]/text()[2]').get('')),
                        'client budget': clean(item.xpath('.//div[@data-tooltip-content="<i>Min. project size</i>"]/text()[2]').get('')),
                        'location': clean(item.xpath('.//div[@data-tooltip-content="<i>Location</i>"]/text()[2]').get('')),
                    }
                    pro += [profile]




 