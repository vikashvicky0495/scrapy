import scrapy


class internship(scrapy.Spider):
    name = 'winchester'
    allowed_domains = ['https://www.midsouthshooterssupply.com/']
    start_urls = [
        'https://www.midsouthshooterssupply.com/dept/reloading/primers/']

    def parse(self, response):
        rows = response.css('div.product')

        for row in rows:
            yield {
                'title': row.css("div.product-description>a::text").get(),
                'price': row.xpath("//span[@class='price']/span/text()").get(),
                'stock_status': row.xpath("//div[@class='price-rating-container']//span[@class='status']//text()").get(),
            }
            prod_url = row.css('"div.product-description" + a::attr(href)').get()
            self.logger.info('get author page url')
            # go to the author page
            yield response.follow(prod_url, callback=self.parse_prod)

        for a in response.css('section.page-content'):
            yield response.follow(a, callback=self.parse)

    def parse_author(self, response):
        yield {
            'description': response.xpath('//div[@id="description"]::text').get(),
            'review': response.xpath('p[@class="pr-rd-description-text"]::text').get(),
            'delivery-info': response.css('.author-born-location::text').get(),
        }
