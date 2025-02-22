from nexus.NexusPHP import NexusPHP
from utils.custom_requests import CustomRequests
from lxml import etree


class LemonHD(NexusPHP):

    def __init__(self, cookie):
        super().__init__("https://lemonhd.club", cookie)
        self.lottery_url = self.url + "/lottery.php"

    def lottery(self, parameter: tuple = None, rt_method: callable = None):
        response = CustomRequests.post(self.lottery_url, headers=self.headers, data="type=0")
        return ''.join(etree.HTML(response.text).xpath("//table/tr[1]/td[1]/text()")).strip()


class Tasks:
    def __init__(self, cookie: str):
        self.lemonHD = LemonHD(cookie)

    def daily_checkin(self):
        return self.lemonHD.attendance(
            lambda response: "".join(etree.HTML(response.text).xpath('//table//tr/td/text()')).strip())

    def daily_lottery(self):
        return self.lemonHD.lottery()
