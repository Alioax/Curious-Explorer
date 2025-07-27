import requests

from http.server import BaseHTTPRequestHandler
from datetime import datetime


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        CLIENT_ID = "urBJ73Tg3W8WO5cH-wKErA"
        SECRET_KEY = "_jaI7Lelz3U2lvTp7empDsrCQgqz3w"

        BOT_TOKEN = '5380868349:AAEeNmOZyaNcl2TXV6J_iO4xBJKr6w-G2ZQ'
        REPEAT_CONTROL_BOT_TOKEN = '5489350111:AAEudYL38-s7IopCWY45WooCdOK-JngVLSE'

        TARGET_CHANNEL_ID = -1001752203532
        CACHE_CHANNEL_ID = -1001770134425

        reddit_acc_data = {
            'grant_type': 'password',
            'username': 'alioax',  # reddit's account username
            'password': 'o91759o9576'  # reddit's account password
        }

        subreddit = "midjourney"
        listing = "hot"  # listing category
        limit = "10"  # posts to check

        def send(method, caption, data="", bot_token=BOT_TOKEN, target=TARGET_CHANNEL_ID):
            if method == "sendMessage":
                payload = {'chat_id': target, 'text': caption}
            if method == "sendPhoto":
                payload = {'chat_id': target,
                           'caption': caption, 'photo': data, }
            if method == "sendVideo":
                payload = {'chat_id': target,
                           'caption': caption, 'video': data, }
            url = "https://api.telegram.org/bot" + \
                str(bot_token) + "/" + str(method)
            r = requests.get(url, params=payload)
            if (r.status_code) == 200:
                print("a message has been sent.")
            else:
                print(f"message hasn't been sent, error: {r.text}")

        def getUpdates(token, empty=False):
            requestURL = f'https://api.telegram.org/bot{token}/getUpdates'
            if empty:
                payload = {'offset': -1}
                r = requests.get(requestURL, params=payload)
            else:
                payload = {'limit': 20}
                r = requests.get(requestURL)
            return r

        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

        headers = {'User-Agent': 'MyAPI/0.0.1'}
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=reddit_acc_data, headers=headers)

        TOKEN = res.json()['access_token']

        headers['Authorization'] = f'bearer {TOKEN}'

        res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/{listing}?limit={limit}',
                           headers=headers)

        posts = res.json()['data']['children']

        names_sent = getUpdates(BOT_TOKEN)
        names_sent = [names_sent.json()['result'][x]['channel_post']['text']
                      for x in range(0, len(names_sent.json()['result']))]

        for post in posts:
            name = post['data']['name']
            if name not in names_sent:
                send('sendMessage', name, bot_token=REPEAT_CONTROL_BOT_TOKEN,
                     target=CACHE_CHANNEL_ID)
                if 'reddit_video_preview' in post['data']['preview']:
                    send('sendVideo', post['data']['title'], post['data']
                         ['preview']['reddit_video_preview']["fallback_url"])
                else:
                    if str(post['data']['url_overridden_by_dest']).endswith('gif'):
                        send('sendVideo', post['data']['title'],
                             post['data']['url_overridden_by_dest'])
                    else:
                        send('sendPhoto', post['data']['title'],
                             post['data']['url_overridden_by_dest'])
            else:
                print('denied a repeated message')
        print('Code Finished! Bye World for a few hours.')
        return
