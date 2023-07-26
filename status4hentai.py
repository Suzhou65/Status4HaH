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

# Error handling, message config
FORMAT = "%(asctime)s |%(levelname)s |%(message)s"
# Error file
logging.basicConfig(level=logging.WARNING, filename="status4hah.error.log",filemode="a",format=FORMAT)

# Time
def GetTime():
    CurrentTime = datetime.datetime.now()
    return CurrentTime.strftime("%Y-%m-%d %H:%M:%S")

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
    # Return as python table
    return StatusTable

# Configuration file
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
            ipb_session = getpass("Please enter the ipb_session_id: ")
            initialize_time = GetTime()
            # Dictionary
            ConfigInitialize = {
                # Recording configuration update time
                "last_update":initialize_time,
                # EHentai-Cookie
                "ipb_member_id":ipb_member_id,
                "ipb_pass_hash":ipb_pass_hash,
                "ipb_session_id":ipb_session,
                # Google Mail as sneder
                "mail_sender":"",
                "mail_scepter":"",
                # Mail address receive
                "mail_receiver": "",
                # Telegram BOT token
                "telegram_token":"",
                # Telegram ID receive
                "telegram_id":""
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
    # Request User-agent
    RequestHeaders = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82"}
    # Hentai@Home page
    HentaiAtHomePage = "https://e-hentai.org/hentaiathome.php"
    # Make SignIn Cookie
    CookiePayload = Configuration(ConfigFilePath)
    ipbm = CookiePayload["ipb_member_id"]
    ipbp = CookiePayload["ipb_pass_hash"]
    ibps = CookiePayload["ipb_session_id"]
    # Make cookies
    BrowserCookies = {"ipb_member_id":ipbm,"ipb_pass_hash":ipbp,"ipb_session_id":ibps}
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
        MessageCheck = "Python Requests TimeOut"
        logging.warning(ErrorTimeOut)
        # Return string
        return MessageCheck
    # Error handling
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        # Return bool
        return ErrorStatus

# Parsing HTML and get status table
def GetHentaiStatus(ResponPayload):
    # Check respon payload
    # Get bytes, maybe is HTML payload
    if type(ResponPayload) is bytes:
        # Parsing bytes to HTML
        ResponPayloadHTML = BeautifulSoup(ResponPayload,"html.parser")
        # Finding table named hct
        TableHCT = ResponPayloadHTML.find("table",{"class":"hct"})
        # Chech logout or other situations
        if not TableHCT:
            # Try to find login table
            TableLogIn = ResponPayloadHTML.find("div",{"class":"d"})
            # Something worse
            if not TableLogIn:
                MessageParsing = "Error occurred when parsing HTML."
                logging.error(MessageParsing)
                return MessageParsing
            # Somehow is logout
            else:
                MessageParsing = "Cookie expires."
                logging.error(MessageParsing)
                return MessageParsing
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
    # Get string, connecting Timeout
    elif type(ResponPayload) is str:
        logging.warning(ResponPayload)
        # Return string with Requests timeout messege
        return ResponPayload
    # Get integer, maybe server error
    elif type(ResponPayload) is int:
        MessageParsing = (f"HTTP Error {ResponPayload}")
        logging.warning(MessageParsing)
        # Return string with HTTP Status code
        return MessageParsing
    # Get exception error input, the worst case
    else:
        return False

# Sending mail
def SendAlertMail(MailPayload,ConfigFilePath):
    # Load configuration
    MailConfig = Configuration(ConfigFilePath)
    # Configuration not found
    if len(MailConfig["mail_sender"]) == 0:
        MessageSending = "Mail configuration not found, please initialize."
        logging.error(MessageSending)
        return 404
    # Find configuration
    else:
        MailAccount = MailConfig["mail_sender"]
        MailPassword = MailConfig["mail_scepter"]
        MailReceiver = MailConfig["mail_receiver"]
    # Sending mail via gmail
    MailMessage = MIMEText(MailPayload)
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
        return MailPayload
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# Sending telegram message via bots
def SendAlertTelegram(TelegramPayload,ConfigFilePath):
    # Load configuration
    TelegramConfig = Configuration(ConfigFilePath)
    # Configuration not found
    if len(TelegramConfig["telegram_token"]) == 0:
        MessageSending = "Telegram configuration not found, please initialize."
        logging.error(MessageSending)
        return 404
    # Find configuration
    else:
        TelegramBotToken = TelegramConfig["telegram_token"]
        TelegramReceiver = TelegramConfig["telegram_id"]
    # Make telegram url
    TelegramBotURL = f"https://api.telegram.org/bot{TelegramBotToken}/sendMessage"
    TelegramJsonPayload = {"chat_id":TelegramReceiver,"text":TelegramPayload}
    # Sending mail via telegram
    try:
        TelegramResponse = requests.post(TelegramBotURL,json=TelegramJsonPayload)
        if TelegramResponse.status_code == 200:
            TelegramResponse.close()
            # Return payload
            return TelegramPayload
        # If not
        else:
            TelegramResponse.close()
            # Return integer
            return TelegramResponse.status_code
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# 2023_07_23