import requests
import confidential
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
from base64 import b64encode

debug = 2

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
    if (debug == 2): print(response.status_code)
    return response

def sendPhoto (chat_id, caption, parse_mode, photo_url, no_link_preview):
    ip = requests.get('https://api.ipify.org').text
    link='https://api.telegram.org/bot' + confidential.api_key + '/sendPhoto'
    params = {
                'chat_id': chat_id,
                'caption': caption,
                'parse_mode': parse_mode,
                'photo': 'http://' + str(ip) + '/' + photo_url,
                'disable_web_page_preview': no_link_preview,
                #this is hardcoded
                'disable_notification': False 
            }
    response = requests.post(link, json=params, timeout=2)
    print(response.text)
    if (debug == 2): print(response.status_code)
    return response

def getUpdates ():
    #take out ?offset=-1 to receive all messages
    link = 'https://api.telegram.org/bot' + confidential.api_key + '/getUpdates?offset=-1'
    response = requests.get(link, timeout=2)
    if (debug == 2): print(response.status_code)
    return response

# def upload_to_imgur (img_name):

#     headers = {"Authorization": "Client-ID " + confidential.imgur_id}

#     api_key = confidential.imgur_secret

#     url = "https://api.imgur.com/3/upload.json"

#     response = requests.post(
#         url, 
#         headers = headers,
#         data = {
#             'key': api_key, 
#             'image': b64encode(open(img_name, 'rb').read()),
#             'type': 'base64',
#             'name': 'iptv-screen.jpg',
#             'title': 'A screenshot'
#         }
#     )    

#     upres = json.loads(response.text)
#     return upres['data']['link']

def check_message (mes, id, store):

    #/start
    if (debug == 2): print(mes)
    if (mes.find('/start')!=-1):
        text = '🤖 @piemonte\_open\_vax\_bot by campa, il codice open source di questo bot è disponibile [qui](https://github.com/itscampa/piemonte-open-vax-bot/)\n\n💉 Usa /subscribe per essere avvisato dei cambiamenti agli open day vaccinali\n\n❌ Usa /unsubscribe per disiscriverti dalle notifiche'
        sendMessage(id, text, 'Markdown', True)
        check_message('/subscribe', id, store)

    #/subscribe
    elif (mes.find('/subscribe')!=-1):
        with open('mailing_list.txt', 'r+', encoding = 'utf-8') as ids, open('mailing_list_username.txt', 'a+', encoding = 'utf-8') as unames:
            if (ids.read().find(str(id)) != -1):
                sendMessage(id, 'Sei già iscritto alle notifiche! 😉', 'Markdown', True)
            else:
                ids.write(str(id) + '\n')
                unames.write(str(store) + '\n')
                sendMessage(id, 'D\'ora in poi riceverai i messaggi ✅', 'Markdown', True)

    #/unsubscribe
    elif (mes.find('/unsubscribe')!=-1):
        deluser('mailing_list.txt', id, True)

def check_website_change ():
    
    trigger = 0
    f = open("reference_page.html", "r+" , encoding = 'utf-8')
    g = open("./images/screenshot.png", "wb")
    
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=chrome-data")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=720,1080")
    chrome_options.add_argument("--hide-scrollbars")

    try:
        driver = webdriver.Chrome('./chromedriver',options=chrome_options)

        if (debug == 3 or debug == 2 or debug == 1): print ('Checking website')
        site_link = 'https://www.ilpiemontetivaccina.it/preadesione/#/'
        driver.get(site_link)

        element = driver.find_element_by_id("vday")
        html = element.get_attribute('innerHTML')
        if (debug == 3): print(html)
    except Exception as e:
        sendMessage(confidential.id_privatechat, str(e), 'Markdown', True)
        if (debug == 1): print(e)

    time.sleep(1)
    if (f.read() != html):
        f.seek(0)
        f.truncate(0)
        f.write(html)
        trigger = 1
        element.screenshot_as_png #to take the page to the rigth place

        #taking screenshot of "vday" section
        if (debug == 3 or debug == 2 or debug == 1): print('Taking screenshot')
        driver.execute_script("document.getElementById('outdated').innerHTML = '';")
        time.sleep(4)
        element_png = element.screenshot_as_png
        g.write(element_png)
        driver.quit()

    f.close()
    g.close()

    return trigger

def deluser (file, user, sendmessage):
    with open(file, 'r', encoding = 'utf-8') as ids:
            if (ids.read().find(str(user)) != -1):
                if (debug == 3 or debug == 2 or debug == 1): print('Found user (' + str(user) + '), now deleting, sendmessage=' + str(sendmessage))
                with open(file, 'r', encoding='utf-8') as f, open('temp.txt', 'w', encoding='utf-8') as g:
                    lines = f.readlines()
                    for i in lines:
                        if (i.rstrip() != str(user)):
                            g.write(i)

                with open(file, 'w', encoding='utf-8') as f, open('temp.txt', 'r', encoding='utf-8') as g:
                    lines = g.readlines()
                    for i in lines:
                        f.write(i)
                    if (sendmessage): sendMessage(user, 'Operazione completata ✅', 'Markdown', True)
    
            else:
                if (debug == 3 or debug == 2 or debug == 1): print('User (' + str(user) + ') to delete not found, sendmessage=' + str(sendmessage))
                if (sendmessage): sendMessage(user, 'Utente non trovato! 🔍', 'Markdown', True)
    

#-------------------------------------------------------------------------------------------
#MAIN

f = open("last_message_id.txt", "r+" , encoding = 'utf-8')

counter = 0

while True:
    try:
        time.sleep(0.5)
        counter = counter + 1
        counter = counter % 500
        response = getUpdates()
        a = json.loads(response.text)
        store = json.dumps(a['result'], indent=4, sort_keys=True)

        try:
            text = a['result'][0]['message']['text']
            message_id = a['result'][0]['message']['message_id']
            user_id = a['result'][0]['message']['chat']['id']
        except Exception as e:
            if (debug == 2): print('Error: ' + str(e).rstrip())
            sendMessage(confidential.id_privatechat, 'Error' + str(e), 'Markdown', True)
            time.sleep(1)
            continue

        # ______                                                  
        # | ___ \                                                 
        # | |_/ /   _ _ __   __ _ _ __  _   ___      ____ _ _   _ 
        # |    / | | | '_ \ / _` | '_ \| | | \ \ /\ / / _` | | | |
        # | |\ \ |_| | | | | (_| | | | | |_| |\ V  V / (_| | |_| |
        # \_| \_\__,_|_| |_|\__,_|_| |_|\__, | \_/\_/ \__,_|\__, |
        #                                __/ |               __/ |
        #                               |___/               |___/ 

        if (counter==1):
            if (check_website_change()):
                if (debug == 3 or debug == 2 or debug == 1): print('Something changed on ilpiemontetivaccina.it')
                with open('mailing_list.txt','r') as mailz:
                    lines = mailz.readlines()
                    for i in lines:
                        sendPhoto (i.rstrip(), '🚨 Hey! 🚨\nSembra ci siano novità su [ilpiemontetivaccina.it](https://www.ilpiemontetivaccina.it/preadesione/#/)', 'Markdown', 'screenshot.png', True)
            else:
                if (debug == 3 or debug == 2 or debug == 1): print('Nothing changed on ilpiemontetivaccina.it')
        #   ___                                  
        #  / _ \                                 
        # / /_\ \_ __  _____      _____ _ __ ___ 
        # |  _  | '_ \/ __\ \ /\ / / _ \ '__/ __|
        # | | | | | | \__ \\ V  V /  __/ |  \__ \
        # \_| |_/_| |_|___/ \_/\_/ \___|_|  |___/
                                                
        f.seek (0)
        history=f.read()
        
        #checking if last message has already been seen
        if (str(message_id) != history):
            if (debug == 2): print('New Message')
            check = 1 
        else:
            if (debug == 2): print('Same Message')
            check = 0

        #answer if it's a new message
        if (check):
            if (debug == 2): print('Answering!')
            f.seek (0)
            f.truncate(0)
            f.write(str(message_id))
            check_message(text, user_id, store)
            #sendMessage(confidential.id_privatechat, text, 'Markdown', True)

    except Exception as e:
        sendMessage(confidential.id_privatechat, str(e), 'Markdown', True)
        if (debug == 2): print(e)
