from .NexusPHP import NexusPHP
from lxml import etree


class Qingwa(NexusPHP):

    def __init__(self, cookie):
        super().__init__("https://www.qingwapt.com", cookie)

    def send_messagebox(self, message: str, callback=None) -> str:
        # 调用父类函数，并将回调函数设为rsp_data = etree.HTML(response.text).xpath("//ul[1]/li/text()")
        return super().send_messagebox(message,
                                       lambda response: " ".join(etree.HTML(response.text).xpath("//ul[1]/li/text()")))


class Tasks:
    def __init__(self, cookie: str):
        self.qingwa = Qingwa(cookie)

    def daily_shotbox(self):
        shbox_text_list = ["蛙总，求上传", "蛙总，求下载"]
        return "\n".join([self.qingwa.send_messagebox(item) for item in shbox_text_list])

    def daily_checkin(self):
        return self.qingwa.attendance()
