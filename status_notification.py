# -*- coding: utf-8 -*-
import sys
import time
import schedule
import status4hentai

# Configuration file path
ConfigFilePath = "status4hah.config.json"
# Status file path
CheckingResultPath = "status4hah.check.csv"
# Create status file
StatusFilePath = "status4hah.status.csv"
# Alert mode selection
AlertMode = 0

# Function
def notification(ConfigFilePath,CheckingResultPath,StatusFilePath,AlertMode):
    # Get Hentai@Home Page
    ResponPayload = status4hentai.CheckHentaiatHome(ConfigFilePath)
    # Check Hentai@Home status
    DataTableOutput = status4hentai.GetHentaiStatus(ResponPayload)
    # Check output
    # Get boolean, means error
    if type(DataTableOutput) is bool:
        TimeStamp = status4hentai.GetTime()
        # Error message
        EventUpdate = "Error occurred when running program, check log."
        # Write status file
        status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
        # Print message
        print(f"{TimeStamp} | {EventUpdate}")
    # Get string, means controllable error or logout
    elif type(DataTableOutput) is str:
        TimeStamp = status4hentai.GetTime()
        # Get HTTP status code or timeout error message
        EventUpdate = DataTableOutput
        # Write status file
        status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
        # Print message
        print(f"{TimeStamp} | {EventUpdate}")
    # Get pandas DataFrame
    else:
        # Drop columns config
        DataTableFilter = ["ID","Created","Client IP","Port","Version","Max Speed","Country"]
        # Drop unneeded columns
        DataTableOutput.drop(columns=DataTableFilter,inplace=True)
        # Saving to checking result
        DataTableOutput.to_csv(CheckingResultPath,mode="w",index=False,header=True)
        # Check server status
        CheckList = DataTableOutput["Status"].isin(["Offline"]).tolist()
        # If server offling, return True
        if True in CheckList:
            TimeStamp = status4hentai.GetTime()
            EventUpdate = "Server offline, sending alert."
            status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
            print(f"{TimeStamp} | {EventUpdate}")
            # Mail alert
            if AlertMode == 0:
                MailPayload = "Hentai@Home server is offline."
                AlertAction = status4hentai.SendAlertMail(MailPayload,ConfigFilePath)
            # Telegram alert
            else:
                TelegramPayload = f"{TimeStamp}\r\nHentai@Home server is offline."
                AlertAction = status4hentai.SendAlertTelegram(TelegramPayload,ConfigFilePath)
            # Check alert action result
            if type(AlertAction) is str:
                print("Alert sending successfully.")
            else:
                print("Unable to sending alert.")
        else:
            TimeStamp = status4hentai.GetTime()
            print(f"{TimeStamp} | All server online.")
            status4hentai.ProgramCurrentStatus(StatusFilePath)

# Execute setting
schedule.every(30).minutes.do(notification,ConfigFilePath,CheckingResultPath,StatusFilePath,AlertMode)
# Running
EventUpdate = "Program start"
status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
InitializeTime = status4hentai.GetTime()
print(f"{InitializeTime} | Now checking, pressing Control + C to exit.")
# Loop
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
# Error handling
except Exception:
    StopTime = status4hentai.GetTime()
    EventUpdate = "Program has stopped working due to error"
    status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
    print(f"{StopTime} | Error occurred when running program.")
# Crtl+C to exit
except KeyboardInterrupt:
    ExitTime = status4hentai.GetTime()
    EventUpdate = "Program has stopped working"
    status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
    print(f"\r\n{ExitTime} | Thank you for using the status recoder.\r\nGoodBye ...")
    sys.exit(0)

# 2023_07_23