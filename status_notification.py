# -*- coding: utf-8 -*-
import sys
import time
import pandas
import logging
import schedule
import status4hentai
from getpass import getpass

#Scheduled Config, Minutes
scheduled_time = 30

#Email configuration Mode
disalbe_phone_book = False
#Email configuration
if bool(disalbe_phone_book) is True:
    sender = "example@gmail.com"
    scepter = "••••••••••••••••"
    receiver = "receiver@gmail.com"
elif bool(disalbe_phone_book) is False:
    mail_config = status4hentai.configuration(update_config=False)
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
        time_mail_config_add = status4hentai.current_time()
        update_config["last_update_time"] = time_mail_config_add
        print("Configuration saved successfully.")
        #Update configuration
        status4hentai.configuration(update_config)

#Error handling
FORMAT = "%(asctime)s |%(levelname)s |%(message)s"
logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a", format=FORMAT)

#Notification function
def notification():
    #Spoon
    spoon_enis = ["ID","Created","Client IP","Port","Version","Max Speed","Country"]
    spoon_zwei = ["Files Served","Trust","Quality","Hitrate","Hathrate"]
    #Set header
    error_header = ["Last Update Time","Error Status"]
    #Get time
    timestamp_event = status4hentai.current_time()
    #Get parsing result, as DataFrame
    status_frame = status4hentai.hentai_status(output_dataframe=True, disalbe_retry=False)
    #Check
    if type(status_frame) is bool:
        #If return False, means Error
        if status_frame is False:
            #Message
            error_message = "Error occurred when parsing."
            print(f"{timestamp_event} | {error_message}")
            #Save Status
            error_status = [timestamp_event, error_message]
            cold_soup = pandas.DataFrame(data=[error_status], columns=error_header)
            cold_soup.to_csv("status_monitor.csv", mode="w", index=False)
        #If return True, means Unable to login E-Hentai, and retry is disable
        elif status_frame is True:
            #Message
            soup_menu = "Unable to login E-Hentai, Login retry is disable."
            print(f"{timestamp_event} | {soup_menu}")
            #Email configuration
            if bool(disalbe_phone_book) is False:
                status4hentai.soup_alert(soup_menu)
            elif bool(disalbe_phone_book) is True:
                status4hentai.soup_alert(soup_menu, sender_account, sender_password, receiver, disalbe_phone_book=True)
            #Save Status
            error_status = [timestamp_event, soup_menu]
            cold_soup = pandas.DataFrame(data=[error_status], columns=error_header)
            cold_soup.to_csv("status_monitor.csv", mode="w", index=False)
    elif type(status_frame) is list:
        error_datatype = "Data type should be DataFrame, please set 'output_dataframe=True'."
        logging.warning(error_datatype)
    #Return DataFrame
    else:
        #Filter
        filtered_soup = status_frame.drop(spoon_enis, axis=1)
        #Set check value
        status_check = "Offline"
        #Check status
        if status_check in filtered_soup.values:
            #Print in terminal
            print(f"{timestamp_event} | Server offline")
            #Message
            broth = filtered_soup.loc[filtered_soup["Status"] == status_check].drop(spoon_zwei, axis=1).to_string(header=False, index=False)
            soup_menu = broth.replace("\n"," ; ")
            #Refresh status
            filtered_soup.to_csv("status_monitor.csv", mode="w", index=False)
            #Email configuration
            if bool(disalbe_phone_book) is False:
                status4hentai.soup_alert(soup_menu)
            else:
                status4hentai.soup_alert(soup_menu, sender_account, sender_password, receiver, disalbe_phone_book=True)
        else:
            print(f"{timestamp_event} | Server online")
            #Refresh status
            filtered_soup.to_csv("status_monitor.csv", mode="w", index=False)
    status4hentai.program_status()

#Scheduled Execute
schedule.every(scheduled_time).minutes.do(notification)
#Running
initialize = status4hentai.program_status(event="Start monitoring")
print(f"{initialize}\r\npressing CTRL+C to exit.")
#Loop
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
#Error save
except Exception as error_status:
    logging.exception(error_status)
    status4hentai.program_status(event="Error")
    print("Save error status to log file ...")
#Crtl+C to exit
except KeyboardInterrupt:
    termination = status4hentai.program_status(event="Offline")
    print(f"\r\n{termination}\r\nThank you for using the offline notification.\r\nGoodBye ...")
    sys.exit(0)
