from .NexusPHP import NexusPHP
from lxml import etree


class Car(NexusPHP):

    def __init__(self, cookie):
        super().__init__("https://carpt.net", cookie)

    def send_messagebox(self, message: str, callback=None) -> str:
        return super().send_messagebox(message,
                                       lambda response: " ".join(
                                           etree.HTML(response.text).xpath("//tr[1]/td/span/text()")))

    def claim_task(self, task_id: str, rt_method=None):
        return super().claim_task(task_id, lambda response: response.json().get("msg", "未知错误"))


class Tasks:
    def __init__(self, cookie: str):
        self.car = Car(cookie)

    def daily_claim_task(self):
        task_id_list = ["5"]
        return "\n".join([self.car.claim_task(item) for item in task_id_list])
