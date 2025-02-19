from .NexusPHP import NexusPHP
from lxml import etree


class Vicomo(NexusPHP):

    def __init__(self, cookie):
        super().__init__("https://ptvicomo.net", cookie)

    def send_messagebox(self, message: str, callback=None) -> str:
        return super().send_messagebox(message,
                                       lambda response: "")


class Tasks:
    def __init__(self, cookie: str):
        self.vicomo = Vicomo(cookie)

    def daily_shotbox(self):
        shbox_text_list = ["小象求象草"]
        rsp_text_list = []
        for item in shbox_text_list:
            self.vicomo.send_messagebox(item)
            message_list = self.vicomo.get_message_list()
            if message_list:
                message = message_list[1].get("topic", "")
                rsp_text_list.append(message)
                self.vicomo.set_message_read(message_list[1].get("id", ""))
        return "\n".join(rsp_text_list)

    def daily_checkin(self):
        return self.vicomo.attendance(
            lambda response: "".join(etree.HTML(response.text).xpath("//td/table//tr/td/p//text()")))
