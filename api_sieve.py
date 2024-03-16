import requests
from bs4 import BeautifulSoup
import random
from login import Login
import secrets

class ApiSieve:

    URL = 'https://api-mts.orbis.easytrader.ir/symbols/api/sectors/sieve'

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    ]

    HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fa",
        "Authorization": "",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        # 'User-Agent': random.choice(user_agents),
        # "Content-Type": "application/json",
        "Sec-Ch-Ua-Mobile": "?0",
        "Referer": "https://d.orbis.easytrader.ir/",
        "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "Sec-Ch-Ua-Platform": '"Linux"',
    }

    def request_method_post(self):
        r = requests.post(url=self.URL, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")
        with open("html/api_sieve.html", 'w') as f:
            f.write(soup.prettify())
        print(r.status_code)

    def request_method_post_logged_in(self):
        user1 = Login(secrets.username, secrets.password)
        session, response = user1.request_method_post()
        r = session.post(url=self.URL, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        with open("./html/api_sieve.html", 'w') as f:
            f.write(soup.prettify())
        print(r.status_code)


if __name__ == '__main__':
    object1 = ApiSieve()
    # object1.request_method_post()
    object1.request_method_post_logged_in()


