import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["in.liptpal.com"]
    # start_urls = ["https://in.liptpal.com/"]
    start_urls = [
        "https://in.liptpal.com/call-girls/central-delhi/call-girl-in-central-dehli-top-vip-hot-and-sexy-best-satisfied/815018"]
    custom_settings = {
        'COOKIES_ENABLED': True,
        'FEED_URI': 'getLiptpal.jl',
        'LOG_FILE': 'my_spider.log',
        'LOG_LEVEL': 'DEBUG'  # You can change this to INFO, WARNING, ERROR, or CRITICAL

    }

    def parse(self, response):
        title = response.xpath(
            "//div[@id='myCarousel']/preceding-sibling::h1/text()").extract_first()
        phone = response.xpath(
            "substring-after(//a[contains(@href,'tel')]/@href, 'tel:')").extract_first()
        ToFollow = response.xpath("""//a[
            starts-with(@href, 'https://in.liptpal') and 
            not(
                contains(@href, 'register') or 
                contains(@href, 'post-ad') or 
                contains(@href, 'faq') or 
                contains(@href, 'promote-your-ad') or 
                contains(@href, 'contact-us') or 
                contains(@href, 'privacy-policy') or 
                contains(@href, 'terms-condition') or 
                contains(@href, 'login'))]/@href""").extract()
        if title and phone:
            yield {
                "source": response.url,
                "title": response.xpath("//div[@id='myCarousel']/preceding-sibling::h1/text()").extract_first(),
                "images": [response.urljoin(url) for url in response.xpath("//div[@id='myCarousel']//img[contains(@src,'storage')]/@src").extract()],
                "phone": response.xpath("substring-after(//a[contains(@href,'tel')]/@href, 'tel:')").extract_first(),
                "desc": ",".join([x.strip() for x in response.xpath("//div[@id='myCarousel']/following-sibling::p/text()[normalize-space()]").extract()])
            }

        print(ToFollow)
        for url in ToFollow:
            yield scrapy.Request(url=url, callback=self.parse)
