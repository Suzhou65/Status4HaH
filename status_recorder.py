# -*- coding: utf-8 -*-
import sys
import status4hentai

# Configuration file path
ConfigFilePath = "status4hah.config.json"
# Runtime file and path
StatusFilePath = "status4hah.status.csv"
# Recording file filter
RecordingFilter = ["ID","Created","Client IP","Port","Version","Max Speed","Country"]
# Recording file path
RecordingPath = "status4hah.record.csv"

# Function
def StatusRecorder(ConfigFilePath,StatusFilePath,RecordingFilter,RecordingPath):
    # Get Hentai@Home Status
    HentaiAtHomePayload = status4hentai.CheckHentaiatHome(ConfigFilePath)
    # Check Hentai@Home status
    StatusTable = status4hentai.GetHentaiStatus(HentaiAtHomePayload)
    # Get string, means error occurred, or Cookie expires.
    if type(StatusTable) is str:
        # Write status file
        status4hentai.ProgramCurrentStatus(StatusFilePath, EventUpdate=StatusTable)
    # Get pandas DataFrame
    else:
        # Drop unneeded columns for status table, and save to status resutl file
        StatusTable.drop(columns=RecordingFilter,inplace=True)
        # Saving
        StatusTable.to_csv(RecordingPath,mode="a",index=False,header=False)
        # Write status file
        status4hentai.ProgramCurrentStatus(StatusFilePath, EventUpdate=("Status recording successfully."))

# Running program
try:
    StatusRecorder(ConfigFilePath,RecordingPath,StatusFilePath)
    sys.exit(0)
# Error handling
except Exception:
    status4hentai.ProgramCurrentStatus(StatusFilePath, EventUpdate=("Program has stopped recording due to error."))
    sys.exit(0)

# 2024_03_04