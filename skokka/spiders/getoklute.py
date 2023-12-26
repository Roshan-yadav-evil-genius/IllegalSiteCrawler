import scrapy


class GetokluteSpider(scrapy.Spider):
    name = "getoklute"
    allowed_domains = ["hi.oklute.com"]
    start_urls = ["https://hi.oklute.com/"]
    custom_settings = {
        'COOKIES_ENABLED': True,
        'JOBDIR': 'Session/getoklute',
        'FEED_URI': 'getOklute.jl',
        'LOG_FILE': 'getOklute.log',
        'LOG_LEVEL': 'DEBUG'  # You can change this to INFO, WARNING, ERROR, or CRITICAL
    }

    def parse(self, response):
        title = response.xpath(
            "//h1[@class='main-title']/text()").extract_first()
        images = response.xpath(
            "//div[@class='gallery-grid']//img/@src").extract()
        if title and images:
            yield {
                "source": response.url,
                "images": response.xpath("//div[@class='gallery-grid']//img/@src").extract(),
                "title": response.xpath("//h1[@class='main-title']/text()").extract_first(),
                "phone": response.xpath("//a[@data-phone]/@data-phone").extract_first(),
                "desc": ",".join([x.strip() for x in response.xpath("//h1[@class='main-title']/following-sibling::p/text()").extract()])
            }

        ToFollow = list(set(response.xpath("""//a[
                starts-with(@href, 'https://hi.oklute.com')]/@href""").extract()))

        for url in ToFollow:
            yield scrapy.Request(url, callback=self.parse)
