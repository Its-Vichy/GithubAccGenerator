import requests, time

class Capmonster(): 
    def __init__(self, captcha_service: str, captcha_key: str):
        self.headers = {
            "content-type": "application/json"
        }

        proxy = 'http://proxies.gay:5000'

        self.captcha_key = captcha_key
        self.captcha_service = captcha_service
        self.proxies = {'http': proxy, 'https://': proxy}

    def create_task(self):
        try:
            payload = {
                    "clientKey": self.captcha_key,
                    "task": {
                        "type": "FunCaptchaTaskProxyless",
                        "websiteURL": f"https://github.com",
                        "websitePublicKey": "69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
                    }
                }

            resp = requests.post(f"https://api.{self.captcha_service}/createTask", json=payload, headers=self.headers, proxies=self.proxies).json()

            if resp["errorId"] == 0:
                return resp["taskId"]
            else:
                print(resp)
                return self.create_task()

        except Exception as e:
            return self.create_task()

    def get_result(self, task_id: str):
        try:
            payload = {
                "clientKey": self.captcha_key,
                "taskId": task_id
            }
            resp = requests.get(f"https://api.{self.captcha_service}/getTaskResult", json=payload, headers=self.headers, proxies=self.proxies).json()

            if resp["errorId"] == 0:
                if resp["status"] == "ready":
                    return resp["solution"]["token"]
                else:
                    time.sleep(0.1)
                    return self.get_result(task_id)
            else:
                return self.get_result(task_id)

        except Exception as e:
            return self.get_result(task_id)

    def get_balance(self):
        try:
            payload = {
                "clientKey": self.captcha_key
            }
            return requests.get(f"https://api.{self.captcha_service}/getBalance", json=payload, headers=self.headers, proxies=self.proxies).json()['balance']

        except Exception as e:
            return self.get_balance()

    def start(self):
        task = self.create_task()
        return self.get_result(task)
