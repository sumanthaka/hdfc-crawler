import re

import scrapy

from hdfccrawler.items import Card


class CardspiderSpider(scrapy.Spider):
    name = "cardspider"
    allowed_domains = ["www.hdfcbank.com"]
    start_urls = ["https://www.hdfcbank.com/personal/pay/cards/credit-cards"]

    def parse(self, response):
        cards = response.xpath('//div[contains(@class, "card-offer-contr")]')
        for card in cards:
            info_url = card.xpath('.//a[translate(@title, "ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz") = "know more"]/@href').get()
            if info_url is not None:
                yield response.follow(info_url, callback=self.parse_info)

    def parse_info(self, response):
        card = Card()
        card["name"] = response.xpath('//div[@class="section-details"]/h1/text()').get()
        lounge_exists = response.xpath('//h4/text()').getall()
        if "Lounge Access" in lounge_exists:
            lounge_benefit = response.xpath('//div[contains(h4, "Lounge Access")]/following-sibling::div[contains(@class,"right-section")]/ul/li/text()').getall()
            if not lounge_benefit:
                lounge_benefit = response.xpath('//div[contains(h4, "Lounge Access")]/following-sibling::div[contains(@class,"right-section")]//p/text()').getall()
            card["lounge"] = lounge_benefit
        else:
            card["lounge"] = "NA"

        milestone_exists = response.xpath('//h4/text()').getall()
        if "Milestone Benefit" in milestone_exists:
            milestone_benefit = response.xpath('//div[contains(h4, "Milestone Benefit")]/following-sibling::div[contains(@class,"right-section")]/ul/li/text()').getall()
            if not milestone_benefit:
                milestone_benefit = response.xpath('//div[contains(h4, "Milestone Benefit")]/following-sibling::div[contains(@class,"right-section")]//p/text()').getall()
            card["milestone"] = milestone_benefit
        else:
            card["milestone"] = "NA"

        renewal_exists = response.xpath('//h4/text()').getall()
        for renewal in renewal_exists:
            if "Renewal" in renewal:
                renewal_benefit = response.xpath('//div[contains(h4, "Renewal")]/following-sibling::div[contains(@class,"right-section")]/ul/li/text()').getall()
                if not renewal_benefit:
                    renewal_benefit = response.xpath('//div[contains(h4, "Renewal")]/following-sibling::div[contains(@class,"right-section")]//p/text()').get()
                card["reversal"] = renewal_benefit
                break
        else:
            card["reversal"] = "NA"

        features = response.xpath('//div[contains(@class, "inner-content") and contains(@class, "right-section")]/ul/li/text()').getall()
        if not features:
            features = response.xpath('//div[contains(@class, "inner-content") and contains(@class, "right-section")]//p/text()').getall()
        if not features:
            rewards_exist = response.xpath('//h4/text()').getall()
            if "Rewards" in rewards_exist:
                features = response.xpath('//div[contains(h4, "Rewards")]/following-sibling::div[contains(@class,"right-section")]//p/text()').get()
        reward_str = []
        for feature in features:
            if 'spent' not in feature.lower():
                continue
            if 'reward point' in feature.lower() or 'cashpoints' in feature.lower():
                reward_str.append(feature.lower().replace(".", ""))

        if not reward_str:
            card["reward"] = "NA"
        else:
            reward_str_split = reward_str[0].split()
            values = []
            point = reward_str_split[reward_str_split.index('reward')-1] if 'reward' in reward_str_split else reward_str_split[reward_str_split.index('cashpoints')-1]
            spent = reward_str_split[reward_str_split.index('reward')+1:reward_str_split.index('spent')]
            spent = ''.join(spent)
            spent = int(re.search(r'\d+', spent).group())
            values.append(int(point))
            values.append(int(spent))
            card["reward"] = values

        yield response.follow(response.request.url + "/fees-and-charges", callback=self.parse_fees, meta={'card': card})

    def parse_fees(self, response):
        fees_str = response.xpath('//div[contains(@class, "inner-content")]/ul/li/text()').get()
        if not fees_str:
            fees_str = response.xpath('//div[contains(@class, "inner-content")]/p/text()').get()
        response.meta['card']["fees"] = fees_str
        yield response.meta['card']
