import os

from flask import Flask, request, jsonify, make_response
from twilio.rest import TwilioRestClient

APP = Flask(__name__)


@APP.route('/_status/', methods=['GET'])
def status():
    return jsonify({'message': 'All systems go.'})


@APP.route('/cloudmailin/echo/', methods=['POST'])
def cloudmailin_echo():
    return make_response(request.data), 503


@APP.route('/cloudmailin/', methods=['POST'])
def cloudmailin():
    data = request.json

    subject = data['headers']['Subject']
    plain_body = data['plain']
    html_body = data['html']

    for keyword in os.environ['SEARCH_KEYWORDS'].split(','):
        if keyword_in_email(keyword, subject, plain_body, html_body):
            send_text_alert(keyword, subject)
            return jsonify({'message': 'SMS sent'})

    return jsonify({'message': 'OK, email did not match search.'})


def keyword_in_email(keyword, subject, plain_body, html_body):
    keyword = keyword.lower()
    return (keyword in subject.lower()
            or keyword in plain_body.lower()
            or keyword in html_body.lower())


def send_text_alert(keyword, subject):
    account = os.environ['TWILIO_SID']
    token = os.environ['TWILIO_AUTH_TOKEN']
    from_number = os.environ['TWILIO_FROM_NUMBER']
    alert_number = os.environ['ALERT_NUMBER']

    client = TwilioRestClient(account=account, token=token)

    client.messages.create(
        from_=from_number,
        to=alert_number,
        body='Freecycle search "{}" : "{}"'.format(keyword, subject)
    )


if __name__ == '__main__':
    APP.run()
