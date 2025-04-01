import scrapy


class BocaratonchamberSpider(scrapy.Spider):
    name = "bocaratonchamber"
    allowed_domains = ["bocaratonchamber.com"]
    start_urls = ["https://web.bocaratonchamber.com/allcategories"]

    def parse(self, response):
        cats = response.css('.ListingCategories_AllCategories_CATEGORY > a::attr(href)').getall()
        for cat in cats:
            yield scrapy.Request(
                url=f"https://web.bocaratonchamber.com{cat}",
                callback=self.parse_categories,
            )

    def parse_categories(self, response):
        if links := response.css('.ListingResults_All_ENTRYTITLELEFTBOX a::attr(href)').getall():
            for link in links:
                yield scrapy.Request(
                    url=f"https://web.bocaratonchamber.com{link}",
                    callback=self.parse_categories,
                )   
        else: 
            yield from self.parse_details(response)

    def parse_details(self, response):
        facebook = response.xpath('//img[@src="/external/wccontrols/v12/socialmedia/images/32/Facebook.png"]/../@href').get('')
        facebook = facebook.removeprefix('/external/wcpages/referral.aspx?URL=')
        linkedin = response.xpath('//img[@src="/external/wccontrols/v12/socialmedia/images/32/LinkedIn.png"]/../@href').get('')
        linkedin = facebook.removeprefix('/external/wcpages/referral.aspx?URL=')
        instagram = response.xpath('//img[@src="/external/wccontrols/v12/socialmedia/images/32/Instagram.png"]/../@href').get('')
        instagram = facebook.removeprefix('/external/wcpages/referral.aspx?URL=')
        phone_number = ' '.join(response.xpath('//span[@class="ListingDetails_Level3_MAINCONTACT"]/text()').getall())
        all_numbers = phone_number.split('|')
        extra = None
        if len(all_numbers) > 1:
            phone_number = all_numbers[0]
            extra = '|'.join(all_numbers[1:])
        full_name = response.xpath('//img[@src="/external/wcpages/images/maincontact.gif"]/following-sibling::*[1]/text()').get()
        first_name, last_name = None, None
        if full_name:
            full_name = full_name.split(' ')
            first_name, last_name = full_name[0], ''.join(full_name[1:])
        yield {
            'company_name':response.css('[property="og:title"]::attr(content)').get(),
            'phone_number':phone_number,
            'extra_phone_numbers':extra,
            'address':response.css('[property="business:contact_data:street_address"]::attr(content)').get(),
            'city':response.css('[itemprop="locality"]::text').get(),
            'state':response.css('[itemprop="region"]::text').get(),
            'zip_code':response.css('[property="business:contact_data:postal_code"]::attr(content)').get(),
            'website':response.css('.ListingDetails_Level3_SITELINK::attr(href)').get(),
            'first_name':first_name,
            'last_name':last_name,
            'industry':response.xpath("//div[contains(@class, 'ListingDetails_Level')]/a").getall()[-1],
            'facebook':facebook,
            'instagram':instagram,
            'linkedin':linkedin,
        }
