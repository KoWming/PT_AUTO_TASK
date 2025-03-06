from .NexusPHP import NexusPHP
from lxml import etree


class Cyanbug(NexusPHP):

    def __init__(self, cookie):
        super().__init__(cookie)

    @staticmethod
    def get_url():
        return "https://cyanbug.net"

    def send_messagebox(self, message: str, callback=None) -> str:
        return super().send_messagebox(message)


class Tasks:
    def __init__(self, cookie: str):
        self.cyanbug = Cyanbug(cookie)

    def daily_shotbox(self):
        shbox_text_list = ["青虫娘，求上传", "青虫娘，求魔力", "青虫娘，求下载"]
        return "\n".join([self.cyanbug.send_messagebox(item) for item in shbox_text_list])

    def daily_checkin(self):
        return self.cyanbug.attendance()
