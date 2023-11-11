# -*- coding: utf-8 -*-
import sys
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
        # Error message
        EventUpdate = "Exception error occurred, check log."
        status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
    # Get string, means controllable error or logout
    elif type(DataTableOutput) is str:
        # Get HTTP status code or timeout error message
        EventUpdate = DataTableOutput
        status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
    # Get pandas DataFrame
    else:
        # Drop columns config
        DataTableFilter = ["Created","Client IP","Port","Version","Max Speed","Country"]
        # Drop unneeded columns
        DataTableOutput.drop(columns=DataTableFilter,inplace=True)
        # Saving
        DataTableOutput.to_csv(RecordingPath,mode="a",index=False,header=False)
        EventUpdate = "Status recording successfully."
        # Write status file
        status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
# Running program
try:
    StatusRecorder(ConfigFilePath,RecordingPath,StatusFilePath)
    sys.exit(0)
# Error handling
except Exception:
    EventUpdate = "Program has stopped working due to error."
    status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
    sys.exit(0)

# 2023_11_12