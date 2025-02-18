from utils.custom_requests import CustomRequests


class NexusPHP:
    def __init__(self, url, cookie: str, url_shoutbox: str = None, url_ajax: str = None, attendance_url: str = None):
        self.url = url
        self.url_shoutbox = url_shoutbox or self.url + "/shoutbox.php"
        self.url_ajax = url_ajax or self.url + "/ajax.php"
        self.attendance_url = attendance_url or self.url + "/attendance.php"
        self.cookie = cookie
        self.headers = {
            "cookie": self.cookie,
            "referer": self.url,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
        }

    """
    发送群聊区消息
    """

    def send_messagebox(self, message: str, rt_method: callable) -> str:
        params = {
            "shbox_text": message,
            "shout": "%E6%88%91%E5%96%8A",
            "sent": "yes",
            "type": "shoutbox"
        }
        response = CustomRequests.get(self.url_shoutbox, headers=self.headers, params=params)
        return rt_method(response)

    """
    申领任务
    """

    def claim_task(self, task_id: str, rt_method: callable) -> str:
        data = {
            "action": "claimTask",
            "params[exam_id]": task_id
        }

        response = CustomRequests.post(self.url_ajax, headers=self.headers, data=data)
        return rt_method(response)

    """
    每日签到
    """

    def attendance(self, rt_method: callable):
        response = CustomRequests.get(self.attendance_url, headers=self.headers)
        return rt_method(response)
