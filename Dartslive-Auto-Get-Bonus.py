import requests
import time
import random
import datetime
from bs4 import BeautifulSoup
import json
import os

class Dartslive(object):

    def __init__(self, email, password):
        self._url_password_input = "https://card.dartslive.com/entry/login/password_input.jsp"
        self._url_do_login = "https://card.dartslive.com/entry/login/doLogin.jsp"
        self._url_get_bonus = "https://card.dartslive.com/account/bonus/index.jsp"
        self._url_coinstore = "https://card.dartslive.com/t/coinstore/pickup.jsp"
        self._url_logout = "https://card.dartslive.com/t/logout.jsp"
        self._email = email
        self._password = password
        self._session = requests.Session()
        self._text = ""

    def post(self, url, data={}):
        try:
            response = self._session.post(url, data=data)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
            return False
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
            return False
        else:
            time.sleep(random.randint(2, 5))
            self._text = response.text
            return True

    def login(self):
        if self.post(self._url_password_input, {'id': self._email}):
            print('\tInput Email Success!')
            if self.post(self._url_do_login, {
                    'id': self._email,
                    'ps': self._password
            }):
                soup = BeautifulSoup(self._text, "html.parser")
                if soup and soup.find(id='cardtop'):
                    print('\tLogin Success!')
                    return True
                print('\tLogin Error')
                return False
        else:
            print('\tInput Email Error')
        return False

    def get_bonus(self):
        if self.post(self._url_get_bonus):
            soup = BeautifulSoup(self._text, "html.parser")
            if soup and soup.find(id='coinBonus'):
                print('\tGet Bonus Success!')
            else:
                print('\tYou have already gotten bonus before!')
            return True
        else:
            print('\tGet Bonus Error')
            return False

    def show_own_coin(self):
        if self.post(self._url_coinstore):
            soup = BeautifulSoup(self._text, "html.parser")
            total_coin = ''
            this_month_coin = ''
            for div in soup.findAll("div", {"class": "coinNumArea"}):
                for span in div.findAll("span", {"class": "num"}):
                    total_coin = span.get_text()
                for span in div.findAll("span", {"class": "thisMonth"}):
                    this_month_coin = span.get_text()
            if total_coin and this_month_coin:
                print('\tYou have', total_coin, this_month_coin, 'coins.')
                return True
        print('\tShow Coin Error')
        return False

    def logout(self):
        if self.post(self._url_logout):
            print('\tLogout Success!')
            return True
        else:
            print('\tLogout Error')
            return False


def main():
    email = []
    password = []
    dir_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_path, 'user.json')) as json_file:
        data = json.load(json_file)
        for ptt in data:
            email.append(ptt['email'])
            password.append(ptt['password'])

    print('====================BEGIN====================')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for i in range(len(email)):
        print('Email: ', email[i])
        dartslive = Dartslive(email[i], password[i])
        if dartslive.login():
            if dartslive.get_bonus():
                dartslive.show_own_coin()
            dartslive.logout()
        time.sleep(random.randint(1, 10) * 60)
    print('=============== END ===============')


if __name__ == "__main__":
    main()
