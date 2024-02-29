# -*- coding: utf-8 -*-
import sys
import status4hentai

# Configuration file path
ConfigFilePath = "status4hah.config.json"
# Runtime file and path
StatusFilePath = "status4hah.status.csv"
# Status file filter
CheckingResultFilter = ["ID","Created","Client IP","Port","Version","Max Speed","Country"]
# Status file and path
CheckingResultPath = "status4hah.check.csv"
# Alert mode selection
AlertMode = 0
# Alert output filter
AlertFilter = ["Files Served","Trust","Quality","Hitrate","Hathrate"]

# Function
def StatusChecker(ConfigFilePath,StatusFilePath,CheckingResultFilter,CheckingResultPath,AlertMode,AlertFilter):
    # Read alert sending status
    ReadConfiguration = status4hentai.Configuration(ConfigFilePath)
    # Get Hentai@Home Status
    HentaiAtHomePayload = status4hentai.CheckHentaiatHome(ConfigFilePath)
    # Check Hentai@Home status
    StatusTable = status4hentai.GetHentaiStatus(HentaiAtHomePayload)
    # Get string, means error occurred, or Cookie expires.
    if type(StatusTable) is str:
        # Write status file
        status4hentai.ProgramCurrentStatus(StatusFilePath, EventUpdate=StatusTable)
        # Than Alert
        status4hentai.SendAlert(AlertMode, ConfigFilePath, MessagePayload=StatusTable)
    # Get pandas DataFrame
    else:
        # Drop unneeded columns for status table, and save to status resutl file
        status4hentai.SaveStatusTable(CheckFilePath=CheckingResultPath, CheckTableInput=StatusTable, CheckFilter=CheckingResultFilter)        
        # Check server status
        CheckOffline = StatusTable["Status"].isin(["Offline"]).tolist()
        # If server offling, return True
        if True in CheckOffline:
            # Drop unneeded columns again, translate pandas table into string
            StatsusString = status4hentai.Table2String(TableInput=StatusTable, DropFilter=AlertFilter)
            # Check alert sending count
            if ReadConfiguration["alert_counting"] == True:
                # Server still offline, alert already sent
                status4hentai.ProgramCurrentStatus(StatusFilePath, EventUpdate=("Server offline, alert already senting."))
            elif ReadConfiguration["alert_counting"] == False:
                # Sending alert
                AlertResult = status4hentai.SendAlert(AlertMode,ConfigFilePath, MessagePayload=(f"Hentai@Home server is currently offline.\r\n\r\n{StatsusString}"))
                # Check sending success or not
                if type(AlertResult) is int:
                    # Sending successfully
                    status4hentai.ProgramCurrentStatus(StatusFilePath, EventUpdate=("Server offline, alert sending successfully."))
                    # Update alert sending status, flip alert counting 
                    ReadConfiguration["alert_counting"] = True
                    # Update configuration
                    status4hentai.Configuration(ConfigFilePath, ConfigUpdate=ReadConfiguration)
                elif type(AlertResult) is str:
                    # Configuration not found. Chat channel wasn't create or HTTP Error.
                    status4hentai.ProgramCurrentStatus(StatusFilePath, EventUpdate=AlertResult)
                elif type(AlertResult) is bool:
                    # Error
                    status4hentai.ProgramCurrentStatus(StatusFilePath, EventUpdate=("Error occurred when sending alert."))
        # All server is online
        else:
            status4hentai.ProgramCurrentStatus(StatusFilePath)
            # Update alert sending status
            if ReadConfiguration["alert_counting"] == True:
                # Reset alert sending status, flip sending status
                ReadConfiguration["alert_counting"] = False
                # Update configuration
                status4hentai.Configuration(ConfigFilePath, ConfigUpdate=ReadConfiguration)
            else:
                pass

# Running program
try:
    StatusChecker(ConfigFilePath,StatusFilePath,CheckingResultFilter,CheckingResultPath,AlertMode,AlertFilter)
    sys.exit(0)
# Error handling
except Exception:
    status4hentai.ProgramCurrentStatus(StatusFilePath, EventUpdate=("Program has stopped working due to error."))
    sys.exit(0)

# 2024_02_29