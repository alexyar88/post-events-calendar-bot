import os
from datetime import datetime, timedelta
import requests

CMC_TOKEN = os.environ['CMC_TOKEN']
TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
TG_CHAT_ID = os.environ['TG_CHAT_ID']


def get_events():
    date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    params = {
        'dateRangeStart': date,
        'dateRangeEnd': date,
        'sortBy': 'trending_events',
        'showViews': 'true',
        'showVotes': 'true',
    }
    headers = {
        'Accept-Encoding': 'deflate, gzip',
        'Accept': 'application/json',
        'x-api-key': CMC_TOKEN
    }
    cmc_api_url = 'https://developers.coinmarketcal.com/v1/events'
    resp = requests.get(cmc_api_url, params=params, headers=headers)

    return resp.json()


def parse_event_list(events_json, max_coins=2):
    events = []
    for event in events_json:
        title = event['title']['en']
        coins = ', '.join([coin['fullname'] for coin in event['coins'][:max_coins]])
        event = f'{coins} &#8212; {title}'
        events.append(event)

    return events


def create_post_text(events):
    date = (datetime.now() + timedelta(days=1)).strftime('%-d %b')

    if len(events) >= 5:
        post = f'Top-5 tomorrow events, {date}:\n\n'
    else:
        post = f'Top tomorrow events, {date}:\n\n'

    for i, event in enumerate(events[:5]):
        post += f'{i + 1}. '
        post += event
        post += '\n\n'

    return post


def send_post(post):
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
    params = {
        'chat_id': TG_CHAT_ID,
        'text': post,
        'parse_mode': 'HTML',
    }

    requests.get(url, params=params)


def main():
    events_json = get_events()['body']
    events = parse_event_list(events_json)
    post = create_post_text(events)
    send_post(post)


if __name__ == '__main__':
    main()
