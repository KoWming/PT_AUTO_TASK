import time

from .NexusPHP import NexusPHP
from lxml import etree
from utils.custom_requests import CustomRequests


class Zm(NexusPHP):

    def __init__(self, cookie):
        super().__init__(cookie)
        self.bonus_url = self.url + "/javaapi/user/drawMedalGroupReward?medalGroupId=3"

    @staticmethod
    def get_url():
        return "https://zmpt.cc"

    def send_messagebox(self, message: str, callback=None) -> str:
        return super().send_messagebox(message, lambda response: "")

    def medal_bonus(self):
        response = CustomRequests.get(self.bonus_url, headers=self.headers)
        response_data = response.json()

        ## response_data format like this 
        # {
        #    "serverTime": 1741177064362,
        #    "success": true,
        #    "errorCode": 0,
        #    "errorMsg": "",
        #    "result": {
        #        "rewardAmount": 15000,
        #        "seedBonus": "818255.0"
        #    }
        # }
        result = response_data.get("result", None)
        if result is None:
            print(f"勋章套装奖励领取失败：{response_data.get('errorMsg', None)}")
        else:
            reward = result['rewardAmount']
            seed_bonus = result['seedBonus']

            print(f"梅兰竹菊成套勋章奖励: {reward}")
            print(f"总电力: {seed_bonus}")


class Tasks:
    def __init__(self, cookie: str):
        self.zm = Zm(cookie)

    def daily_shotbox(self):
        shbox_text_list = ["皮总，求电力", "皮总，求上传"]
        rsp_text_list = []
        for item in shbox_text_list:
            self.zm.send_messagebox(item)
            time.sleep(3)
            message_list = self.zm.get_messagebox()
            if message_list:
                message = message_list[0]
                rsp_text_list.append(message)
        return "\n".join(rsp_text_list)

    def daily_checkin(self):
        return self.zm.attendance()

    def medal_bonus(self):
        return self.zm.medal_bonus()
