# -*- coding: utf-8 -*-
import sys
import time
import schedule
import status4hentai

# Configuration file path
ConfigFilePath = "status4hah.config.json"
# Recording file path
RecordingPath = "status4hah.record.csv"
# Create status file
StatusFilePath = "status4hah.status.csv"

# Function
def StatusRecorder(ConfigFilePath,RecordingPath,StatusFilePath):
    # Get Hentai@Home Page
    ResponPayload = status4hentai.CheckHentaiatHome(ConfigFilePath)
    # Check Hentai@Home status
    DataTableOutput = status4hentai.GetHentaiStatus(ResponPayload)
    # Check output
    # Get boolean, means exception error
    if type(DataTableOutput) is bool:
        TimeStamp = status4hentai.GetTime()
        # Error message
        EventUpdate = "Exception error occurred, check log."
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
        DataTableFilter = ["Created","Client IP","Port","Version","Max Speed","Country"]
        # Drop unneeded columns
        DataTableOutput.drop(columns=DataTableFilter,inplace=True)
        # Saving
        DataTableOutput.to_csv(RecordingPath,mode="a",index=False,header=False)        
        TimeStamp = status4hentai.GetTime()
        EventUpdate = "Recording ..."
        # Write status file
        status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
        print(f"{TimeStamp} | {EventUpdate}")

# Execute setting
schedule.every(30).minutes.do(StatusRecorder,ConfigFilePath,RecordingPath,StatusFilePath)
# Running
EventUpdate = "Program start"
status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
InitializeTime = status4hentai.GetTime()
print(f"{InitializeTime} | Now recording, pressing Control + C to exit.")
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