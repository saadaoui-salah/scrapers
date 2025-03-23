import jmespath
import scrapy
from core.utils.search import find_emails


class Post(scrapy.Item):
    text = scrapy.Field()
    image = scrapy.Field()

class LinkedInSpider(scrapy.Spider):
    name = "linkedin"
    api_url = "https://www.linkedin.com/voyager/api/graphql?"\
        "variables=(count:10,start:{},moduleKey:ORGANIZATION_MEMBER_FEED_DESKTOP,organizationalPageUrn:urn%3Ali%3Afsd_organizationalPage%3A99450908)&queryId=voyagerFeedDashOrganizationalPageUpdates.18637dddbaa3f548f490aa51105a241b"
    headers = {
        "Host": "www.linkedin.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/vnd.linkedin.normalized+json+2.1",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Li-Lang": "fr_FR",
        "X-Li-Track": '{"clientVersion":"1.13.32076","mpVersion":"1.13.32076","osName":"web","timezoneOffset":1,"timezone":"Africa/Algiers","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1.0909090909090908,"displayWidth":1919.9999999999998,"displayHeight":1080}',
        "X-Li-Page-Instance": "urn:li:page:d_flagship3_profile_view_base_recent_activity_content_view;0vHxsDVoSgOdQHobDUnyBQ==",
        "Csrf-Token": "ajax:8923240780359256773",
        "X-Restli-Protocol-Version": "2.0.0",
        "Referer": "https://www.linkedin.com/in/govardhana-miriyala-kannaiah/recent-activity/all/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers",
    }
    cookies = {
        "JSESSIONID": '"ajax:8923240780359256773"',
        "li_at": "AQEDATDhe-kEX6YEAAABlYMrCTYAAAGVpzeNNk4AZI8BIpUDdRcQDoUQLuF-3cuaVbgarvgHWXEhZDQvIjoieLVTGbGDOsj7uuM55drAUzWPXAf3h0Q0uuqk3UlqU3uRMR0eFTBXoPdC7iYTiWmGuzHp"
    }
    page = 0
    emails = []

    def start_requests(self):
        yield scrapy.Request(url=self.api_url.format(self.page), headers=self.headers, callback=self.parse, cookies=self.cookies)

    def parse(self, response):
        data = response.json()['data']
        posts = filter(lambda x: x.get('metadata', {}).get('actionsPosition','') == 'ACTOR_COMPONENT',response.json()['included'])
        for post in posts:
            text = post['commentary']['text']['text']
            emails = find_emails(text)
            if isinstance(emails, str) and emails not in self.emails:
                yield {
                    'email': emails,
                    'name': post['actor']['name']['text']
                }
                continue
            for email in emails:
                if emails in self.emails:
                    continue
                yield {
                    'email': email,
                    'name': post['actor']['name']['text']
                }

        self.page += 1
        yield scrapy.Request(url=self.api_url.format(self.page), headers=self.headers, callback=self.parse, cookies=self.cookies)

