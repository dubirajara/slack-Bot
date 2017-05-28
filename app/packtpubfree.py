import os
import re
from bs4 import BeautifulSoup
import requests
from slackclient import SlackClient


'''
Script to send a message in slack if daily packtpub free book is about python.
'''

url = 'https://www.packtpub.com/packt/offers/free-learning'

header = {}
header['Host'] = 'www.packtpub.com'
header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'
header['Accept'] = '*/*'
header['Accept-Language'] = 'en-US,en;q=0.5'
header['Accept-Encoding'] = 'gzip, deflate'
header['Upgrade-Insecure-Requests'] = '1'

r = requests.get(url, headers=header)
soup = BeautifulSoup(r.text, 'lxml')

slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))


def send_message(message):
    slack_client.api_call(
        "chat.postMessage",
        channel='Chanel ID',
        as_user="true:",
        text=message,
    )


def get_packtpub():
    div = soup.find('div', class_='dotd-main-book-summary float-left')
    patterns = 'Python | Django | Flask'
    words = div.find_all(text=re.compile(patterns))

    if words:
        title = soup.h2.get_text().strip()

        msg = "_Libro gratis solo hoy:_ *{}*: {}".format(title, url)

        send_message(msg)


if __name__ == "__main__":
    get_packtpub()
