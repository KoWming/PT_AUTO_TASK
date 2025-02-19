import time

from .NexusPHP import NexusPHP
from lxml import etree


class Zm(NexusPHP):

    def __init__(self, cookie):
        super().__init__("https://zmpt.cc", cookie)

    def send_messagebox(self, message: str, callback=None) -> str:
        return super().send_messagebox(message, lambda response: "")


class Tasks:
    def __init__(self, cookie: str):
        self.zm = Zm(cookie)

    def daily_shotbox(self):
        shbox_text_list = ["皮总，求电力", "皮总，求上传"]
        rsp_text_list = []
        for item in shbox_text_list:
            self.zm.send_messagebox(item)
            time.sleep(0.5)
            message_list = self.zm.get_messagebox()
            if message_list:
                message = message_list[0]
                rsp_text_list.append(message)
        return "\n".join(rsp_text_list)

    def daily_checkin(self):
        return self.zm.attendance()
