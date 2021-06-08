import requests
import confidential

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
    if (debug == 2): print(str(chat_id) + ': status ' + str(response.status_code))
    return response
    

#-------------------------------------------------------------------------------------------
#MAIN

f = open("last_message_id.txt", "r+" , encoding = 'utf-8')

counter = 0

while True:
    print('\n1. To send message to subscribers\n2. To exit')
    select = input()
    if (select=='1'):
        print('Insert the update you want to send everyone')
        text = input()
        print('Insert the mailing list you want to use')
        mailing = input()
        try:
            with open(str(mailing).rstrip(),'r') as mailz:
                lines = mailz.readlines()
                for i in lines:
                    sendMessage (i.rstrip(), '🔧 Update 🔧\n' + text, 'Markdown', True)
        except FileNotFoundError:
            print('Error: Insert valid filename')
    elif (select=='2'):
        exit()