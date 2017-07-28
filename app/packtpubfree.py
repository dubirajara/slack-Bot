import re
import time
from bs4 import BeautifulSoup
import requests
from slackclient import SlackClient


header = {}
header['Host'] = 'www.packtpub.com'
header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'
header['Accept'] = '*/*'
header['Accept-Language'] = 'en-US,en;q=0.5'
header['Accept-Encoding'] = 'gzip, deflate'
header['Upgrade-Insecure-Requests'] = '1'


def get_packtpub():
    '''Scraping packtpub web searching daily free ebook about python'''
    url = 'https://www.packtpub.com/packt/offers/free-learning'
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    div = soup.find('div', class_='dotd-main-book-summary float-left')
    patterns = 'Python|Django|Flask|scikit-learn|pandas'
    words = div.find_all(text=re.compile(patterns))

    if words:
        title = soup.h2.get_text().strip()
        today = time.strftime("%d/%m")
        msg = f"_Libro gratis solo hoy ({today}):_ *{title}*: {url}"

        send_message(msg)


def send_message(msg):
    '''send a message in slack if daily packtpub free ebook about python'''
    slack_client = SlackClient('SLACK_TOKEN')

    slack_client.api_call(
        "chat.postMessage",
        channel='here the Chanel ID',
        as_user="true:",
        text=msg
    )


if __name__ == "__main__":
    get_packtpub()
