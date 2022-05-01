from module import captcha, email
import httpx, threading


def gen():
    # content lenght / cookie =  _octo=
    session = httpx.Client(headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': '_device_id=9e172d5d49e48201e5a357b6af21257b; has_recent_activity=0; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; tz=Europe%2FParis; tz=Europe%2FParis; logged_in=no; _gh_sess=9ugyrnSQI%2B3xIMQNyM3IY1agB%2FCISEH7nkPqs6H1XorPDReaQ%2BZ1Ew19eKvHCRYp42x0f7o4P7nUORgIGIzFsKYdIyKnKk0Yh9TTBMR7fKciyfzqSLFXqhi6RQsQgixKbKPKwmRR%2FBbBTy%2BYyX1HeFkNHhVohyn3rkllykCkysq9JqTEwZemqFgUMXmPhBeV%2BidPjFqAZKyodPsbjXq1m6t6ZLC%2BkqyiSkiR%2BVq2gs%2BTTPgdn38FQgarX7nHTc%2FUUmYS2%2FqfdsAwYBWKn4OHiKfR%2B5nbkykkJGqGe6f4qB71PizC--%2FhiNUQqDNJ5R639O--94alGZYIFPJtqRPm%2FI2zwg%3D%3D',
        'origin': 'https://github.com',
        'referer': 'https://github.com/join',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }, proxies='http://proxies.gay:5000', timeout=30)

    content = session.get('https://github.com/join').text

    authenticity_token = content.split('<input type="hidden" data-csrf="true" name="authenticity_token" value="')[1].split('" />')[0].strip()
    timestamp = int(content.split('<input class="form-control" type="hidden" name="timestamp" value="')[1].split('" />')[0].strip())
    timestamp_secret = content.split('<input class="form-control" type="hidden" name="timestamp_secret" value="')[1].split('" />')[0].strip()

    print(f'[authenticity_token] {authenticity_token}')
    print(f'[timestamp_secret] {timestamp_secret}')
    print(f'[timestamp] {timestamp}')

    m = email.Email('http://proxies.gay:5000')
    mail = m.get_mail()
    print(f'[email] {mail}')

    print('[captcha] solving...')
    cap = captcha.Capmonster('anti-captcha.com', 'lol').start()
    print(f'[captcha] {cap[:35]}')

    username = mail.split('@')[0]

    data = {
        'authenticity_token': authenticity_token,
        'user[login]': username,
        'user[email]': mail,
        'user[password]': mail,
        'source': 'form-join',
        'required_field_be2b': '',
        'timestamp': timestamp,
        'timestamp_secret': timestamp_secret,
        'octocaptcha-token': cap,
        'suggested_usernames[]': username + '-design',
        'suggested_usernames[]': username + '-spec',
        'suggested_usernames[]': username + '430',
    }

    response = session.post('https://github.com/join', data=data, follow_redirects=True)

    if response.status_code == 302 or response.status_code == 200:
        authenticity_token = session.get('https://github.com/account_verifications?recommend_plan=false').text.split('name="authenticity_token" value="')[1].split('"')[0].strip()
        print(f'[authenticity_token] {authenticity_token}')

        print('[creating] success, waiting for confirmation code')
        code = m.get_verification_token()
        print(f'[confirm_code] {code}')

        l_code = list(code)

        confirm_data = f'authenticity_token={authenticity_token}&recommend_plan=true&plan=&setup_organization=&launch_code%5B%5D={code}'
        print(confirm_data)

        session.headers['referer'] = str(response.url)
        confirm_response = session.post('https://github.com/account_verifications', data=confirm_data)

        with open('./oof.txt', 'a+') as f:
            f.write(f'{mail}:{session.cookies}')

        if confirm_response.status_code == 302:
            print(f'[verification] Successfully confirmed account, {mail}')
        else:
            if 'Your browser did something unexpected. Please try again. If the error continues' in confirm_response.text:
                print(f'[error verif -> {confirm_response.status_code}] Your browser did something unexpected. Please try again. If the error continues')
            else:
                print(confirm_response.text)


for _ in range(2):
    threading.Thread(target=gen).start()
