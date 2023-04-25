try:
    import unzip_requirements
except ImportError:
    pass

import logging
import os

from slack_bolt import App, Ack
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

app = App(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    token=os.environ['SLACK_BOT_TOKEN'],
    process_before_response=True
)


def just_ack(ack: Ack):
    ack()


@app.message("hello")
def message_hello(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hey there <@{message['user']}>!"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Click Me"
                    },
                    "action_id": "button_click"
                },
            },
        ],
        text=f"Hey there <@{message['user']}>!"
    )


def action_button_click(say, body: dict):
    say(f"<@{body['user']['id']}> clicked the button")


app.action("button_click")(ack=just_ack, lazy=[action_button_click])


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)


if __name__ == '__main__':
    app.start()
