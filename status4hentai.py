# -*- coding: utf-8 -*-
import csv
import json
import re
import pandas
import logging
import smtplib
import requests
import datetime
from getpass import getpass
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

#Error handling
FORMAT = "%(asctime)s |%(levelname)s |%(message)s"
logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a", format=FORMAT)

#Time stemp
def current_time():
    today = datetime.datetime.now()
    return today.strftime("%Y-%m-%d %H:%M")

#Program Status
def program_status( event=() ):
    ststus_header = ["Time", "Status"]
    status_table =  [current_time(), event]
    status_output = pandas.DataFrame(data=[status_table], columns=ststus_header)
    status_output.to_csv("status_program.csv", mode="w", index=False)
    return status_table

#Sign in fuction
def configuration( update_config=() ):
    if bool(update_config) is False:
        #Reading configuration file
        try:
            with open("config.json", "r") as configuration_file:
                #Return dictionary
                return json.load(configuration_file)
        #If file not found
        except FileNotFoundError:
            #Stamp
            time_initialize = current_time()
            #Initialization
            print("Configuration not found, please initialize.\r\n")
            ipb_member_id = input("Please enter the ipb_member_id: ")
            ipb_pass_hash = getpass("Please enter the ipb_pass_hash: ")
            ipb_session = getpass("Please enter the ipb_session_id: ")
            #Dictionary
            initialize_config = {
                "last_update_time":time_initialize,
                "ipb_member_id":ipb_member_id,
                "ipb_pass_hash":ipb_pass_hash,
                "ipb_session_id":ipb_session
                }
            #Save configuration file
            with open("config.json", "w") as configuration_file:
                json.dump(initialize_config, configuration_file, indent=2)
                print("Configuration saved successfully.")
                #Return dictionary after initialize
                return initialize_config
    #Update configuration file
    elif bool(update_config) is True:
        with open("config.json", "w") as configuration_file:
            json.dump(update_config, configuration_file, indent=2)
            #Return dictionary after update
            return update_config

#Sign in e-hentai, and get HTML respon
def hentai6home( pass_hash_renew=(), session_renew=() ):
    #Global
    login_headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68"}
    hentaiathome = "https://e-hentai.org/hentaiathome.php"
    #Cookie
    cookie_generate = configuration(update_config=False)
    ipbm = cookie_generate["ipb_member_id"]
    ipbp = cookie_generate["ipb_pass_hash"]
    ibps = cookie_generate["ipb_session_id"]
    #Sign in
    if bool(pass_hash_renew) is False:
        #Cookies
        login_cookies = {"ipb_member_id":ipbm, "ipb_pass_hash":ipbp, "ipb_session_id":ibps}
        #Get hentaiathome page
        try:
            hentai_respon = requests.get(hentaiathome, headers=login_headers, cookies=login_cookies, timeout=5)
            if hentai_respon.status_code == 200:
                hentai_respon.close()
                return hentai_respon.content
            else:
                hentai_respon.close()
                return hentai_respon.status_code
        except requests.exceptions.Timeout as error_time:
            logging.warning(error_time)
            return False
        except Exception as error_status:
            logging.exception(error_status)
            return False
    #Sign in again after update
    elif bool(pass_hash_renew) is True:
        update_config = cookie_generate
        update_config["ipb_pass_hash"] = pass_hash_renew
        update_config["ipb_session_id"] = session_renew
        #Stamp
        time_renew_hash = current_time()
        update_config["last_update_time"] = time_renew_hash
        #Update configuration
        configuration(update_config)
        login_cookies = {"ipb_member_id":ipbm, "ipb_pass_hash":pass_hash_renew, "ipb_session_id":session_renew}
        try:
            hentai_respon = requests.get(hentaiathome, headers=login_headers, cookies=login_cookies, timeout=10)
            if hentai_respon.status_code == 200:
                hentai_respon.close()
                return hentai_respon.content
            else:
                hentai_respon.close()
                return hentai_respon.status_code
        except requests.exceptions.Timeout as error_time:
            logging.warning(error_time)
            return False
        except Exception as error_status:
            logging.exception(error_status)
            return False

#Parsing HTML and get status table
def hentai_status( output_dataframe=(), disalbe_retry=() ):
    #Get respon
    h6h_respon = hentai6home(pass_hash_renew=False)
    #Get respon correct
    if type(h6h_respon) is bytes:
        #Parsing HTML
        hentai_soup = BeautifulSoup(h6h_respon,"html.parser")
        soup_table = hentai_soup.find("table",{"class":"hct"})
        #Check status table
        if soup_table is not None:
            #Get table correct
            pass
        #If status table not founf
        elif soup_table is None:
            #Try to get login table
            login_table = hentai_soup.find("div",{"class":"d"})
            if login_table is not None:
                #Found login table, maybe the cookie is expired
                if bool(disalbe_retry) is False:
                    #Let's try again
                    print("Data expired, please enter data again.\r\n")
                    pass_hash_renew = getpass("Please enter the ipb_pass_hash: ")
                    session_renew = getpass("Please enter the ipb_session_id: ")
                    #Update data, try again
                    h6h_respon = hentai6home(pass_hash_renew, session_renew)
                    #Again, parsing HTML
                    hentai_soup = BeautifulSoup(h6h_respon,"html.parser")
                    #Get status table
                    soup_table = hentai_soup.find("table",{"class":"hct"})
                #Disalbe login retry
                elif bool(disalbe_retry) is True:
                    msg_disable = "Login retry is disable."
                    logging.warning(msg_disable)
                    return True
            #If login table not found
            elif login_table is None:
                msg_prompt = "Error occurred when parsing."
                logging.error(msg_prompt)
                return False
    #If server respon status not 200
    elif type(h6h_respon) is int:
        msg_request = (f"HTTP Status Code: {h6h_respon}")
        logging.warning(msg_request)
        return False
    #If error occurred when request
    elif type(h6h_respon) is bool:
        return False
    #Cooking
    try:
        #Parsing table
        status_table = soup_table.find_all("tr")[1:]
        soup_content = list()
        for tr in status_table:
            soup_content.append([td.text.replace("\n","").replace("\xa0","") for td in tr.find_all("td")])
        #Cooking method
        if bool(output_dataframe) is False:
            #Revome character
            for i, content_element in enumerate(soup_content):
                content_element = [element.replace(",","").replace(" / min","").replace(" / day","") for element in content_element]
                soup_content[i] = content_element
            return soup_content
        #Pandas can Cooking
        elif bool(output_dataframe) is True:
            soup_package = [th.text.replace("\n","") for th in soup_table.find("tr").find_all("th")]
            soup_frame = pandas.DataFrame(data=soup_content, columns=soup_package)
            return soup_frame
    #Overcooked
    except Exception as error_status:
        logging.exception(error_status)
        return False

#Mail alert
def soup_alert( soup_menu, sender_account=(), sender_password=(), receiver=(), disalbe_phone_book=() ):
    #Read mail set from book
    if bool(disalbe_phone_book) is False:
        #Load mail configuration
        mail_config = configuration(update_config=False)
        #Try to read configuration
        try:
            sender_account = mail_config["sender"]
            sender_password = mail_config["scepter"]
            receiver = mail_config["receiver"]
        #If configuration not found
        except KeyError:
            #Initialization
            update_config = mail_config
            print("Mail Configuration not found, please initialize.\r\n")
            #Sender
            sender_account = input("Please enter the sender account: ")
            update_config["sender"] = sender_account
            #Password
            sender_password = getpass("Please enter the sender password: ")
            update_config["scepter"] = sender_password
            #Receiver
            receiver = input("Please enter the receiver address: ")
            update_config["receiver"] = receiver
            #Stamp
            time_mail_config_add = current_time()
            update_config["last_update_time"] = time_mail_config_add
            print("Configuration saved successfully.")
            #Update configuration
            configuration(update_config)
    #Directly setting email configuration
    elif bool(disalbe_phone_book) is True:
        pass
    #Sending Mail
    time_sending = current_time()
    msg = MIMEText(soup_menu)
    msg["Subject"] = (f"Hentai@Home Offline Alert {time_sending}")
    msg["From"] = sender_account
    msg["To"] = receiver
    #Mail server
    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(sender_account, sender_password)
        #Sending Mail
        smtpserver.sendmail(sender_account, [receiver], msg.as_string())
        close_msg = smtpserver.quit()
        print(close_msg)
        return None
    except Exception as error_status:
        logging.exception(error_status)
        print("Error occurred when sending mail")
        return 404

#2021_03_06