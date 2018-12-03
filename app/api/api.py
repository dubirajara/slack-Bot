from flask import Blueprint, jsonify, abort
from sqlalchemy import desc

from app.models import Slack


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/list/', methods=['GET'])
def api_list():
    '''api to retrieve all msgs json serializer'''
    messages = []
    for message in Slack.query.order_by(desc(Slack.created)).all():
        messages.append({
            'id': message.id,
            'username': message.username,
            'content': message.content,
            'channel': message.channel,
            'channel_id': message.channel_id,
            'timestamp': message.timestamp,
            'created': message.created
        })

    return jsonify(messages)


@api.route('/<int:id>/', methods=['GET'])
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


@api.route('/user/<path:username>/', methods=['GET'])
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
    if messages:
        return jsonify(messages)

    else:
        abort(404)


@api.route('/channel/<path:channel>/', methods=['GET'])
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
    if messages:
        return jsonify(messages)

    else:
        abort(404)
