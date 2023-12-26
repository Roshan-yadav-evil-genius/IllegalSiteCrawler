import scrapy
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class GetskokkaSpider(scrapy.Spider):
    name = "getskokka"
    allowed_domains = ["www.skokka.in"]
    custom_settings = {
        'COOKIES_ENABLED': True,
        'JOBDIR': 'Session/getskokka',
        'FEED_URI':'getSkokka.jl',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }
    start_urls = [
        # "https://www.skokka.in",
        "https://www.skokka.in/call-girls/"
    ]

    def parse(self, response):
        ToFollow = response.xpath(
            "//a[contains(@href,'https://www.skokka.in') and not(contains(@href,'/ad/')) ]/@href").extract()
        ToExtract = response.xpath(
            "//a[contains(@href,'https://www.skokka.in') and contains(@href,'/ad/') ]/@href").extract()
        NextPage = response.xpath(
            "//a[contains(@title,'next')]").extract_first()

        for url in ToExtract:
            yield scrapy.Request(url, callback=self.ExtractDetails)

        if NextPage:
            currentPageNum = self.getPageNumberFromUrl(response.url)
            NextPageUrl = self.add_parameter_to_url(
                response.url, 'p', currentPageNum+1)
            yield scrapy.Request(NextPageUrl, callback=self.parse)

        for url in ToFollow:
            yield scrapy.Request(url, callback=self.parse)

    def getPageNumberFromUrl(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        page_number = query_params.get('p', [1])[0]
        return int(page_number)

    def add_parameter_to_url(self, url, param_name, param_value):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params[param_name] = [param_value]
        new_query = urlencode(query_params, doseq=True)
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc,
                             parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
        return new_url

    def ExtractDetails(self, response):
        desc = phone = title = images = None
        source = response.url
        try:
            images = response.xpath(
                "//div[@class='brick']/*/img/@src").extract()
        except:
            pass
        try:
            title = response.xpath(
                "//*[contains(@class,'main-title')]/text()").extract_first()
        except:
            pass
        try:
            phone = response.xpath(
                "//div[contains(@class,'contactdk')]/*[@number]/@number").extract_first()
        except:
            pass
        try:
            desc = ", ".join(response.xpath(
                "//*[contains(@class,'service-detail')]/*/text()").extract()).strip()
        except:
            pass

        yield {"source": source, "images": images, "title": title, "phone": phone, "desc": desc}
