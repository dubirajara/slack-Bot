import datetime
from flask import Flask, render_template, request, Response, jsonify, abort
from sqlalchemy import desc
from slackclient import SlackClient
from config import Config
import bleach
from models import db, Slack


app = Flask(__name__)
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
    msgs = Slack.query.order_by(
        Slack.created.desc()).paginate(page, config.POSTS_PER_PAGE, False)
    return render_template('index.html', msgs=msgs)


@app.route('/user/<path:username>/', methods=['GET'])
def user(username, page=1):
    msgs = Slack.query.filter_by(username=username).order_by(
        Slack.created.desc())
    return render_template('user.html', msgs=msgs)


@app.route('/channel/<path:channel>/', methods=['GET'])
def channel(channel):
    msgs = Slack.query.filter_by(channel=channel).order_by(
        Slack.created.desc())
    return render_template('user.html', msgs=msgs)


@app.route('/api/list/', methods=['GET'])
def api_list():
    '''api to retrieve all msgs json serializer'''
    messages = []
    for message in Slack.query.order_by(Slack.created.desc()).all():
        messages.append({
            'id': message.id,
            'username': message.username,
            'content': message.content,
            'channel': message.channel,
            'channel_id': message.channel_id,
            'timestamp': message.timestamp,
            'created': message.created
        })
    response = jsonify(messages)
    return response


@app.route('/api/list/<int:id>/', methods=['GET'])
def api_id(id):
    '''api to retrieve a msg per id json serializer'''
    message = Slack.query.filter_by(id=id).first()
    if message:
        response = jsonify({
            'id': message.id,
            'username': message.username,
            'content': message.content,
            'channel': message.channel,
            'channel_id': message.channel_id,
            'timestamp': message.timestamp,
            'created': message.created
        })

        return response

    else:
        abort(404)


@app.route('/api/list/<path:username>/', methods=['GET'])
def api_username(username):
    messages = []
    for message in Slack.query.filter_by(username=username):
        messages.append({
            'id': message.id,
            'username': message.username,
            'content': message.content,
            'channel': message.channel,
            'channel_id': message.channel_id,
            'timestamp': message.timestamp,
            'created': message.created
        })
    response = jsonify(messages)
    return response


@app.route('/api/list/channel/<path:channel>/', methods=['GET'])
def api_channel(channel):
    messages = []
    for message in Slack.query.filter_by(channel=channel):
        messages.append({
            'id': message.id,
            'username': message.username,
            'content': message.content,
            'channel': message.channel,
            'channel_id': message.channel_id,
            'timestamp': message.timestamp,
            'created': message.created
        })
    response = jsonify(messages)
    return response


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

        msg = f"_Hola {username} ! Gracias por compartirlo. " \
            "Puedes consultar tus aportes y de los demás en:_ " \
            "https://pythonmadrid.herokuapp.com/"

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
