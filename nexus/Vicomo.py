from .NexusPHP import NexusPHP
from lxml import etree


class Vicomo(NexusPHP):

    def __init__(self, cookie):
        super().__init__("https://ptvicomo.net", cookie)

    def send_messagebox(self, message: str, callback=None) -> str:
        return super().send_messagebox(message,
                                       lambda response: "")
        # TODO: 象站返回数据在邮箱种，需要进一步处理


class Tasks:
    def __init__(self, cookie: str):
        self.vicomo = Vicomo(cookie)

    def daily_shotbox(self):
        shbox_text_list = ["小象求象草"]
        return "\n".join([self.vicomo.send_messagebox(item) for item in shbox_text_list])

    def daily_checkin(self):
        return self.vicomo.attendance(
            lambda response: "".join(etree.HTML(response.text).xpath("//td/table//tr/td/p//text()")))
