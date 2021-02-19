import requests
import json
import os
import datetime as dt
from urllib.request import Request, urlopen


HOOK_URL = os.environ['HookUrl']
API_URL = os.environ['ApiUrl']


def webhook(code, url):
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "office.com" in HOOK_URL:
        # message information to display in Teams
        message = {
            "@context": "https://schema.org/extensions",
            "@type": "MessageCard",
            "themeColor": "64a837",
            "title": "System health check",
            "text": f"URL Checked  UTC time of **{now}**",
            "sections": [
                {
                    "facts": [
                        {
                            "name": "code",
                            "value": f"{code}"
                        },
                        {
                            "name": "URL: ",
                            "value": f"{url}"
                        }
                    ]
                }
            ]
        }
    elif "slack.com" in HOOK_URL:
        message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":heavy_check_mark: Service restored" if code >= 200 and code <= 220 else ":x: Service Unavailable",
                        "emoji": True
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"URL tested at {now}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"URL: {url}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": f"Success code: {code}" if code >= 200 and code <= 220 else f"Error code: {code}",
                        "emoji": True
                    }
                }
            ]
        }

    # request connection to messaging system
    request = Request(
        HOOK_URL,
        json.dumps(message).encode('utf-8'))

    # post message to messaging system
    response = urlopen(request)
    response.read()
        

def status_code(url):
    try:
        return requests.get(url).status_code
    except Exception as e:
        return e


def lambda_handler():
    websites = json.load(requests.get(API_URL))
    for (url, previous_response) in websites:
        code = status_code(url)
        if code != previous_response:
            # todo update websites
            webhook(url, code)


