from .NexusPHP import NexusPHP
from lxml import etree


class Zm(NexusPHP):

    def __init__(self, cookie):
        super().__init__("https://zmpt.cc", cookie)

    def send_messagebox(self, message: str, callback=None) -> str:
        return super().send_messagebox(message,
                                       lambda response: " ".join(
                                           etree.HTML(response.text).xpath("//tr[1]/td//text()")))
        # TODO: ZM回应非直接刷新，需要额外刷新一次。考虑后期同象站一样从邮箱获取电力数据

class Tasks:
    def __init__(self, cookie: str):
        self.zm = Zm(cookie)

    def daily_shotbox(self):
        shbox_text_list = ["皮总，求电力", "皮总，求上传"]
        return "\n".join([self.zm.send_messagebox(item) for item in shbox_text_list])
