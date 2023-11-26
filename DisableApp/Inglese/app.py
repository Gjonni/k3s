import requests
import os
import json
from datetime import datetime
import smtplib
from email.message import EmailMessage
import logging
import sys


##### ENVIROMENT
username =  os.environ.get('INGLESE_USER')
password =  os.environ.get('INGLESE_PASSOWRD')
hostname = os.environ.get('INGLESE_URL') 
email_address = os.environ.get('EMAIL_ADDRESS') 
email_password = os.environ.get('EMAIL_PASSWORD')
email_host = os.environ.get('EMAIL_HOST') 

##### LOGGING
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger("route.response.time")



def get_token():
    r = requests.post(f'https://{hostname}/autenticazione', json={
    "email": username ,
    "password": password ,
}).json()
    return {  'Authorization': 'Bearer ' + r['token']}

def get_lezione():
    results = []
    r = requests.get(f'https://{hostname}/lezioni/prenotabili', headers=token).json()
    for item in r:
        if "13:00" in item['inizioLezione'] and "elena.nannicini@par-tec.it" in item['docente']:
            date = datetime.strptime( item['dataLezione'], "%Y-%m-%d").weekday()
            if date == 2:
                results.append(item)
    logger.debug(f"{results}")
    return results

def send_mail(lezioni):
    elements = "\r\n".join(f"il {i['dataLezione']} dalle ore {i['inizioLezione']} alle {i['fineLezione']}" for i in lezioni)
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Ecco le Lezioni di inglese prenotate!'
        msg['From'] = email_address
        msg['To'] = 'giovanni.filice@icloud.com'
        msg.set_content(f"Le seguenti lezioni sono state prenotate \r\n {elements}")
        with smtplib.SMTP(email_host, 587) as smtp:
            smtp.starttls()
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
    except requests.exceptions.HTTPError as e:
        logger.debug(f"{e}")

def main():
    results = []
    for lezione in get_lezione():
        try: 
            r200 = requests.get(f"https://{hostname}/lezioni/prenota/{lezione['idLezione']}" , headers=token)
            if r200.status_code == 200:
                for item in r400:
                    results.append(item)
                send_mail(results)
            r200.raise_for_status()
            logger.debug(f"{results}")
            return results
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(e.response.text)
            if e.response.status_code == 400:
                r400 = requests.get(f'https://{hostname}/lezioni/prenotazioni/' , headers=token).json()
                for item in r400:
                   results.append(item)
                send_mail(results)
            logger.debug(f"{results}")
            return results        

            

if __name__ == "__main__":
  token=get_token()
  main()



