import datetime
from flask import Flask, render_template, request, Response
from sqlalchemy import desc
from slackclient import SlackClient
from config import Config
import bleach
from models import db, Slack

app = Flask(__name__)
db.init_app(app)
db.app = app
app.config.from_object(Config)

config = Config()
slack_client = SlackClient(config.SLACK_TOKEN)


# function to send messegae in slack by userbot:


def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        as_user="true:",
        text=message,

    )


# custom template tag to convert urls in urls likabled:


@app.template_filter('linkify')
def linkify(link):
    return bleach.linkify(link)


@app.route('/')
def home():
    msgs = Slack.query.order_by(desc(Slack.timestamp)).all()
    return render_template('index.html', msgs=msgs)


# function to get slack messages using outgoing webhook:


@app.route('/api/slackbot', methods=['POST'])
def outgoing_msg():
    if request.form.get('token') == config.SLACK_WEBHOOK_SECRET:
        channel_name = request.form.get('channel_name')
        channel_id = request.form.get('channel_id')
        username = request.form.get('user_name')
        time = request.form.get('timestamp')
        timestamp = datetime.datetime.fromtimestamp(
            int(float(time))).strftime('%d-%m-%Y %H:%M:%S')
        text = request.form.get('text').replace('::', '', 1)
        text = text.replace('>', '', 1).replace('<', '', 1)

        # Enable this block to debug and show in terminal the retrieve data:
        # inbound_message = "{} {} in {} says: {}".format(
        #        timestamp,
        #        username,
        #        channel_name,
        #        text
        #         )
        # print(inbound_message)

        # if get outgoing webhook response ok, userbot reply with this message:
        msg = "_Hola {} ! Gracias por compartirlo. " \
              "Puedes consultar tus aportes y de los demás en:_ " \
              "https://your-url.com/".format(username)

        send_message(channel_id, msg)

        slack_msg = Slack(
            username=username,
            content=text,
            channel=channel_name,
            channel_id=channel_id,
            timestamp=timestamp)

        # save in DB outgoing webhook messages:

        db.session.add(slack_msg)
        db.session.commit()

    return Response(), 200


if __name__ == "__main__":
    app.run(port=5000)
