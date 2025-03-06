from .NexusPHP import NexusPHP
from lxml import etree


class Lgs(NexusPHP):

    def __init__(self, cookie):
        super().__init__(cookie)

    @staticmethod
    def get_url():
        return "https://ptlgs.org"

    def send_messagebox(self, message: str, callback=None) -> str:
        return super().send_messagebox(message)


class Tasks:
    def __init__(self, cookie: str):
        self.lgs = Lgs(cookie)

    def daily_shotbox(self):
        shbox_text_list = ["黑丝娘 求上传", "黑丝娘 求工分"]
        return "\n".join([self.lgs.send_messagebox(item) for item in shbox_text_list])

    def daily_checkin(self):
        return self.lgs.attendance()
