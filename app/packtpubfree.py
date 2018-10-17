import os
import re
import time
from bs4 import BeautifulSoup
import requests
from slackclient import SlackClient
import twitter


header = {'Host': 'www.packtpub.com',
          'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
          'Accept': '*/*',
          'Accept-Language': 'en-US,en;q=0.5',
          'Accept-Encoding': 'gzip, deflate',
          'Upgrade-Insecure-Requests': '1'}


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
        msg_slack = f"_Libro gratis solo hoy ({today}):_ *{title}*: {url}"
        msg_twitter = f"Free Ebook today ({today}): " \
                      f"{title}: http://bit.ly/PacktDailyOffer #Python #PacktPub #FreeLearning"

        send_message_slack(msg_slack)
        send_message_twitter(msg_twitter)


def send_message_slack(msg_slack):
    '''send a message in slack if daily packtpub free ebook about python'''
    slack_client = SlackClient('SLACK_TOKEN')

    slack_client.api_call(
        "chat.postMessage",
        channel='here the Chanel ID',
        as_user="true:",
        text=msg_slack
    )


def send_message_twitter(msg_twitter):
    '''send a message in twitter if daily packtpub free ebook about python'''
    api = twitter.Api(consumer_key=os.environ.get('consumer_key'),
                      consumer_secret=os.environ.get('consumer_secret'),
                      access_token_key=os.environ.get('access_token_key'),
                      access_token_secret=os.environ.get('access_token_secret'))

    api.PostUpdate(msg_twitter)


if __name__ == "__main__":
    get_packtpub()
