import scrapy


class GetsdukoSpider(scrapy.Spider):
    name = "getsduko"
    allowed_domains = ["in.sduko.com"]
    custom_settings = {
        'COOKIES_ENABLED': True,
        'JOBDIR': 'Session/getsduko',
        'FEED_URI':'getSduko.jl',
         'LOG_FILE': 'getsduko.log',
        'LOG_LEVEL': 'DEBUG' ,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        }
    }
    start_urls = [
        # "https://in.sduko.com",
        "https://in.sduko.com/escorts/punjab/"
                  ]

    def parse(self, response):
        phoneno = response.xpath("//a[contains(@class,'btntelephone') and @data-last]/@data-last").extract_first()
        if phoneno:
            desc = title = images = None
            try:
                phoneno=phoneno.replace(" ",'')
            except:
                pass
            try:
                images= response.xpath("//div[contains(@class,'brick')]//img/@src").extract()
            except:
                pass
            try:
                title =  response.xpath("//div[contains(@class,'details-left-items')]/h1/text()").extract_first().strip()
            except:
                pass
            try:
                desc = ", ".join(response.xpath("//div[contains(@class,'details-left-items')]/p[not(@*)]/text()").extract())
            except:
                pass

            yield {"source": response.url, "images": images, "title": title, "phone": phoneno, "desc": desc}

        AvailableUrls=response.xpath("//a[starts-with(@href, 'https://in.sduko.com') and not(contains(@href, '/u/'))]/@href").extract()

        PaginationUrls = response.xpath("//a[contains(@class,'page-link') and @href]/@href").extract()

        if PaginationUrls:
            PaginationUrls = [response.urljoin(url) for url in PaginationUrls]
            for url in PaginationUrls:
                yield scrapy.Request(url,callback=self.parse)
        
        for url in AvailableUrls:
            yield scrapy.Request(url,callback=self.parse)