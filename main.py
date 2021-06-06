import requests
from bs4 import BeautifulSoup
from requests.api import get
import confidential
import json
import smtplib
import time 

def sendMessage (chat_id, text, parse_mode, no_link_preview):
    link='https://api.telegram.org/bot' + confidential.api_key + '/sendMessage'
    params = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': no_link_preview,
                #this is hardcoded
                'disable_notification': False 
            }
    response = requests.post(link, json=params, timeout=2)
    print(response.status_code)
    return response

def getUpdates ():
    #take out ?offset=-1 to receive all messages
    link = 'https://api.telegram.org/bot' + confidential.api_key + '/getUpdates?offset=-1'
    response = requests.get(link, timeout=2)
    print(response.status_code)
    return response

def check_message (mes):
    print(mes)
    if (mes.find('/help')!=-1):
        sendMessage(confidential.id_privatechat, '*the fuck d\'ya want*', 'Markdown', True)
    elif (mes.find('/ping')!=-1):
        sendMessage(confidential.id_privatechat, '*ping pong, king kong*', 'Markdown', True)

def check_pinebook ():
    print ('Checking pinebook')
    text='14″ PINEBOOK Pro LINUX LAPTOP (ANSI, US Keyboard) [Out of Stock]' 
    product_link = 'https://pine64.com/product/14%E2%80%B3-pinebook-pro-linux-laptop-ansi-us-keyboard/'
    page=requests.get(product_link)
    soup = BeautifulSoup (page.content, 'html.parser')
    #print(soup.prettify())
    html = soup.find('h1').getText()

    if (html!=text):

        #do things
        print('Something changed!')
        text = 'Something changed on the PineBook page you were watching \n[link here](' + product_link + ')'
        response = sendMessage (confidential.id_privatechat, text, 'Markdown', True)
        return response

    else:
        print('All the same :(')
        return 0


f = open("last_message_id.txt", "r+" , encoding = 'utf-8')
counter = 0

while True:
    time.sleep(0.5)
    counter = counter + 1
    counter = counter % 100
    response = getUpdates()
    a = json.loads(response.text)
    #print(json.dumps(a['result'], indent=4, sort_keys=True))

    text = a['result'][0]['message']['text']
    username = a['result'][0]['message']['chat']['username']
    message_id = a['result'][0]['message']['message_id']
    
    # ______                                                  
    # | ___ \                                                 
    # | |_/ /   _ _ __   __ _ _ __  _   ___      ____ _ _   _ 
    # |    / | | | '_ \ / _` | '_ \| | | \ \ /\ / / _` | | | |
    # | |\ \ |_| | | | | (_| | | | | |_| |\ V  V / (_| | |_| |
    # \_| \_\__,_|_| |_|\__,_|_| |_|\__, | \_/\_/ \__,_|\__, |
    #                                __/ |               __/ |
    #                               |___/               |___/ 

    if (counter==1):
        check_pinebook ()

    #   ___                                  
    #  / _ \                                 
    # / /_\ \_ __  _____      _____ _ __ ___ 
    # |  _  | '_ \/ __\ \ /\ / / _ \ '__/ __|
    # | | | | | | \__ \\ V  V /  __/ |  \__ \
    # \_| |_/_| |_|___/ \_/\_/ \___|_|  |___/
                                                                                 
    f.seek (0)
    history=f.read()
        
    if (str(message_id) != history):
        print('New Message')
        check = 1 
    else:
        print('Same Message')
        check = 0

    if (username==confidential.tg_username and check):
        print('It\'s you!')
        f.seek (0)
        f.write(str(message_id))
        check_message(text)
        #sendMessage(confidential.id_privatechat, text, 'Markdown', True)


