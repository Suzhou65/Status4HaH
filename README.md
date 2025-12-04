# Status4HaH
[![python](https://github.takahashi65.info/lib_badge/python.svg)](https://www.python.org/)
[![UA](https://github.takahashi65.info/lib_badge/active_maintenance.svg)](https://github.com/Suzhou65/Status4HaH)
[![Size](https://img.shields.io/github/repo-size/Suzhou65/Status4HaH)](https://shields.io/category/size)

Status check for Hentai@Home Client.

## Contents
- [Status4HaH](#status4hah)
  * [Contents](#contents)
  * [Development Purpose](#development-purpose)
  * [Security and Disclaimer](#security-and-disclaimer)
  * [Limitation](#limitation)
  * [Usage](#usage)
    + [E-Hentai](#e-hentai)
    + [Hentai@Home](#hentaihome)
    + [Scheduling](#scheduling)
    + [Email alert](#email-alert)
    + [Telegram alert](#telegram-alert)
  * [Configuration file](#configuration-file)
  * [Modules instantiation](#modules-instantiation)
  * [Import module](#import-module)
  * [Function](#function)
    + [Get HentaiAtHome status](#get-hentaiathome-status)
    + [Offline notification](#offline-notification)
    + [Status recorder](#status-recorder)
    + [Web Based Monitor](#web-based-monitor)
  * [Dependencies](#dependencies)
    + [Python version](#python-version)
    + [Python module](#python-module)
    + [Webpage](#webpage)
    + [PHP](#php)
  * [License](#license)
  * [Resources](#resources)
    + [Beautiful Soup](#beautiful-soup)
    + [Hentai@Home distribution system](#hentaihome-distribution-system)
    + [Install HentaiatHome](#install-hentaiathome)
    + [Stack Overflow](#stack-overflow)
    + [Screenshot](#screenshot)

## Development Purpose
Supervise the operational status of multiple Hentai@Home clients and dispatch alerts upon detecting offline conditions. It transmission the offline alerts either as a one-only notification or on a continuous mode. Alerts may be dispatched through email or Telegram. It also facilitates the export of client operation status data, with the default setting segmenting data on a per-client IDs.

## Security and Disclaimer
> **Security**  
> Although the password inside the cookie has been hashed, if someone modifies the script, add a backdoor function to send it back.  
> It's possible to login to your account without knowing the actual username and password.  
>
> **Disclaimer**  
> The original Status4HaH won't have those functions.  
> Please make sure you download the clean copy from this repository.  

## Limitation
If the **Once-only** mode is set for alert function, no more alerts will be delivered. Even if more Hentai@Home clients offline during after alert sending, alert function will enable again after Hentai@Home clients come back online. Same thing happens when **webpage parsing errors** or **network errors** happen.

## Usage
### E-Hentai
> **Using cookies to login**  
> If your browser is Chrome-based (ex. Google Chrome or Microsoft Edge), right-click to open Developer Tools and switch to the ```Network``` panel. After refreshing the [Hentai@Home](https://e-hentai.org/hentaiathome.php) page, click the element called hentaiathome.php, which tags cookies. You can find ```ipb_member_id``` and ```ipb_pass_hash```. please fill into the configuration file.

> **HTTP User-Agent Header**  
> Pleae copy your browser's `User-Agent`, fill into the configuration file.

### Hentai@Home
You should already running Hentai@Home client.

### Scheduling
Using Crontab for job scheduling. systemd also recommended.
```conf
#MIM HOUR DAY MONTH WEEK
*/30  *    *    *    *    root  python /script_path/status_notification.py
```
> **Avoiding for making heavy server load on E-Hentai**  
>  Not recommended for change less then 30 minutes.

### Email alert
Using Gmail as default. configuration at line 24 to 25.
```python
# Web and mail config
class Link():
    def __init__(self):
        self.HentaiAtHome = "https://e-hentai.org/hentaiathome.php"
        self.Telegram     = "https://api.telegram.org/bot"
        self.SMTPServer   = "smtp.gmail.com"
        self.SMTPPort     =  587
```
> **Note**  
> Google account needed, sign in using App passwords, receiver mail address is unlimited.  
> You may replace it with any other mail server that supports SMTP.

### Telegram alert
sing Telegram Bot, contect [BotFather](https://t.me/botfather) create new Bot accounts.

At this point chat channel wasn't created, so you can't find the `ChatID`. Running `Message2Me` function will receive `400 Bad Request` from Telegram API, following message will printout:
```
19:19:00 | Telegram ChatID is empty, notifications will not be sent.
```
You need to start the chat channel with that bot, i.e. say `Hello the world` to him. Then running `GetTelegramChatID`
```python
import status4haha
ConfigFilePath = "/Documents/script/status4hah.config.json"
Al = status4haha.Alert(ConfigFilePath)
Al.GetTelegramChatID()
```
Now ChatID will printout:
```
19:19:18 | You ChatID is: XXXXXXXXX
```

## Configuration file
Using JSON format file storage configuration.
```json
{
  "EHentai": {
    "UserAgent": "",
    "ipb_member_id": "",
    "ipb_pass_hash": "",
    "TableHeader": [
      "Client","ID","Status","Created","Last Seen",
      "Files Served","Client IP","Port","Version","Max Speed",
      "Trust","Quality","Hitrate","Hathrate","Region"]
  },
  "RuntimeStatus": {
    "StatusPath": "/var/www/html/status4hah.runtime.csv"
  },
  "DisplayDrop": { 
    "OutputPath": "/var/www/html/status4hah.status.csv",
    "Filter": ["ID","Created","Client IP","Port"]
  },
  "Recording":{
    "StatusRecord": false,
    "RecordingPath": "/Documents/script/record/"
  },
  "Alert": {
    "Mode": false,
    "ContinuousAlert": false
   },
   "Telegram_BOTs": {
      "Token": "",
      "ChatID": ""
   },
   "Mail": {
    "Sender": "",
    "Scepter": "",
    "Receiver": ""
   }  
}
```
Configuration file must include following parameters:


## Modules instantiation
Module not included in [Python Standard Library](https://docs.python.org/3/library/index.html) are needed.
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

## Import module
```python
# Import as module
import status4hentai
# Alternative
import status4hentai as s4h
```

## Function
### Get HentaiAtHome status
```python
import status4hentai as s4h

# Configuration file path
ConfigFilePath = "/Documents/script/status4hah.config.json"

Eh = s4h.EHentai(ConfigFilePath)
Rt = s4h.Runtime(ConfigFilePath)
# Get Hentai@Home status
ClientStatus = Eh.CheckHentaiatHome()
# Error
if isinstance(ClientStatus, bool):
  Rt.StatusRuntime("Error occurred during connect to E-hentai.")
# E-Hentai server HTTP error
elif isinstance(ClientStatus, int):
  Rt.StatusRuntime(f"E-Hentai Server Error: {ClientStatus}")
# E-Hentai Logout
elif isinstance(ClientStatus, str):
  Rt.StatusRuntime(ClientStatus)
# Get Hentai@Home status
elif isinstance(ClientStatus, list):
  print(ClientStatus)
```
> **Output:**  
> ```list``` object parsing HTML content correctly.  
> ```String``` meaning account logout.  
> ```Integer``` meaning HTTP status codes, mostly E-Hentai server or Cloudflare CDN issue.  
> ```Boolean```meaning undefined error, please review the error handling in ```error.status4hah.log```.

### Offline notification
Demonstration script named `status_notification.py`.
```python
import status4hentai as s4h
from sys import exit

# Configuration file path
ConfigFilePath = "/Documents/script/status4hah.config.json"
# Script
def main():
    Rt = s4h.Runtime(ConfigFilePath)
    Eh = s4h.EHentai(ConfigFilePath)
    Al = s4h.Alert(ConfigFilePath)
    # Get Hentai@Home status
    ClientStatus = Eh.CheckHentaiatHome()
    # Error
    if isinstance(ClientStatus, bool):
        raise Exception()
    # E-Hentai server HTTP error
    elif isinstance(ClientStatus, int):
        raise Exception()
    # E-Hentai Logout
    elif isinstance(ClientStatus, str):
        Al.Alarm(ClientStatus)
        raise Exception()
    # Get Hentai@Home status
    elif isinstance(ClientStatus, list):
        pass
    # Undefined error
    else:
        raise Exception()
    # Check online status
    OfflineClient = Eh.OfflineChecker(ClientStatus)
    if isinstance(OfflineClient, bool):
        raise Exception()
    elif isinstance(OfflineClient, list):
        if len(OfflineClient) == 0:
            # Delete continuous alert blocker
            Al.RemoveObstacle()
        else:
            OfflineNotify = (f"Hentai@Home client offline.\r\nClient Name: {OfflineClient}")
            Al.Alarm(OfflineNotify)
# Runtime
if __name__ == "__main__":
    try:
        main()
    except Exception:
        exit(0)
```

### Status recorder
Demonstration script named `status_recorder.py`.
```python
import status4hentai as s4h
from sys import exit

# Configuration file path
ConfigFilePath = "/Documents/script/status4hah.config.json"
# Script
def main():
    Rt = s4h.Runtime(ConfigFilePath)
    Eh = s4h.EHentai(ConfigFilePath)
    # Get Hentai@Home status
    ClientStatus = Eh.CheckHentaiatHome()
    # Error
    if isinstance(ClientStatus, bool):
        raise Exception()
    # E-Hentai server HTTP error
    elif isinstance(ClientStatus, int):
        raise Exception()
    # E-Hentai Logout
    elif isinstance(ClientStatus, str):
        raise Exception()
    # Get Hentai@Home status
    elif isinstance(ClientStatus, list):
        # Drop key
        Rt.StatusKeyDrop(ClientStatus)
        # Writing into CSV file
        Rt.StatusRecorder(ClientStatus)
    # Undefined error
    else:
        Rt.Message(f"Undefined error occurred.")
        raise Exception()
# Runtime
if __name__ == "__main__":
    try:
        main()
    except Exception:
        exit(0)
```

### Web Based Monitor
`status_monitor.php` is a simple php script webpage to view the status file output via `status_notification.py`.

> **Demonstration**  
> See the [Demonstration](https://takahashi65.info/page/status_monitor.php).

## Dependencies
### Python version
Testing passed on above Python version:
- 3.7.3
- 3.9.2
- 3.9.6
- 3.12.11

### Python module
- logging
- pathlib
- json
- datetime
- textwrap
- csv
- requests
- bs4
- email
- smtplib

### Webpage
- Apache or NGINX

### PHP
- php 7.3 or above, recommend using php-FPM

## License
General Public License -3.0

## Resources
### Beautiful Soup
- [Beautiful Soup 4.9.0 documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
### Hentai@Home distribution system
- [About Hentai@Home](https://ehwiki.org/wiki/Hentai@Home)
### Install HentaiatHome
- [Raspbian install Hentai@Home, setting environment](https://gist.github.com/Suzhou65/3323c05432c0276487c6e21486e3ca80)
- [Raspbian install Hentai@Home, mount external hard drive](https://gist.github.com/Suzhou65/a68c44f343953fc245f6d4438cdbab77)
- [Raspbian install Hentai@Home, initialization are starting](https://gist.github.com/Suzhou65/8207e6c7487bf303cc7615ad94352e42)
### Stack Overflow
- [python BeautifulSoup parsing table](https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table)
### Screenshot
- [Screenshot of demonstration](https://gist.github.com/Suzhou65/b0632fcf8e179c5e58e96b2de127cbcc)
