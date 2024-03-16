import requests
from bs4 import BeautifulSoup
import secrets
import re


class Login:

    URL = "https://account.emofid.com/Login"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session, self.GET_response = self.__GET_request()
        self.POST_response = self.session.post(url=self.URL, data=self.__form_data())

    def __GET_request(self):
        session = requests.session()
        response = session.get(self.URL)
        if response.status_code != 200:
            raise Exception('Could not reach login page by get request method!')
        return session, response

    def __get_token(self):
        try:
            bs = BeautifulSoup(self.GET_response.text, 'html.parser')
            form = bs.find('form')
            inputs = form.find_all('input')
            token = inputs[3]['value']
        except:
            raise Exception("Somthing is wrong with the token!")
        return token

    def __form_data(self):
        data = {
            'Username': self.username,
            'Password': self.password,
            'button': 'login',
            '__RequestVerificationToken': self.__get_token()
        }
        return data

    def is_logged_in(self):
        if self.POST_response is None:
            return False
        else:
            soup = BeautifulSoup(self.POST_response.text, 'html.parser')
            if re.search(".*Easy Trader.*", str(soup.find('title'))):
                return True
            elif re.search(".*ورود.*", str(soup.find('title'))):
                return False
            else:
                return False


if __name__ == '__main__':

    # create an object
    obj1 = Login(secrets.username, secrets.password)
