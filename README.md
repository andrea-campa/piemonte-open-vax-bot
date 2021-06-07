# Piemonte Open Vax Bot  
A telegram bot that sends a notification whenever a new COVID-2019 vaccines open day is published on the Piedmont website: [ilpiemontetivaccina.it](https://www.ilpiemontetivaccina.it/preadesione/#/)

---
## Requirements
You can use the *setup.sh script* in the directory or:

- Install the python requirements with ``python3 -m pip install -r requirements.txt``

- Install chromedriver

- Install xvfb

- You'll also need to create some blank files in the directory:
    - last_message_id.txt
    - confidential.py
    - mailing_list.txt
    - mailing_list_username.txt
    - reference_page.html  