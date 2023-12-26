import scrapy
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser


class GetliptpalSpider(scrapy.Spider):
    name = "getliptpal"
    allowed_domains = ["in.liptpal.com"]
    custom_settings = {
        'COOKIES_ENABLED': True,
        'JOBDIR': 'Session/getliptpal',
        'FEED_URI': 'getLiptpal.jl',
         'LOG_FILE': 'getLiptpal.log',
        'LOG_LEVEL': 'DEBUG' 
    }
    start_urls = ["https://in.liptpal.com/"]

    def parse(self, response):
        # open_in_browser(response)
        # inspect_response(response,self)
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
                "images": [ response.urljoin(url) for url in response.xpath("//div[@id='myCarousel']//img[contains(@src,'storage')]/@src").extract()],
                "phone": response.xpath("substring-after(//a[contains(@href,'tel')]/@href, 'tel:')").extract_first(),
                "desc": ",".join([x.strip() for x in response.xpath("//div[@id='myCarousel']/following-sibling::p/text()[normalize-space()]").extract()])
            }


        
        for url in ToFollow:
            yield scrapy.Request(url=url, callback=self.parse)
