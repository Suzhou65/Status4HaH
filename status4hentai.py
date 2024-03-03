# -*- coding: utf-8 -*-
import json
import pandas
import logging
import smtplib
import requests
import datetime
from getpass import getpass
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

# For error handling, logfile config
FORMAT = "%(asctime)s |%(levelname)s |%(message)s"
# Error logfile name and level config
logging.basicConfig(level=logging.WARNING,filename="status4hah.error.log",filemode="a",format=FORMAT)

# Generate timestamp
def GetTime():
    CurrentTime = datetime.datetime.now()
    return CurrentTime.strftime("%Y-%m-%d %H:%M")

# Program running status
def ProgramCurrentStatus(StatusFilePath,EventUpdate=()):
    # Table header config
    StstusHeader = ["Time","Status"]
    # If check procress complete normally
    if not EventUpdate:
        StatusTable = [GetTime(),"Check Complete"]
    # If not, update status
    else:
        StatusTable = [GetTime(),EventUpdate]
    # Save as table
    status_output = pandas.DataFrame(data=[StatusTable],columns=StstusHeader)
    # Save to csv file
    status_output.to_csv(StatusFilePath,mode="w",index=False)

# Configuration file read and write
def Configuration(ConfigFilePath,ConfigUpdate=()):
    # Just read configuration
    if not ConfigUpdate:
        # Reading configuration file
        try:
            with open(ConfigFilePath,"r") as ConfigurationFile:
                # Return as python dictionary
                return json.load(ConfigurationFile)
        # If file not found
        except FileNotFoundError:
            # Initialization message
            print("Configuration not found, please initialize.\r\n")
            # Input basic configuration
            ipb_member_id = getpass("Please enter the ipb_member_id: ")
            ipb_pass_hash = getpass("Please enter the ipb_pass_hash: ")
            configuration_update = GetTime()
            # Dictionary
            ConfigInitialize = {
                # Recording configuration update time
                "last_update":configuration_update,
                # EHentai-Cookie
                "ipb_member_id":ipb_member_id,
                "ipb_pass_hash":ipb_pass_hash,
                # Broswer User-Agent
                "request_header":"",
                # Google Mail as sneder
                "mail_sender":"",
                "mail_scepter":"",
                # Mail address receive
                "mail_receiver": "",
                # Telegram BOT token
                "telegram_token":"",
                # Telegram ID receive
                "telegram_id":"",
                # Check flag
                "alert_counting":False
                }
            # Save configuration file
            with open(ConfigFilePath,"w") as ConfigurationFile:
                # Save
                json.dump(ConfigInitialize,ConfigurationFile,indent=2)
                print("Configuration saved successfully.")
                # Return dictionary
                return ConfigInitialize
    # Update configuration
    elif type(ConfigUpdate) is dict:
        # Log update time
        TimeConfigUpdate = GetTime()
        ConfigUpdate["last_update"] = TimeConfigUpdate
        # Save
        with open(ConfigFilePath,"w") as ConfigurationFile:
            json.dump(ConfigUpdate,ConfigurationFile,indent=2)
            # Return dictionary
            return ConfigUpdate

# Check Hentai@Home
def CheckHentaiatHome(ConfigFilePath):
    # Hentai@Home page
    HentaiAtHomePage = "https://e-hentai.org/hentaiathome.php"
    # Get cookie and header config
    GetPayload = Configuration(ConfigFilePath)
    # Make cookies
    ipbm = GetPayload["ipb_member_id"]
    ipbp = GetPayload["ipb_pass_hash"]
    BrowserCookies = {"ipb_member_id":ipbm,"ipb_pass_hash":ipbp}
    # Make user-agent
    Headers = GetPayload["request_header"]
    RequestHeaders = {"user-agent":Headers}
    # Get hentaiathome page
    try:
        HentaiAtHomeRespon = requests.get(HentaiAtHomePage,headers=RequestHeaders,cookies=BrowserCookies,timeout=10)
        # If request succcess
        if HentaiAtHomeRespon.status_code == 200:
            HentaiAtHomeRespon.close()
            # Return payload
            return HentaiAtHomeRespon.content
        # If not
        else:
            HentaiAtHomeRespon.close()
            # Return integer
            return HentaiAtHomeRespon.status_code
    # If timeout
    except requests.exceptions.Timeout as ErrorTimeOut:
        logging.warning(ErrorTimeOut)
        # Return integer
        return 408
    # Error handling
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        # Return bool
        return False

# Parsing HTML and get status table
def GetHentaiStatus(HentaiAtHomePayload):
    # Check respon payload
    if type(HentaiAtHomePayload) is int:
        # Get integer, maybe server error or request timeout. Return string with HTTP Status code
        return (f"HTTP Status Code: {HentaiAtHomePayload}")
    elif type(HentaiAtHomePayload) is bool:
        # Get exception input, the worst case
        return ("Exception happened during processing of request Hentai@Home Status.")
    else:
        # Get bytes, maybe is HTML payload, Parsing bytes to HTML
        HentaiAtHomePayload2HTML = BeautifulSoup(HentaiAtHomePayload,"html.parser")
        # Finding table named hct, which contain HentaiAtHome status
        TableHCT = HentaiAtHomePayload2HTML.find("table",id="hct")
        # Chech logout or other situations
        if not TableHCT:
            # Try to find login table
            TableLogIn = HentaiAtHomePayload2HTML.find("table",id="d")
            # Something worse
            if not TableLogIn:
                return ("Error occurred when parsing HTML payload.")
            # Somehow is logout
            else:
                return ("Cookie expires. Please update configuration file")
        # Get table correctly, start parsing
        else:
            # Makeing empty list
            ContentList = []
            ContentHeader = []
            # Parsing table
            StatusTable = TableHCT.find_all('tr')
            for tr in StatusTable:
                # Find header row
                th = tr.find_all("th")
                RowHeader = [tr.text for tr in th]
                # Find data row
                td = tr.find_all("td")
                RowContent = [tr.text for tr in td]
                # Filling in
                ContentList.append(RowContent)
                ContentHeader.append(RowHeader)
            # Remove empty element
            ContentHeader = ContentHeader[0]
            ContentList.pop(0)
            # Return Pandas dataframe
            return pandas.DataFrame(ContentList,columns=ContentHeader)

# Save Pandas dataframe to CSV
def SaveStatusTable(CheckFilePath,CheckTableInput,CheckFilter=()):
    try:
        if not CheckFilter:
            CheckTableInput.to_csv(CheckFilePath,mode="w",index=False,header=True)
            return CheckTableInput
        else:
            CheckTableInput.drop(columns=CheckFilter,inplace=True)
            CheckTableInput.to_csv(CheckFilePath,mode="w",index=False,header=True)
            return CheckTableInput
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# Trans Pandas dataframe with offline server into dictionary and string
def Table2String(TableInput,DropFilter):
    try:
        # Drop unneeded columns again
        TableInput.drop(columns=DropFilter,inplace=True)
        # Choice offline server only
        TableInput = TableInput.loc[TableInput["Status"] == "Offline"]
        # Translate into dictionary
        Table2Dict = TableInput.to_dict(orient="records")
        # Translate dictionary into string
        Dict2String = str(Table2Dict).replace("[","").replace("]","").replace("}, {","},\r\n{")
        return Dict2String
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# Sending alert
def SendAlert(AlertMode,ConfigFilePath,MessagePayload):
    # Load configuration
    MessageConfig = Configuration(ConfigFilePath)
    # Sending telegram message via bots
    if AlertMode == 0:
        # Ckeck configuration
        if len(MessageConfig["telegram_token"]) == 0:
            return ("Telegram configuration not found, please initialize.")
        # Find configuration
        else:
            TelegramBotToken = MessageConfig["telegram_token"]
            TelegramReceiver = MessageConfig["telegram_id"]
            # Make telegram url
            TelegramBotURL = f"https://api.telegram.org/bot{TelegramBotToken}/sendMessage"
            TelegramJsonPayload = {"chat_id":TelegramReceiver,"text":MessagePayload}
            # Sending telegram 
            try:
                TelegramResponse = requests.post(TelegramBotURL,json=TelegramJsonPayload)
                if TelegramResponse.status_code == 200:
                    TelegramResponse.close()
                    # Return payload
                    return 200
                # Chat channel wasn't create
                elif TelegramResponse.status_code == 400:
                    TelegramResponse.close()
                    # Return 400 Bad request
                    return ("Chat channel wasn't create.")
                # Other error
                else:
                    TelegramResponse.close()
                    return (f"Telegram API respons: {TelegramResponse.status_code}")
            except Exception as ErrorStatus:
                logging.exception(ErrorStatus)
                return False
    # Sending mail via Gmail
    else:
        # Ckeck configuration
        if len(MessageConfig["mail_sender"]) == 0:
            return ("Mail configuration not found, please initialize.")
        # Find configuration
        else:
            MailAccount = MessageConfig["mail_sender"]
            MailPassword = MessageConfig["mail_scepter"]
            MailReceiver = MessageConfig["mail_receiver"]
            # Sending mail via gmail
            MailMessage = MIMEText(MessagePayload)
            MailTimeStamp = GetTime()
            MailMessage["Subject"] = (f"Alert | {MailTimeStamp}")
            MailMessage["From"] = MailAccount
            MailMessage["To"] = MailReceiver
            try:
                # Connect to gmail server
                SmtpServer = smtplib.SMTP("smtp.gmail.com",587)
                SmtpServer.ehlo()
                SmtpServer.starttls()
                SmtpServer.ehlo
                SmtpServer.login(MailAccount,MailPassword)
                # Sending
                SmtpServer.sendmail(MailAccount,[MailReceiver],MailMessage.as_string())
                # Close connection
                SmtpServer.quit()
                # Retun mail text
                return 200
            except Exception as ErrorStatus:
                logging.exception(ErrorStatus)
                return False

# 2024_03_04