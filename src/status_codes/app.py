import requests
import json
import os
import logging
import datetime as dt
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# HOOK_URL = os.environ['HookUrl']
HOOK_URL = 'https://hooks.slack.com/services/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'

# set logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
                        "text": f"Error code: {code}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Down since: ",
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
    try:
        response = urlopen(request)
        response.read()
        logger.info("Message posted")
    except HTTPError as err:
        logger.error(f"Request failed: {err.code} {err.reason}")
    except URLError as err:
        logger.error(f"Server connection failed: {err.reason}")



def status_code(url):
    try:
        return requests.get(url).status_code
    except Exception as e:
        return e


def lambda_handler(event, context):
    url = 'https://www.northampton.gov.uk'
    code = status_code(url)
    webhook(code, url)
    print (str(url) + ": " + str(code))

    # urls = ['google.com', 'bing.com', 'lgss-digital.co.uk']
    # for url in urls:
    #     code = status_code(url)
    #     webhook(code, url)
    #     print (str(url) + ": " + str(code))


lambda_handler(None, None)