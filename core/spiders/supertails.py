import scrapy
from furl import furl
from w3lib.html import remove_tags
import json
from uuid import uuid4


class SupertailsSpider(scrapy.Spider):
    name = "supertails"
    start_urls = ["https://supertails.com"]
    proxy = 'burp'

    def parse(self, response):
        cats = response.css('[data-parent="health-hygiene3"], [data-parent="clothing-accessories3"], [data-parent="collars-leashes-harnesses3"], [data-parent="grooming3"], [data-parent="dog-toys3"], [data-parent="treats-chews_image_https-cdn-shopify-com-s-files-1-0565-8021-0861-files-product_food_dog_mob_1_f58957c7-fd44-4533-abf6-fb2533ca2bd0-png-v-16446432063"], [data-parent="dog-food_image_-https-cdn-shopify-com-s-files-1-0565-8021-0861-files-product_food_dog_mob_1_f58957c7-fd44-4533-abf6-fb2533ca2bd0-png-v-16446432063"]')
        for cat in cats:
            for cat2 in cat.css('ul > li a'):
                slug = cat2.css('::attr(href)').get().split('/collections/')[-1].split('?')[0]
                url = f'https://search.unbxd.io/78960c876fcf6b023ecb00405dac2866/ss-unbxd-prod-supertails43231684495044/category?p=category_handle_uFilter%3A%22{slug}%22&facet.multiselect=true&variants=true&variants.count=100&fields=compareAtPrice,price,computed_discount,availableForSaleOfVariants,uniqueId,productUrl,productType,totalInventory,title,availability,variantCount,imageUrl,tags,images,meta_display_label,v_price,v_computed_discount,v_compareAtPrice,v_availableForSale,v_weight,v_Size,v_imageUrl,v_weightUnit,variantId,vendor,vId,v_sku,skuId,meta_offer1,meta_offer2,meta_rating,meta_rating_count,meta_category,meta_sub_category,meta_pet_type,meta_category_l4,meta_category_l5,meta_app_only_product,meta_video_highlight,meta_sizechart_image&spellcheck=true&pagetype=boolean&rows=40&start=0&version=V2&viewType=Grid&facet.version=V2'
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_products
                )

        for slug in ['puppy-corner', 'dog-medicines']:
            url = f'https://search.unbxd.io/78960c876fcf6b023ecb00405dac2866/ss-unbxd-prod-supertails43231684495044/category?p=category_handle_uFilter%3A%22{slug}%22&facet.multiselect=true&variants=true&variants.count=100&fields=compareAtPrice,price,computed_discount,availableForSaleOfVariants,uniqueId,productUrl,productType,totalInventory,title,availability,variantCount,imageUrl,tags,images,meta_display_label,v_price,v_computed_discount,v_compareAtPrice,v_availableForSale,v_weight,v_Size,v_imageUrl,v_weightUnit,variantId,vendor,vId,v_sku,skuId,meta_offer1,meta_offer2,meta_rating,meta_rating_count,meta_category,meta_sub_category,meta_pet_type,meta_category_l4,meta_category_l5,meta_app_only_product,meta_video_highlight,meta_sizechart_image&spellcheck=true&pagetype=boolean&rows=40&start=0&version=V2&viewType=Grid&facet.version=V2'
            yield scrapy.Request(
                url=url,
                callback=self.parse_products
            )

    def parse_products(self, response):
        data = response.json()['response']
        for product in data['products']:
            for variant in product['variants']:
                url =f"https://supertails.com{variant['productUrl']}.json"
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_pdp
                )
        if data['numberOfProducts']  > data['start']:
            url = furl(response.url)
            url.args['start'] = int(url.args['start']) + 40
            yield scrapy.Request(
                url=url.url,
                callback=self.parse_products
            )
            

    def parse_pdp(self, response):
        product = response.json()['product']
        html = scrapy.Selector(text=product['body_html'])
        images = False
        for variant in product['variants']:
            ingredients = html.xpath("//p/*[contains(text(),'ngredients:')]/../following-sibling::*[1]//text()").getall()
            item = {
                'id':str(uuid4()),
                'title': product['title'],
                'weight/quantity': variant['title'],
                'url': f"{response.url.replace('.json','')}?variant={variant['id']}",
                'images': [image['src'] for image in product['images']],
                'ingredients': ' '.join(ingredients)
            }
            if not images:
                images = True
                for image in item['images']:
                    yield scrapy.Request(
                        url=image,
                        callback=self.parse_images,
                        meta={'item': item}
                    )
                    
            description = remove_tags(product['body_html'])
            for ing in ingredients:
                description.replace(ing,'')

            item['description'] = description
            
            yield scrapy.Request(
                url=response.url.replace('.json',''),
                callback=self.parse_details,
                meta={'item': item}
            )

    def parse_details(self, response):
        item = response.meta['item']
        script = response.xpath('//script[contains(text(), "(rawData && rawData.trim()) {")]/text()').get()
        data = script.split("const rawData = '")[1].split("';")[0]
        try:
            data = json.loads(data)
            for feat in data:
                item[feat['key']] = feat['value']
            yield item
        except:
            yield item



    def parse_images(self, response):
        item = response.meta['item']
        file_name = f"{item['id']}&{item['title'].replace(' ', '_')}"
        with open(f'./supertails-images/{file_name}.png', 'wb') as f:
            f.write(response.body)