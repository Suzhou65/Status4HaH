# Status4HaH
[![python](https://github.takahashi65.info/lib_badge/python.svg)](https://www.python.org/)
[![python version](https://github.takahashi65.info/lib_badge/python-3.6.svg)](https://www.python.org/) 
[![UA](https://github.takahashi65.info/lib_badge/active_maintenance.svg)](https://github.com/Suzhou65/Status4HaH)
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
    + [Screenshot](#screenshot)
## Usage
You need to have E-Hentai account, and already running Hentai@Home client.
### Scheduling and server loading
- Scheduling  
Using Crontab for job scheduling.
```shell
#MIM HOUR DAY MONTH WEEK
*/30  *    *    *    *    root  python /script_path/status_notification.py
```
```diff
- Avoiding for making heavy server load on E-Hentai.
- Not recommended for change less then 30 minutes.
```
### E-Hentai account
Using cookies to login is the same as using a browser extension or viewer.

If your browser is Chrome-based (ex. Google Chrome or Microsoft Edge), right-click to open Developer Tools and switch to the ```Network``` panel. After refreshing the [Hentai@Home](https://e-hentai.org/hentaiathome.php) page, click the element called hentaiathome.php, which tags cookies. You can find ```ipb_member_id``` and ```ipb_pass_hash```.

Please fill in the cookie's value inin theonfiguration file. If you didn't fill in the configuration, it will ask for the cookie when you run the script.
```text
Configuration not found, please initialize.

Please enter the ipb_member_id: 114514
Please enter the ipb_pass_hash: ••••••••••••••••••••••••••••••••
```
### Email alert
- Google account needed, sign in using App passwords.
- Receiver mail address is unlimited.

The first time you run the mail alert function, it will check the configuration file. If the mail configuration is not found, it will return a string ```Mail configuration not found, please initialize.```
### Telegram alert
- Using Telegram Bot, contect [BotFather](https://t.me/botfather) create new Bot accounts.
- HTTP ```API Token``` and ```chat id``` are needed.
- If the chat channel wasn't created, the Telegram API will return ```HTTP 400 Bad Request```. You need to start the chat channel, including that bot.

The first time you run the Telegram alert function, it will check the configuration file. If Telegram Bot configuration is not found, it will return the string ```Telegram configuration not found, please initialize.```
## Configuration file
- Status4HaH store configuration as JSON format file.
- Configuration file named ```status4hah.config.json```.

You can editing the clean copy, which looks like this:
```json
{
  "last_update_time": "",
  "ipb_member_id": "",
  "ipb_pass_hash": "",
  "request_header": "",
  "mail_sender": "",
  "mail_scepter": "",
  "mail_receiver": "",
  "telegram_token": "",
  "telegram_id": "",
  "alert_counting":false
}
```
If you fill in the correct configuration, it will skip the initialization check and running script.
## Modules instantiation
Some module not included in [Python Standard Library](https://docs.python.org/3/library/index.html) are needed.
- [pandas](https://pypi.org/project/pandas/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
## Security and Disclaimer
```diff
- Although the password inside the cookie has been hashed,
- if someone modifies the script, add a backdoor function to send it back.
- It's possible to login to your account without knowing the actual username and password.
- The original Status4HaH won't have those functions.
- Please make sure you download the clean copy from this repository.
```
## Import module
- Import as module
```python
import status4hentai
```
- Alternatively, you can import the function independently.
```python
from status4hentai import CheckHentaiatHome
```
## Function
### Get HentaiAtHome status
```python
# Get Hentai@Home Status
HentaiAtHomePayload = status4hentai.CheckHentaiatHome(ConfigFilePath)
# Check Hentai@Home status
StatusTable = status4hentai.GetHentaiStatus(HentaiAtHomePayload)
```
- It will return ```Pandas DataFrame``` if parsing HTML content correctly.
- If return ```string``` means controllable error, like server error or logout, that string maybe HTTP Status Code, or Python requests function timeout.
- If return ```boolean``` means exception error, please check ```status4hah.error.log``` for error handling.
### Offline notification
- The demonstration script is```status_notification.py```.
- Configuration as follows are needed.
```python
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
```
When login cookie expires, you will receive an alert message: ```Cookie expires. Please update the configuration file```.
### Status recorder
- The demonstration script is```status_recorder.py```.
- Configuration as follows are needed.
```python
# Configuration file path
ConfigFilePath = "status4hah.config.json"
# Runtime file and path
StatusFilePath = "status4hah.status.csv"
# Recording file filter
RecordingFilter = ["ID","Created","Client IP","Port","Version","Max Speed","Country"]
# Recording file path
RecordingPath = "status4hah.record.csv"
```
### Web Based Monitor
```status_monitor.php``` is a simple php script webpage to view the status file generated by ```status_notification.py```.

- See the [Demonstration](https://takahashi65.info/page/status_monitor.php).
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
- php 7.3 or above, recommend using php-FPM
## License
General Public License -3.0
## Resources
### Beautiful Soup
- [Beautiful Soup 4.9.0 documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
### E-Hentai
- [About Hentai@Home](https://ehwiki.org/wiki/Hentai@Home)
### Install HentaiatHome
- [Raspbian install Hentai@Home, setting environment](https://gist.github.com/Suzhou65/3323c05432c0276487c6e21486e3ca80)
- [Raspbian install Hentai@Home, mount external hard drive](https://gist.github.com/Suzhou65/a68c44f343953fc245f6d4438cdbab77)
- [Raspbian install Hentai@Home, initialization are starting](https://gist.github.com/Suzhou65/8207e6c7487bf303cc7615ad94352e42)
### Stack Overflow
- [python BeautifulSoup parsing table](https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table)
### Screenshot
- [Screenshot of demonstration](https://gist.github.com/Suzhou65/b0632fcf8e179c5e58e96b2de127cbcc)
