import httpx, time, re

# just for debug this mail was spotted

class Email:
    def __init__(self, proxy: str):
        self.session= httpx.Client(proxies= proxy, timeout=30)
    
    def get_mail(self):
        return self.session.get('https://emailtemp.org/en/messages').json()['mailbox']
    
    def get_verification_token(self):
        while True:
            time.sleep(5)
            try:
                response= self.session.get('https://emailtemp.org/en/messages')

                if response.text == '':
                    continue
                
                for message in response.json()['messages']:
                    if message['from'] == 'GitHub':
                        print(f'[email] got a message from github')
                        code = message['content'].split('/confirm_verification/')[1].split('?via_launch_code_email=true')[0]
                        return code
            except:
                pass