import datetime
from flask import Flask, render_template, request, Response
from sqlalchemy import desc
from slackclient import SlackClient
import bleach

from app.models import db, Slack
from app.api.api import api
from config import Config

app = Flask(__name__)
app.register_blueprint(api)
app.config.from_object(Config)
db.init_app(app)

config = Config()
slack_client = SlackClient(config.SLACK_TOKEN)


def send_message(channel_id, message):
    '''call api to send message in slack by userbot'''
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        as_user="true:",
        text=message,

    )


@app.template_filter('linkify')
def linkify(link):
    '''custom template tag to convert urls in clickable links'''
    return bleach.linkify(link)


@app.route('/')
@app.route('/<int:page>', methods=['GET'])
def home(page=1):
    '''retrieve all msgs and render in home'''
    msgs = Slack.query.order_by(
        Slack.created.desc()).paginate(page, config.POSTS_PER_PAGE, False)
    return render_template('index.html', msgs=msgs)


@app.route('/user/<path:username>/', methods=['GET'])
def user(username, page=1):
    '''retrieve all msgs per user'''
    msgs = Slack.query.filter_by(username=username).order_by(
        Slack.created.desc())
    return render_template('user.html', msgs=msgs)


@app.route('/channel/<path:channel>/', methods=['GET'])
def channel(channel):
    '''retrieve all msgs per channel'''
    msgs = Slack.query.filter_by(channel=channel).order_by(
        Slack.created.desc())
    return render_template('user.html', msgs=msgs)


@app.route('/api/slackbot', methods=['POST'])
def outgoing_msg():
    '''get slack messages using outgoing webhook'''
    if request.form.get('token') == config.SLACK_WEBHOOK_SECRET:
        channel_name = request.form.get('channel_name')
        channel_id = request.form.get('channel_id')
        username = request.form.get('user_name')
        time = request.form.get('timestamp')
        timestamp = datetime.datetime.fromtimestamp(
            int(float(time))).strftime('%d/%m/%Y %H:%M:%S')
        text = request.form.get('text').strip(': ')
        text = text.replace('>', '', 1).replace('<', '', 1)

        # uncomment this block if you want to debug and show in console the retrieve data:
        # inbound_message = f"{timestamp} {username} in {channel_name} says: {text}"
        # print(inbound_message)

        # if get outgoing webhook response ok, userbot reply with this message:
        msg = f"_Hola {username} ! Gracias por compartirlo. " \
              "Puedes consultar tus aportes y de los demás en:_ " \
              "https://your-url.com/"

        send_message(channel_id, msg)

        slack_msg = Slack(
            username=username,
            content=text,
            channel=channel_name,
            channel_id=channel_id,
            timestamp=timestamp)

        db.session.add(slack_msg)
        db.session.commit()

    return Response(), 200


if __name__ == "__main__":
    app.run()
