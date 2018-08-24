# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.spidermiddlewares.httperror import HttpError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait = webdriver.support.ui.WebDriverWait
By = webdriver.common.by.By
Keys = webdriver.common.keys.Keys

class RedfinSearchSpider(Spider):
    name = 'redfin_search'
    allowed_domains = ['redfin.com']
    start_urls = ['http://redfin.com/']

    def __init__(self):
        options = COptions()
        options.set_headless()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)

    def start_requests(self):
        yield Request('https://www.redfin.com/', callback=self.parse, errback=self.handle_err)

    def parse(self, response):
        try:
            self.driver.get(response.url)
            search = self.driver.find_element_by_id('search-box-input')
            search.clear()
            search.send_keys('69 Nancy Court, Clayton, NC 27520')
            search.send_keys(Keys.RETURN)
            PRICE_CONDITION = '//div[@class="info-block price"]/div/div/span'
            # price = WebDriverWait(self.driver, 10).until(
            #         EC.presence_of_element_located((By.find_elements_by_xpath, PRICE_CONDITION))
            #     )
            price = self.driver.find_elements_by_xpath(PRICE_CONDITION)
            try:
                update = {'List Price': price[1].text} 
            except:
                update = {}
            return update
        finally:
            self.driver.quit()

    def handle_err(self, failure):
        
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            self.logger.error(repr(failure))

            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
            
 

