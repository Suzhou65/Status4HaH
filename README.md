# Status4HaH
[![python](https://github.takahashi65.info/lib_badge/python.svg)](https://www.python.org/)
[![python version](https://github.takahashi65.info/lib_badge/python-3.6.svg)](https://www.python.org/) 
[![UA](https://github.takahashi65.info/lib_badge/active_development.svg)](https://github.com/Suzhou65/Status4HaH)
[![Size](https://img.shields.io/github/repo-size/Suzhou65/Status4HaH)](https://shields.io/category/size)

Status check for Hentai@Home Client.

## Contents
- [Status4HaH](#status4hah)
  * [Contents](#contents)
  * [Usage](#usage)
    + [Scheduling and server loading](#scheduling-and-server-loading)
    + [E-Hentai account](#e-hentai-account)
    + [Email alert](#email-alert)
    + [Telegram alert](#telegram-alert)
  * [Configuration file](#configuration-file)
  * [Modules instantiation](#modules-instantiation)
  * [Security and Disclaimer](#security-and-disclaimer)
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
  * [License](#license)
  * [Resources](#resources)
    + [Beautiful Soup](#beautiful-soup)
    + [E-Hentai](#e-hentai)
    + [Install HentaiatHome](#install-hentaiathome)
    + [Stack Overflow](#stack-overflow)

## Usage
You need to have E-Hentai account, and already running Hentai@Home client.
### Scheduling and server loading
- Scheduling  
Using schedule module for job scheduling, you can found the scheduling setting at scripts examples.
- Avoiding for making heavy server load on E-Hentai
```diff
- Default interval at scripts is 30 minutes, not recommended for change less then 30 minutes.
```

### E-Hentai account
Using cookies to login, same as browser extension or viewer.

If you browser is Chromium based, right click to opening Developer Tools, switch to ```Network``` panel. After refresh [Hentai@Home](https://e-hentai.org/hentaiathome.php) page, click the element call ```hentaiathome.php```, you can find ```ipb_member_id```, ```ipb_pass_hash```  and ```ipb_session_id``` at HTTP header.

First time running this checker, it will asking the cookies.
```text
Configuration not found, please initialize.

Please enter the ipb_member_id: 114514
Please enter the ipb_pass_hash: ••••••••••••••••••••••••••••••••
Please enter the ipb_session_id: ••••••••••••••••••••••••••••••••
```
### Email alert
- Google account needed, sign in using App passwords.
- Receiver is unlimited.

First time running mail alert function, it will check configuration file. If mail configuration not found, it will print alert.
```text
Mail configuration not found, please initialize.
```
And return integer values ```404```.
### Telegram alert
- Using Telegram BOTs, contect [BotFather](https://t.me/botfather) create new bot accounts.
- HTTP ```API Token``` and ```chat id``` are needed.
- If the chat channel wasn't create, Telegram API will return HTTP code 400.

First time running Telegram alert function, it will check configuration file. If mail configuration not found, it will print alert.
```text
Telegram configuration not found, please initialize.
```
And return integer values ```404```.

## Configuration file
- Status4HaH store configuration as JSON format file.
- Configuration file named ```status4hah.config.json```.

You can editing the clean copy, which looks like this:
```json
{
  "last_update": "",
  "ipb_member_id": "",
  "ipb_pass_hash": "",
  "ipb_session_id": "",
  "mail_sender": "",
  "mail_scepter": "",
  "mail_receiver": "",
  "telegram_token": "",
  "telegram_id": ""
}
```
If you fill in with correct configure, it will skip initialization check and alert.

## Modules instantiation
Some module not included in [Python Standard Library](https://docs.python.org/3/library/index.html) are needed.
- [pandas](https://pypi.org/project/pandas/)
- [schedule](https://pypi.org/project/schedule/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

## Security and Disclaimer
Although **ipb_pass_hash** is the password which has been hashed.
```diff
- If someone modify the script, adding function to send it back with ipb_member_id.
- it's possible to login your account without knowing the actual username and password.
+ Original Status4HaH won't have those function.
+ Please make sure you download the clean copy from this Repository.
```

## Import module
- Import as module
```python
import status4hentai
```
- Alternatively, you can import the function independent
```python
from status4hentai import GetHentaiStatus
```

## Function
### Get HentaiAtHome status
```python
# Get Hentai@Home Page
ResponPayload = status4hentai.CheckHentaiatHome(ConfigFilePath)
# Check Hentai@Home status
DataTableOutput = status4hentai.GetHentaiStatus(ResponPayload)
```
- It will return ```Pandas DataFrame``` if parsing HTML content correctly.
- If return ```string``` means controllable error, like server error or logout,
- If return ```boolean``` means exception error.
### Offline notification
- The demonstration script is```status_notification.py```.
- Configuration as follows are needed.
```python
# Configuration file path
ConfigFilePath = "status4hah.config.json"
# Status file path
CheckingResultPath = "status4hah.check.csv"
# Create status file
StatusFilePath = "status4hah.status.csv"
# Alert mode selection
AlertMode = 0
```
### Status recorder
- The demonstration script is```status_recorder.py```.
- Configuration as follows are needed.
```python
# Configuration file path
ConfigFilePath = "status4hah.config.json"
# Recording file path
RecordingPath = "status4hah.record.csv"
# Create status file
StatusFilePath = "status4hah.status.csv"
```
### Web Based Monitor
```status_monitor.php``` is a simple php script webpage to view the status file generated by ```status_notification.py```.

See the [Example](https://takahashi65.info/page/status_monitor.php), and the [Screenshot](https://gist.github.com/Suzhou65/b0632fcf8e179c5e58e96b2de127cbcc).

## Dependencies
### Python version
- Python 3.6 or above
### Python module
- sys
- time
- json
- pandas
- logging
- smtplib
- requests
- datetime
- getpass
- BeautifulSoup
- MIMEText

### Webpage
- Apache or NGINX
- php 7.3 or above

## License
General Public License -3.0

## Resources
### Beautiful Soup
- [Beautiful Soup 4.9.0 documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Beautiful Soup 4.4.0 documentation, Zh-CN](https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/)

### E-Hentai
- [About Hentai@Home](https://ehwiki.org/wiki/Hentai@Home)

### Install HentaiatHome
- [Raspbian install Hentai@Home, setting environment](https://gist.github.com/Suzhou65/3323c05432c0276487c6e21486e3ca80)
- [Raspbian install Hentai@Home, mount external hard drive](https://gist.github.com/Suzhou65/a68c44f343953fc245f6d4438cdbab77)
- [Raspbian install Hentai@Home, initialization are starting](https://gist.github.com/Suzhou65/8207e6c7487bf303cc7615ad94352e42)

### Stack Overflow
- [python BeautifulSoup parsing table](https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table)
