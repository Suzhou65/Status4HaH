# -*- coding: utf-8 -*-
import logging
from pathlib import Path
import json
import datetime
import textwrap
import csv
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
import smtplib

# For error handling, logfile config
FORMAT = "%(asctime)s |%(levelname)s |%(message)s"
logging.basicConfig(
    level=logging.WARNING,
    filename="error.status4hah.log", filemode="a", format=FORMAT)

# Web and mail config
class Link():
    def __init__(self):
        self.HentaiAtHome = "https://e-hentai.org/hentaiathome.php"
        self.Telegram     = "https://api.telegram.org/bot"
        self.SMTPServer   = "smtp.gmail.com"
        self.SMTPPort     =  587

# Configuration function, reading json file
class Configuration():
    def __init__(self, ConfigFilePath):
        try:
            ConfigInput = Path(ConfigFilePath)
            with ConfigInput.open("r", encoding = "utf-8") as ConfigFile:
                ConfigData = json.load(ConfigFile)
                self.Load = ConfigData
        # Error
        except Exception as ConfigurationError:
            raise Exception(ConfigurationError)
        # QC 2025K25

# Runtime package
class Runtime():
    def __init__(self, ConfigFilePath):
        self.RuntimeConfig  = Configuration(ConfigFilePath).Load
        #
        self.StatusHeader   = self.RuntimeConfig['EHentai']['TableHeader']
        # Runtime status csv
        self.Status4Rumtime = self.RuntimeConfig['RuntimeStatus']['StatusPath']
        # H@H client status csv
        self.ClientsStatus  = self.RuntimeConfig['DisplayDrop']['OutputPath']
        self.DropKey        = self.RuntimeConfig['DisplayDrop']['Filter']
        # Recording function
        self.ActiveRecord   = self.RuntimeConfig['Recording']['StatusRecord']
        self.TapePath       = self.RuntimeConfig['Recording']['RecordingPath']
        # Terminal text width
        self.MessageWidth = 100

    # Print runtime info
    def Message(self, MessageText =('foo')):
        PrintTime = datetime.datetime.now()
        TimeHMS = PrintTime.strftime("%H:%M:%S")
        TextPrefix = (f"{TimeHMS} | ")
        UsableWidth = self.MessageWidth - len(TextPrefix)
        SequentIndent = " " * len(TextPrefix)
        Wrapping = textwrap.fill(
            MessageText, width=UsableWidth, subsequent_indent=SequentIndent)
        print(TextPrefix + Wrapping)
        # QC 2025K25

    # Runtime status
    def StatusRuntime(self, Event = ('bar')):
        try:
            PrintTime = datetime.datetime.now()
            TimeYMDHM = PrintTime.strftime("%Y-%m-%d %H:%M")
            StatusBook = (f"{TimeYMDHM}, {Event}")
            RuntimeCSV = Path(self.Status4Rumtime)
            with RuntimeCSV.open("w") as RuntimeTable:
                RuntimeTable.write(StatusBook)
            self.Message(Event)
        except Exception as StatusTableError:
            logging.warning(StatusTableError)
        # QC 2025K25

    # Drop sensitive keys
    def StatusKeyDrop(self, StatusData):
        try:
            # Get drop keys
            RemoveKeys = self.DropKey
            # Disable sensitive keys dropping, return with sensitive keys
            if isinstance(RemoveKeys, bool) and RemoveKeys is False:
                return StatusData
            # Enable sensitive keys dropping
            elif isinstance(RemoveKeys, list):
                pass
            # Error
            else:
                # Error prompt
                self.Message("StatusKeyDrop should be select between false or filter list.")
                # Error warning
                logging.warning("Invalid filter config. Applying minimal sensitive key filtering.")
                # Minimum sensitive keys dropping
                RemoveKeys = ["Client IP","Port"]
            # Dropping
            for StatusRow in StatusData:
                for RemoveKey in RemoveKeys:
                    StatusRow.pop(RemoveKey, None)
            return StatusData
        except Exception as StatuDropError:
            logging.warning(StatuDropError)
        # QC 2025L05

    # Webpage status output
    def StatusWebpage(self, DisplayData):
        try:
            if not DisplayData:
                logging.warning("Input status data is empty.")
                return
            elif isinstance(self.ClientsStatus, bool) and self.ClientsStatus is False:
                self.Message("Webpage status output disable.")
                return
            elif isinstance(self.ClientsStatus, bool) and self.ClientsStatus is True:
                logging.warning("Config: OutputPath should be False or path string.")
                return
            elif isinstance(self.ClientsStatus, str) and self.ClientsStatus != "":
                # File path
                StatusWeb = Path(self.ClientsStatus)
                with open(StatusWeb, "w", newline="", encoding="utf-8") as StatusCSV:
                    StatusWriter = csv.DictWriter(StatusCSV,fieldnames=self.StatusHeader, extrasaction="ignore")
                    # Write header
                    StatusWriter.writeheader()
                    # Write clients row
                    for Row in DisplayData:
                        StatusWriter.writerow(Row)
            else:
                logging.warning("Config: OutputPath should be string or boolean.")
        except Exception as StatusWebError:
            logging.warning(StatusWebError)
        # QC 2025L04

    # Saving H@H clients data into separate CSV
    def StatusRecorder(self, DataInput):
        if not isinstance(self.ActiveRecord, bool):
            logging.warning("StatusRecord should be bool.")
            return
        # Disable recording
        elif isinstance(self.ActiveRecord, bool) and self.ActiveRecord is False:
            self.Message("StatusRecord disable.")
            return
        # Enable recording
        elif isinstance(self.ActiveRecord, bool) and self.ActiveRecord is True:
            RecordingPath = Path(self.TapePath)
            DataInput: list[dict]
            try:
                RecordingPath.mkdir(parents=True, exist_ok=True)
                for DataRow in DataInput:
                    ClientName = DataRow.get("Client", None)
                    if ClientName is None:
                        continue
                    TapePath = RecordingPath / f"{ClientName}.csv"
                    FileExists = TapePath.exists()
                    with TapePath.open("a", newline="", encoding="utf-8") as TapeWriter:
                        RowWriter = csv.DictWriter(TapeWriter, fieldnames=self.StatusHeader, extrasaction="ignore")
                        if not FileExists:
                            RowWriter.writeheader()
                        RowWriter.writerow(DataRow)
            except Exception as RecordError:
                logging.warning(RecordError) 
        # QC 2025L05

# Hentai@Home check
class EHentai():
    def __init__(self, ConfigFilePath):
        self.EHentaiConfig  = Configuration(ConfigFilePath).Load
        self.Member         = self.EHentaiConfig['EHentai']['ipb_member_id']
        self.Password       = self.EHentaiConfig['EHentai']['ipb_pass_hash']
        self.UserAgent      = self.EHentaiConfig['EHentai']['UserAgent']
        self.Com = Link()
        self.RtM = Runtime(ConfigFilePath)

    # Check H@H clients status
    def CheckHentaiatHome(self):
        try:
            # Checking
            with requests.get(
                self.Com.HentaiAtHome,
                headers = {"user-agent": self.UserAgent},
                cookies = {"ipb_member_id": self.Member, "ipb_pass_hash": self.Password},
                timeout = 30) as CheckRespon:
                # HTTP Error
                if CheckRespon.status_code != 200:
                    logging.warning(CheckRespon.status_code)
                    return CheckRespon.status_code
                # HTTP 200 OK
                else:
                    # BS4 kick-in
                    ResponHTML = BeautifulSoup(CheckRespon.content, "html.parser")
            # Try to find table named hct, which contain HentaiAtHome status
            TableHCT = ResponHTML.find("table", id="hct")
            # Try to find login table
            TableLogIn = ResponHTML.find("table", id="d")
            # Check logout
            if TableLogIn and not TableHCT:
                NeedLogin = ("Status4Hah require login.")
                self.RtM.StatusRuntime(NeedLogin)
                return NeedLogin
            # Get status table
            elif TableHCT and not TableLogIn:
                # Rows in table
                HCTRows = TableHCT.find_all("tr")
                # Header as key
                HCTHeaders = [th.get_text(strip=True) for th in HCTRows[0].find_all('th')]
                # List for all clients
                ParsedRows = []
                # Value after first row
                for HCTRow in HCTRows[1:]:
                    ElementTDs = HCTRow.find_all("td")
                    # Empty value section
                    if not ElementTDs:
                        continue
                    # Dictionary for client
                    RowDict = {}
                    # Package with key and value
                    for key, cell in zip(HCTHeaders, ElementTDs):
                        # Value text
                        text = cell.get_text(strip=True).replace("KB/s","KBps").replace(" / "," per ")
                        # Adding blank in empty value
                        RowDict[key] = text if text != "" else None
                    ParsedRows.append(RowDict)
                # Return Status dictionary
                return ParsedRows
            # Exception
            else:
                return False
        except Exception as CheckHentaiatHomeError:
            logging.warning(CheckHentaiatHomeError)
            return False
        # QC 2025K30

    # Check offline client
    def OfflineChecker(self, StatusDictionary):
        try:
            # Offline client list
            OfflineClientList = []
            # Check all client
            for ClientList in StatusDictionary:
                if ClientList['Status'] == ("Offline"):
                    OfflineClientList.append(ClientList['Client'])
                else:
                    pass
            return OfflineClientList
        except Exception as OfflineCheckerError:
            logging.warning(OfflineCheckerError)
            return False
        # QC 2025L02

# Offline alert
class Alert():
    def __init__(self, ConfigFilePath):
        self.Com           = Link()
        self.RtM           = Runtime(ConfigFilePath)
        self.AlertConfig   = Configuration(ConfigFilePath).Load
        # Mode
        self.ModeSelert    = self.AlertConfig['Alert']['Mode']
        # Once-only or continuous mode
        self.Continuous    = self.AlertConfig['Alert']['ContinuousAlert']
        # Telegram
        self.BotToken      = self.AlertConfig['Telegram_BOTs']['Token']
        self.ChatID        = self.AlertConfig['Telegram_BOTs']['ChatID']
        # SMTP
        self.MailSender    = self.AlertConfig['Mail']['Sender']
        self.SenderScepter = self.AlertConfig['Mail']['Scepter']
        self.Receiver      = self.AlertConfig['Mail']['Receiver']
        # Timestemp
        SendingTime        = datetime.datetime.now()
        self.SendingYMDHMS = SendingTime.strftime("%Y-%m-%d %H:%M:%S")
        self.SendingHMS    = SendingTime.strftime("%H:%M:%S")

    # Alarm function
    def Alarm(self, AlarmMessage = (None)):
        try:
            # Disable alert
            if isinstance(self.ModeSelert, bool) and self.ModeSelert is False:
                self.RtM.Message("Telegram or mail alert is currently disabled.")
                return
            # Empty path string
            elif isinstance(self.ModeSelert, str) and self.ModeSelert == "":
                logging.warning("To enable alert, mode should be select between telegram or mail.")
                return
            # Mode select
            elif isinstance(self.ModeSelert, str) and self.ModeSelert != "":
                AlarmMode = self.ModeSelert.lower()
            # Error
            else:
                logging.warning("Mode should be select between telegram or mail, or disable.")
                return
            # Continuous mode
            if isinstance(self.Continuous, bool) and self.Continuous is True:
                self.RtM.Message("Telegram or Mail alert is currently under continuous mode.")
                # Telegram alert
                if AlarmMode == "telegram":
                    self.Telegram(AlarmMessage)
                # Mail alert
                elif AlarmMode == "mail":
                    self.Mail(AlarmMessage)
                return
            # Error
            elif isinstance(self.Continuous, bool) and self.Continuous is False:
                logging.warning("Continuous mode should be select between true or path string.")
                return
            # Enable once-only alert
            elif isinstance(self.Continuous, str) and self.Continuous != "":
                Blocker = Path(self.Continuous)
                # Stop alert
                if Blocker.exists():
                    self.RtM.Message("Telegram or Mail alert is currently under once-only mode.")
                    return
                # Blocker not found, alert then create blocker
                else:
                    if AlarmMode == "telegram":
                        self.Telegram(AlarmMessage)
                    elif AlarmMode == "mail":
                        self.Mail(AlarmMessage)
                    # Create once-only blocker
                    try:
                        with open(Blocker, "w") as Obstacle:
                            Obstacle.write(self.SendingYMDHMS)
                        return
                    except Exception as ObstacleError:
                        logging.warning(ObstacleError)
                        return
        # Undefined error
        except Exception as AlarmError:
            logging.warning(AlarmError)
        # QC 2025L04

    # Delete alert blocker for disable continuous alert
    def RemoveObstacle(self):
        try:
            # Reset once-only alert blocker
            if isinstance(self.Continuous, str):
                Obstacle = Path(self.Continuous)
                if Obstacle.exists():
                    try:
                        Obstacle.unlink()
                    # Blocker already delete
                    except FileNotFoundError:
                        pass
            # Continuous mode
            elif isinstance(self.Continuous, bool):
                pass
        # Undefined error
        except Exception as ObstacleRemoveError:
            logging.warning(ObstacleRemoveError)
        # QC 2025L04

    # Set default message for testing
    def Telegram(self, TelegramMessage = ('Here, the world!')):
        # Connetc URL
        TgURL = (self.Com.Telegram + f"{self.BotToken}/sendMessage")
        # Text content
        TgMsg = {"chat_id": f"{self.ChatID}", "text": TelegramMessage}
        try:
            TgResponse = requests.post(TgURL, json=TgMsg, timeout=30)
            if TgResponse.status_code == 200:
                self.RtM.Message(TelegramMessage)
            elif TgResponse.status_code == 400:
                self.RtM.Message("Telegram ChatID is empty, notifications will not be sent.")
                logging.warning(TgResponse.status_code)
            else:
                logging.warning(TgResponse.status_code)
            TgResponse.close()
        # Undefined error
        except Exception as TelegramErrorStatus:
            logging.warning(TelegramErrorStatus)
        # QC 2025L03

    # Get Telegram ChatID
    def GetTelegramChatID(self):
        # Connetc URL
        TgAskURL = (self.Com.Telegram + f"{self.BotToken}/getUpdates")
        try:
            TgAskResponse = requests.post(TgAskURL, timeout=30)
            if TgAskResponse.status_code == 200:
                TgAskData = json.loads(TgAskResponse.text)
            else:
                logging.warning(TgAskResponse.status_code)
                return
            # Empty result
            if len(TgAskData['result']) == 0:
                self.RtM.Message("You must send message to bot first.")
            # Select ChatID
            else:
                CheckChatID = TgAskData["result"][0]['message']['chat']['id']
                self.RtM.Message(f"Your ChatID is: {CheckChatID}")
            TgAskResponse.close()
        # Undefined error
        except Exception as TelegramGetIDError:
            logging.warning(TelegramGetIDError)
        # QC 2025L03

    # Sending mail alert, default using gmail smtp
    def Mail(self, MailMessage= ('Sweet Escape')):
        try:
            # Mail text
            MailMessage = MIMEText(MailMessage)
            # Mail title
            MailMessage["Subject"] = (f"H@H offline alert | {self.SendingHMS}")
            MailMessage["From"] = self.MailSender
            MailMessage["To"] = self.Receiver
            # Connect to gmail server
            LinkSMTPServer = smtplib.SMTP(self.Com.SMTPServer, self.Com.SMTPPort)
            LinkSMTPServer.ehlo()
            LinkSMTPServer.starttls()
            LinkSMTPServer.login(self.MailSender, self.SenderScepter)
            # Sending
            LinkSMTPServer.sendmail(self.MailSender, self.Receiver, MailMessage.as_string())
            # Close connection
            LinkSMTPServer.quit()
        # Undefined error
        except Exception as MailErrorStatus:
            logging.warning(MailErrorStatus)
        # QC 2025L03
