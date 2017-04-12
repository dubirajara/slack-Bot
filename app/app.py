import os
import datetime
from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from slackclient import SlackClient


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    basedir,
    'app.sqlite')
db = SQLAlchemy(app)


SLACK_TOKEN = ('YOUR SLACK BOT USER TOKEN', None)

slack_client = SlackClient(SLACK_TOKEN)
SLACK_WEBHOOK_SECRET = 'YOUR SLACK WEBHOOK TOKEN'


class Slack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True)
    content = db.Column(db.String(500), index=True)
    channel = db.Column(db.String(100), index=True)
    timestamp = db.Column(db.String(100), index=True)

    def __repr__(self):
        return '<User %r>' % (self.username)


def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        as_user="true:",
        text=message,

    )


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel_name = request.form.get('channel_name')
        channel_id = request.form.get('channel_id')
        username = request.form.get('user_name')
        time = request.form.get('timestamp')
        timestamp = datetime.datetime.fromtimestamp(
            int(float(time))).strftime('%d-%m-%Y %H:%M:%S')
        text = request.form.get('text')

        if 'http://' in text.lower():
            inbound_message = "{} {} in {} says: {}".format(
                timestamp,
                username,
                channel_name,
                text
                 )
            print(inbound_message)
            msg = "Hello {} ! It worked! Gracias por compartirlo.".format(
                username)
            send_message(channel_id, msg)

            slack_msg = Slack(
                username=username,
                content=text,
                channel=channel_name)
            db.session.add(slack_msg)
            db.session.commit()

        return Response(), 200


@app.route('/')
def home():
    msgs = Slack.query.all()
    return render_template('index.html', msgs=msgs)


if __name__ == "__main__":
    app.run(debug=True)
