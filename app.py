# coding=utf-8

from flask import Flask, request
import requests
import json
import urllib.request
import urllib.parse
import urllib3

http = urllib3.PoolManager()
# r = http.request('GET', 'http://docs.python.org')
# htmlSource = r.data

requests.packages.urllib3.disable_warnings()

import ssl



app = Flask(__name__)
app.app_context().push()

users = dict()
    
@app.route("/")
def hello():
    return "Hello, World!"

# dict_keys(['instance_id', 'event', 'data'])

@app.route("/test", methods=['POST'])
def runserver():
    # print(request.json['instance_id'])
    # print(request.json['event'])
    res_data = request.json['data']
    # print(type(res_data))

    try:
        if type(res_data) is dict:
            # print(res_data.keys())
            msg_lst = res_data['messages']
            msg = msg_lst[0]
            name = msg['pushName']
            msg_text = msg['message']['conversation']
            phone_no = msg['key']['remoteJid'][:12]

            if phone_no not in users.keys() and ( msg_text.lower().strip() == 'hare krishna' or msg_text.lower().strip() == 'hare krisna' or msg_text.lower().strip() == 'hare krsna'):
                users[phone_no] = [1, True, name]
                encoded_msg = urllib.parse.quote('*Hare Krishna {}!* \n\nYou are now subscribed to receive daily Bhagvad Gita shlokas. \n\nYou will receive a message every day at 5:00 AM. \n\nYou can unsubscribe anytime by sending "unsubscribe" to this number. \n\nYour journey of self realisation starts now.'.format(name))
                return_webhook_url = 'https://betablaster.in/api/send.php?number={}&type=text&message={}&instance_id=626A3E916DE40&access_token=5a30cf125df4e52a36ce4daa0403885f'.format(phone_no, encoded_msg)
                print(return_webhook_url)
                # urllib.request.urlopen(return_webhook_url)
                r=http.request('GET', return_webhook_url)
                print(r.data)

            elif phone_no in users.keys() and ( msg_text.lower().strip() == 'hare krishna' or msg_text.lower().strip() == 'hare krisna' or msg_text.lower().strip() == 'hare krsna'):
                users[phone_no] = [users[phone_no][0], True, name]
                encoded_msg = urllib.parse.quote('*Hare Krishna {}!* \n\nYou are now subscribed to receive daily Bhagvad Gita shlokas. \n\nYou will receive a message every day at 5:00 AM. \n\nYou can unsubscribe anytime by sending "unsubscribe" to this number. \n\nYour journey of self realisation starts now.'.format(name))
                return_webhook_url = 'https://betablaster.in/api/send.php?number={}&type=text&message={}&instance_id=626A3E916DE40&access_token=5a30cf125df4e52a36ce4daa0403885f'.format(phone_no, encoded_msg)
                print(return_webhook_url)
                r=http.request('GET', return_webhook_url)
                print(r.data)


            elif phone_no in users.keys() and msg_text.lower().strip() == 'unsubscribe':
                users[phone_no][1] = False
                encoded_msg = urllib.parse.quote('You have been unsubscribed from Bhagavad Gita notifications. \n\nYou can resubscribe anytime by sending "hare krishna" to this number.')
                return_webhook_url = 'https://betablaster.in/api/send.php?number={}&type=text&message={}&instance_id=626A3E916DE40&access_token=5a30cf125df4e52a36ce4daa0403885f'.format(phone_no, encoded_msg)
                print(return_webhook_url)
                r=http.request('GET', return_webhook_url)
                print(r.data)


    except:
        pass



    print(users)
    return "Hello, World!"

chapter_shlokas = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78]

def getChSh(n):
    ch = 1
    for n_schlokas in chapter_shlokas:
        if(n-n_schlokas > 0):
            n = n - n_schlokas
            ch = ch + 1
    
    return (ch, n);

@app.route("/init", methods=['GET'])
def print_date_time():
    for phone_no in users.keys():
        user_data = users[phone_no];
        if(user_data[1]):
            ch, sh = getChSh(user_data[0]);
            URL = 'https://bhagavadgitaapi.in/slok/{}/{}'.format(ch, sh)
            print(URL)
            page = requests.get(URL)

            result = json.loads(page.text)

            wrd_by_wrd_translation = ''
            commentary = ''
            message_text = ''
            if('No Commentary' in result['siva']['ec']):
                wrd_by_wrd_translation = result['siva']['ec'][:(result['siva']['ec'].find('No Commentary'))].replace('?', '')   
                message_text = result['slok'] + '\n\n' + result['transliteration'] + '\n\nCommentary by ' + result['siva']['author'] + '\n\nTranslation: ' + result['siva']['et'] + '\n\nWord By Word Meaning:' + wrd_by_wrd_translation

                
            else:
                wrd_by_wrd_translation = result['siva']['ec'][:(result['siva']['ec'].find('Commentary'))].replace('?', '')                
                commentary =  result['siva']['ec'][(result['siva']['ec'].find('Commentary')) + (11) : ].replace('?', '')   
                message_text = result['slok'] + '\n\n' + result['transliteration'] + '\n\nCommentary by ' + result['siva']['author'] + '\n\nTranslation: ' + result['siva']['et'] + '\n\nWord By Word Meaning:' + wrd_by_wrd_translation + '\n\nCommentary: ' + commentary


            encoded_msg = urllib.parse.quote(message_text)
            return_webhook_url = 'https://betablaster.in/api/send.php?number={}&type=text&message={}&instance_id=626A3E916DE40&access_token=5a30cf125df4e52a36ce4daa0403885f'.format(phone_no, encoded_msg)
            print(return_webhook_url)
            r=http.request('GET', return_webhook_url)
            print(r.data)
            users[phone_no][0] = users[phone_no][0] + 1

    return ""


if __name__ == "__main__":
    # sched = BackgroundScheduler()
    # sched.start()
    # sched.add_job(print_date_time, 'interval', seconds=40)
    app.run(debug=True)
    

