import os
import re
import time

import slack
from selenium import webdriver
import twitter
from slack.errors import SlackApiError

slack_client = slack.WebClient(token=os.environ.get('SLACK_TOKEN'))
channel = os.environ.get('SLACK_CHANNEL')


def get_packtpub():
    '''Scraping packtpub web searching daily free ebook about python'''
    patterns = 'Python|Django|Flask|scikit-learn|pandas'
    url = 'https://www.packtpub.com/packt/offers/free-learning'

    driver = webdriver.PhantomJS()
    driver.implicitly_wait(10)
    driver.get(url)

    text = driver.find_element_by_class_name("product-info__content").text

    if re.search(patterns, text):
        title = driver.find_element_by_class_name("product-info__title").text
        image = driver.find_element_by_class_name("product-image").get_attribute('src')
        today = time.strftime("%d/%m")
        msg_slack = f":python: _Libro gratis solo hoy ({today}):_ *{title}*: {url}"
        print(msg_slack)
        msg_twitter = f"Free Ebook today ({today}): " \
                      f"{title}: http://bit.ly/PacktDailyOffer #Python #PacktPub #FreeLearning"

        delete_slack_message()
        send_message_slack(msg_slack, image)
        send_message_twitter(msg_twitter)

    else:
        print('Not python today')

    driver.quit()


def send_message_slack(msg_slack, image):
    '''send a message in slack if daily packtpub free ebook about python'''
    response = slack_client.chat_postMessage(
        channel=channel,
        as_user="true:",
        attachments=[{
            "color": "#36a64f",
            "text": msg_slack,
            "image_url": image
            }])

    print(response['ok'])


def send_message_twitter(msg_twitter):
    '''send a message in twitter if daily packtpub free ebook about python'''
    api = twitter.Api(consumer_key=os.environ.get('consumer_key'),
                      consumer_secret=os.environ.get('consumer_secret'),
                      access_token_key=os.environ.get('access_token_key'),
                      access_token_secret=os.environ.get('access_token_secret'))

    api.PostUpdate(msg_twitter)


def delete_slack_message():
    response = slack_client.conversations_history(channel=channel)

    all_msgs = (item['ts'] for item in response['messages'] if response['messages'][0]['user'] == 'U4ZCW6UCW')

    for msg in all_msgs:
        try:
            slack_client.chat_delete(channel=channel, ts=msg)
        except SlackApiError:
            ...


if __name__ == "__main__":
    get_packtpub()
