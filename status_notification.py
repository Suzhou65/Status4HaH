# -*- coding: utf-8 -*-
import sys
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
def StatusChecker(ConfigFilePath,CheckingResultPath,StatusFilePath,AlertMode):
    # Read alert sending status
    ReadConfiguration = status4hentai.Configuration(ConfigFilePath)
    # Get status value
    AlertFlag = ReadConfiguration["alert_counting"]
    # Get Hentai@Home Page
    ResponPayload = status4hentai.CheckHentaiatHome(ConfigFilePath)
    # Check Hentai@Home status
    DataTableOutput = status4hentai.GetHentaiStatus(ResponPayload)
    # Check output. Get boolean, means exception error
    if type(DataTableOutput) is bool:
        # Error message
        EventUpdate = "Exception error occurred, check log."
        # Write status file
        status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
    # Get string, means controllable error or logout
    elif type(DataTableOutput) is str:
        # Get HTTP status code or timeout error message
        EventUpdate = DataTableOutput
        # Write status file
        status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
    # Get pandas DataFrame
    else:
        # Drop columns config
        DataTableFilter = ["ID","Created","Client IP","Port","Version","Max Speed","Country"]
        # Drop columns config in alert
        DataTableFilterAlert = ["Files Served","Trust","Quality","Hitrate","Hathrate"]
        # Drop unneeded columns
        DataTableOutput.drop(columns=DataTableFilter,inplace=True)
        # Saving to checking result
        DataTableOutput.to_csv(CheckingResultPath,mode="w",index=False,header=True)
        # Check server status
        CheckList = DataTableOutput["Status"].isin(["Offline"]).tolist()
        # If server offling, return True
        if True in CheckList:
            # Drop unneeded columns again
            DataTableOutput.drop(columns=DataTableFilterAlert,inplace=True)
            # Choice offline server only
            DataTableOutput = DataTableOutput.loc[DataTableOutput["Status"] == "Offline"]
            # Translate into dictionary
            StatsusDict = DataTableOutput.to_dict(orient="records")
            # Translate dictionary into string
            StatsusString = str(StatsusDict).replace("[","").replace("]","").replace("}, {","},\r\n{")
            # Check alert sending count
            if AlertFlag == True:
                # Server still offline, alert already sent
                EventUpdate = "Server offline, alert already senting."
                status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
            elif AlertFlag == False:
                # Alert payload
                MessagePayload = f"Hentai@Home server is currently offline.\r\n\r\n{StatsusString}"
                # Sending alert
                AlertAction = status4hentai.SendAlert(AlertMode,ConfigFilePath,MessagePayload)
                # Check sending success or not
                if type(AlertAction) is str:
                    # Sending successfully
                    EventUpdate = "Server offline, alert sending successfully."
                    status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
                    # Update alert sending status
                    ConfigUpdate = ReadConfiguration
                    # Flip sending status
                    ConfigUpdate["alert_counting"] = True
                    # Update configuration
                    ReadConfiguration = status4hentai.Configuration(ConfigFilePath,ConfigUpdate)
                elif AlertAction == 404:
                    # configuration not found
                    EventUpdate = "Unable sending alert due to configuration not found."
                    status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
                elif AlertAction == 400:
                    # Chat channel wasn't create
                    EventUpdate = "Unable sending alert, chat channel wasn't create."
                    status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
                else:
                    # Error handling
                    EventUpdate = "Error occurred when sending alert."
                    status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
        # All server is online
        else:
            status4hentai.ProgramCurrentStatus(StatusFilePath)
            # Update alert sending status
            if AlertFlag == True:
                # Reset alert sending status
                ConfigUpdate = ReadConfiguration
                # Flip sending status
                ConfigUpdate["alert_counting"] = False
                # Update configuration
                ReadConfiguration = status4hentai.Configuration(ConfigFilePath,ConfigUpdate)
            else:
                pass

# Running program
try:
    StatusChecker(ConfigFilePath,CheckingResultPath,StatusFilePath,AlertMode)
    sys.exit(0)
# Error handling
except Exception:
    StopTime = status4hentai.GetTime()
    EventUpdate = "Program has stopped working due to error."
    status4hentai.ProgramCurrentStatus(StatusFilePath,EventUpdate)
    sys.exit(0)

# 2023_11_16