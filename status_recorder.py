#coding=utf-8
import csv
import time
import pandas
import logging
import schedule
import status4hentai

#Error handling
FORMAT = "%(asctime)s |%(levelname)s |%(message)s"
logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a", format=FORMAT)

#Create_recoding_file
try:
    with open("status_record.csv", mode="r") as record_book:
        tape = csv.reader(record_book)
        record_book.close()
#If data not found
except FileNotFoundError:
    print("Recoding file create")
    with open("status_record.csv", mode="w") as record_book:
        tape = csv.writer(record_book)
        tape.writerow(["Client","ID","Status","Last Seen","Files Served","Trust","Quality","Hitrate","Hathrate"])
        record_book.close()

#Function
def status_recorder():
    event_time = status4hentai.current_time()
    status_frame = status4hentai.hentai_status(output_dataframe=True, disalbe_retry=False)
    #Check
    if type(status_frame) is bool:
        #If return False, means Error
        if status_frame is False:
            #Message
            print(f"{event_time} | Error occurred when parsing HTML page.")
            #Status
            with open("status_record.csv", mode="a") as record_book:
                taping = csv.writer(record_book)
                taping.writerow(["","","Error",event_time,"","","","",""])
                record_book.close()
        #If return True, means Unable to login E-Hentai, and retry is disable
        elif status_frame is True:
            print(f"{event_time} | Unable to login E-Hentai, Login retry is disable")
            #Status
            with open("status_record.csv", mode="a") as record_book:
                taping = csv.writer(record_book)
                taping.writerow(["","","Unable Login",event_time,"","","","",""])
                record_book.close()
    elif type(status_frame) is list:
        error_datatype = "Data type should be DataFrame, please set 'output_dataframe=True'."
        logging.warning(error_datatype)
    #Recording
    else:
        filter_spoon = ["Created","Client IP","Port","Version","Max Speed","Country"]
        filtered_soup = status_frame.drop(filter_spoon, axis=1)
        filtered_soup.to_csv("status_record.csv", mode="a", index=False, header=False)
        print(f"{event_time} | Recording ...")

#Execute setting
schedule.every(45).minutes.do(status_recorder)
#Running
initialize = status4hentai.current_time()
print(f"{initialize} | Now recording, pressing CTRL+C to exit.")
#Loop
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
#Error save
except Exception as error_status:
    logging.exception(error_status)
    print("Save error status to log file ...")
#Crtl+C to exit
except KeyboardInterrupt:
    exit_time = status4hentai.current_time()
    print(f"\r\n{exit_time} | Thank you for using the status recoder.\r\nGoodBye ...")
