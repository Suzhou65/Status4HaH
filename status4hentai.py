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
# TESTPASS 25J25

# Link reference
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
    # TESTPASS 25K25

# Runtime package
class Runtime():
    def __init__(self, ConfigFilePath):
        self.RuntimeConfig  = Configuration(ConfigFilePath).Load
        # Runtime status csv
        self.Status4Rumtime = self.RuntimeConfig['RuntimeStatus']['StatusPath']
        # H@H client status csv
        self.ClientsStatus  = self.RuntimeConfig['DisplayDrop']['OutputPath']
        self.DropKey        = self.RuntimeConfig['DisplayDrop']['Filter']
        # Recording functio
        self.ActiveRecord   = self.RuntimeConfig['Recording']['StatusRecord']
        self.TapePath       = self.RuntimeConfig['Recording']['RecordingPath']
        # Terminal text width
        self.MessageWidth = 100
    # Print runtime info
    def Message(self, MessageText =('foo')):
        PrintTime = datetime.datetime.now()
        TimeHMS    = PrintTime.strftime("%H:%M:%S")
        TextPrefix = (f"{TimeHMS} | ")
        UsableWidth = self.MessageWidth - len(TextPrefix)
        SequentIndent = " " * len(TextPrefix)
        Wrapping = textwrap.fill(
            MessageText, width=UsableWidth, subsequent_indent=SequentIndent)
        print(TextPrefix + Wrapping)
    # TESTPASS 25K25
    # Runtime status
    def StatusRuntime(self, Event = ('bar')):
        try:
            PrintTime = datetime.datetime.now()
            TimeYMDHMS = PrintTime.strftime("%Y-%m-%d %H:%M:%S")
            StatusBook = (f"{TimeYMDHMS}, {Event}")
            RuntimeCSV = Path(self.Status4Rumtime)
            with RuntimeCSV.open("w") as RuntimeTable:
                RuntimeTable.write(StatusBook)
            self.Message(Event)
        except Exception as StatusTableError:
            logging.warning(StatusTableError)
    # TESTPASS 25K25
    # Drop sensitive keys
    def StatusKeyDrop(self, StatusData):
        try:
            RemoveKeys = self.DropKey
            for StatusRow in StatusData:
                for RemoveKey in RemoveKeys:
                    StatusRow.pop(RemoveKey, None)
            return StatusData
        except Exception as StatuDropError:
            logging.warning(StatuDropError)
    # TESTPASS 25K30
    # Webpage status output
    def StatusWebpage(self, DisplayData):
        try:
            # Table header
            StatusHeader = list(DisplayData[0].keys())
            # File path
            StatusWeb = Path(self.ClientsStatus)
            with open(StatusWeb, "w", newline="", encoding="utf-8") as StatusCSV:
                StatusWriter = csv.DictWriter(StatusCSV, fieldnames=StatusHeader)
                # Write header
                StatusWriter.writeheader()
                # Write clients row
                for Row in DisplayData:
                    StatusWriter.writerow(Row)
        except Exception as StatusWebError:
            logging.warning(StatusWebError)
    # TESTPASS 25K30
    # Save H@h clients data into separate CSV
    def StatusRecorder(self, DataInput):
        # Disable recording
        if isinstance(self.ActiveRecord, bool) and self.ActiveRecord is False:
            pass
        # Enable recording
        if isinstance(self.ActiveRecord, bool) and self.ActiveRecord is True:
            RecordingPath = Path(self.TapePath)
            DataInput: list[dict]
            try:
                RecordingPath.mkdir(parents=True, exist_ok=True)
                for DataRow in DataInput:
                    ClientName = DataRow.get("Client", None)
                    if ClientName is None:
                        continue
                    TapePath = RecordingPath / f"{ClientName}.csv"
                    FieldNames = list(DataRow.keys())
                    FileExists = TapePath.exists()
                    with TapePath.open("a", newline="", encoding="utf-8") as TapeWriter:
                        RowWriter = csv.DictWriter(TapeWriter, fieldnames=FieldNames)
                        if not FileExists:
                            RowWriter.writeheader()
                        RowWriter.writerow(DataRow)
            except Exception as RecordError:
                logging.warning(RecordError) 
    # TESTPASS 25K30

# Hentai@Home check
class EHentai():
    def __init__(self, ConfigFilePath):
        self.EHentaiConfig  = Configuration(ConfigFilePath).Load
        self.Member         = self.EHentaiConfig['EHentai']['ipb_member_id']
        self.Password       = self.EHentaiConfig['EHentai']['ipb_pass_hash']
        self.UserAgent      = self.EHentaiConfig['EHentai']['UserAgent']
        self.Com = Link()
        self.RtM = Runtime(ConfigFilePath)
    def CheckHentaiatHome(self):
        try:
            # Checking
            CheckRespon = requests.get(
                self.Com.HentaiAtHome,
                headers = {"user-agent": self.UserAgent},
                cookies = {"ipb_member_id": self.Member, "ipb_pass_hash": self.Password},
                timeout = 30)
            # HTTP Error
            if CheckRespon.status_code != 200:
                CheckRespon.close()
                logging.warning(CheckRespon.status_code)
                return CheckRespon.status_code
            # HTTP 200 OK
            elif CheckRespon.status_code == 200:
                CheckRespon.close()
            # BS4 kick-in
            ResponHTML = BeautifulSoup(CheckRespon.content, "html.parser")
            # Try to find table named hct, which contain HentaiAtHome status
            TableHCT = ResponHTML.find("table", id="hct")
            # Try to find login table
            TableLogIn = ResponHTML.find("table", id="d")
            # Check logout
            if TableLogIn and not TableHCT:
                NeedLogin = ("Require Login")
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
    # TESTPASS 25K30
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
    # UNT

# Alert function
class Alert():
    def __init__(self, ConfigFilePath):
        self.Com           = Link()
        self.RtM           = Runtime(ConfigFilePath)
        self.AlertConfig   = Configuration(ConfigFilePath).Load
        # Telegram
        self.BotToken      = self.AlertConfig['Telegram_BOTs']['Token']
        self.ChatID        = self.AlertConfig['Telegram_BOTs']['ChatID']
        # SMTP
        self.MailSender    = self.AlertConfig['Mail']['Sender']
        self.SenderScepter = self.AlertConfig['Mail']['Scepter']
        self.Receiver      = self.AlertConfig['Mail']['Receiver']
        # Stop alert Continuity
        self.Continuity    = self.AlertConfig['Alert']['ContinuityDisable']
        # Timestemp
        SendingTime        = datetime.datetime.now()
        self.SendingYMDHMS = SendingTime.strftime("%Y-%m-%d %H:%M:%S")
        self.SendingHMS    = SendingTime.strftime("%H:%M:%S")
    # Keep sending alert or not
    def StopAlert(self, Reset = (False)):
        # Keeping alert
        if isinstance(self.Continuity, bool) and self.Continuity is False:
            return 200
        # Enable stop alert
        if isinstance(self.Continuity, str):
            Blocker = Path(self.Continuity)
            # All client online
            if Reset is True:
                # Delete blocker
                try:
                    Blocker.unlink()
                    return 200
                # Blocker already delete
                except FileNotFoundError:
                    return 200
                # Fail-safe
                except Exception as StopAlertError:
                    logging.warning(StopAlertError)
                    return 200
            # Client offline
            if Reset is False:
                # Alert continuity set, stop alert
                if Blocker.exists():
                    return 400
                # Blocker not found, create blocker and alert
                else:
                    try:
                        with open(Blocker, "w") as BlockStone:
                            BlockStone.write(self.SendingYMDHMS)
                        return 200
                    # Fail-safe
                    except Exception as StopAlertError:
                        logging.warning(StopAlertError)
                        return 200
        # Fail-safe
        else:
            logging.warning("ContinuityDisable should be false of path string")
            return 200
    # UNT
    # Set default message for testing
    def Telegram(self, TelegramMessage = ('Here, the world!')):
        # Connetc URL
        TgURL = (self.Com.Telegram + f"{self.BotToken}/sendMessage")
        # Text content
        TgMsg = {"chat_id": f"{self.ChatID}", "text": TelegramMessage}
        try:
            TgResponse = requests.post(TgURL, json=TgMsg, timeout=30)
            if TgResponse.status_code == 200:
                TgResponse.close()
                self.RtM.Message(TelegramMessage)
            elif TgResponse.status_code == 400:
                TgResponse.close()
                self.RtM.Message("Telegram ChatID is empty, notifications will not be sent.")
                logging.warning(TgResponse.status_code)
            else:
                TgResponse.close()
                logging.warning(TgResponse.status_code)
        except Exception as TelegramErrorStatus:
            logging.warning(TelegramErrorStatus)
    # UNT
    # Get Telegram ChatID
    def GetTelegramChatID(self):
        # Connetc URL
        TgAskURL = (self.Com.Telegram + f"{self.BotToken}/getUpdates")
        try:
            TgAskResponse = requests.post(TgAskURL, timeout=30)
            if TgAskResponse.status_code == 200:
                TgAskData = json.loads(TgAskResponse.text)
                TgAskResponse.close()
                # Empty result
                if len(TgAskData['result']) == 0:
                    self.RtM.Message("You must send message to bot first.")
                # Select ChatID
                else:
                    CheckChatID = TgAskData["result"][0]['message']['chat']['id']
                    self.RtM.Message(f"Your ChatID is: {CheckChatID}")
            else:
                TgAskResponse.close()
                logging.warning(TgAskResponse.status_code)
        except Exception as TelegramGetIDError:
            logging.warning(TelegramGetIDError)
    # UNT
    # Sending mail alert, default using gmail smtp
    def Mail(self, MailMessage= ('Sweet Escape')):
        try:
            # Mail text
            MailMessage = MIMEText(MailMessage)
            # Mail title
            MailMessage["Subject"] = (f"Hentai@Home Offline | {self.SendingHMS}")
            MailMessage["From"] = self.MailSender
            MailMessage["To"] = self.Receiver
            # Connect to gmail server
            LinkSMTPServer = smtplib.SMTP(self.Com.SMTPServer, self.Com.SMTPPort)
            LinkSMTPServer.ehlo()
            LinkSMTPServer.starttls()
            LinkSMTPServer.login(self.MailSender, self.SenderScepter)
            # Sending
            LinkStatus = LinkSMTPServer.sendmail(
                self.MailSender, self.Receiver, MailMessage.as_string())
            # Close connection
            LinkSMTPServer.quit()
            return LinkStatus
        except Exception as MailErrorStatus:
            logging.warning(MailErrorStatus)
    # UNT
