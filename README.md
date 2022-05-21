# Status4HaH
[![python](https://github.takahashi65.info/lib_badge/python.svg)](https://www.python.org/)
[![python version](https://github.takahashi65.info/lib_badge/python-3.6.svg)](https://www.python.org/) 
[![UA](https://github.takahashi65.info/lib_badge/active_development.svg)](https://github.com/Suzhou65/Status4HaH)
[![Size](https://github-size-badge.herokuapp.com/Suzhou65/Status4HaH.svg)](https://github.com/axetroy/github-size-badge)

Status check for Hentai@Home Client.

## Contents
- [Status4HaH](#status4hah)
  * [Contents](#contents)
  * [Usage](#usage)
    + [Scheduling and server loading](#scheduling-and-server-loading)
    + [E-Hentai account](#e-hentai-account)
    + [Email sending](#email-sending)
  * [Configuration file](#configuration-file)
  * [Modules instantiation](#modules-instantiation)
  * [Security and Disclaimer](#security-and-disclaimer)
  * [Import module](#import-module)
  * [Function](#function)
    + [Get HentaiAtHome status](#get-hentaiathome-status)
    + [Offline checker](#offline-checker)
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

If you browser is Google Chrome, right click to opening DevTools, switch to ```Network``` panel. After refresh [Hentai@Home](https://e-hentai.org/hentaiathome.php) page, click the element call ```hentaiathome.php```, you can find ```ipb_member_id```, ```ipb_pass_hash```  and ```ipb_session_id``` at HTTP header.

First time running this checker, it will asking the cookies.
```text
Configuration not found, please initialize.

Please enter the ipb_member_id: 114514
Please enter the ipb_pass_hash: ••••••••••••••••••••••••••••••••
Please enter the ipb_session_id: ••••••••••••••••••••••••••••••••
```
If cookire expired, it will asking for update.
```text
Data expired, please enter data again.

Please enter the ipb_pass_hash: ••••••••••••••••••••••••••••••••
Please enter the ipb_session_id: ••••••••••••••••••••••••••••••••
```
If you doesn't went to stuck in login retry, you can also set ```disalbe_retry``` to ```True```.
```python
hentai_status(disalbe_retry=True)
```
When cookie data expired, it wil return ```True```. It's different from error occurred, which return ```False``` as result.

### Email sending
- Google account needed, sign in using App passwords.
- Receiver is unlimited.

First time running email sending, it will asking configuration.
```text
Mail Configuration not found, please initialize.

Please enter the sender account: example@gmail.com
Please enter the sender password: •••••••••
Please enter the receiver address: receiver@gmail.com
```

You can also set ```disalbe_phone_book``` to ```True```, directly setting email configuration.
```python
#Email configuration Mode
disalbe_phone_book = False
#Email configuration
if bool(disalbe_phone_book) is True:
    sender = "example@gmail.com"
    scepter = "••••••••••••••••"
    receiver = "receiver@gmail.com"
elif bool(disalbe_phone_book) is False:
    mail_config = status4hentai.configuration(update_config=False)
    #Try to read configuration
    sender_account = mail_config["sender"]
    sender_password = mail_config["scepter"]
    receiver = mail_config["receiver"]

soup_alert(soup_menu, sender_account, sender_password, receiver, disalbe_phone_book=True)
```

## Configuration file
Status4HaH store configuration as JSON format file, named ```config.json```.

You can editing the clean copy, which looks like this:
```json
{
  "last_update_time": "",
  "ipb_member_id": "",
  "ipb_pass_hash": "",
  "ipb_session_id": "",
  "sender": "example@gmail.com",
  "scepter": "",
  "receiver": "receiver@gmail.com"
}
```
If you fill in with correct configure, it will skip initialization step.

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
```python
import status4hentai as hentai
```
- Alternatively, you can import the function independent
```python
from status4hentai import hentai_status
```

## Function
### Get HentaiAtHome status
```python
from status4hentai import hentai_status
status_list = hentai_status()

if type(status_list) is bool:
  if status_list is False:
    print("Error occurred when parsing.")
  elif status_list is True:
    print("Unable to login E-Hentai, Login retry is disable.")
elif type(status_frame) is list:
  print(status_list)
else:
  print("Data type should be list, please disable 'output_dataframe=True'.")
```
by default, it will return list as result:
```python
[
  ['Server_Enis','•••••','Online','2017-09-12','Today 13:17','28265461','•••.••.•••.•••','80','1.6.1 Stable','2000 KB/s','+1000','4572','3.7','2.6','Taiwan'],
  ['Server_Zwi','•••••','Online''2017-09-16','Today 13:18','36396067','•••.•••.•••.•••','80','1.6.1 Stable','2500 KB/s','+1000','5757','4.2','2.9','Moldova']
  ]
```
If you want to return pandas DataFrame, set ```output_dataframe``` to ```True```:
```python
status_frame = hentai_status(output_dataframe=True)

if type(status_frame) is bool:
  if status_frame is False:
    print("Error occurred when parsing.")
  elif status_frame is True:
    print("Unable to login E-Hentai, Login retry is disable.")
elif type(status_frame) is list:
  print("Data type should be DataFrame, please set 'output_dataframe=True'.")
else:
  print(status_frame)
```
It will return DataFrame as result:

 Client      | ID    | Status | Created    | Last Seen   | Files Served | Client IP       | Port | Version      | Max Speed | Trust | Quality | Hitrate | Hathrate | Country 
-------------|:------|-------:|-----------:|------------:|-------------:|----------------:|-----:|-------------:|----------:|------:|--------:|--------:|---------:|---------
 Server_Enis | ••••• | Online | 2017-09-12 | Today 13:17 |   28265461   | •••.••.•••.•••  |  80  | 1.6.1 Stable | 2000 KB/s | +807  | 4933    | 3.7     | 2.6      | Taiwan
 Server_Zwi  | ••••• | Online | 2017-09-16 | Today 13:18 |   36396067   | •••.•••.•••.••• |  80  | 1.6.1 Stable | 2500 KB/s | +982  | 3921    | 4.1     | 2.9      | Moldova

If you enable ```disalbe_retry```, it will return ```True``` as result when cookie data expired.
```python
status_frame = hentai_status(output_dataframe=True, disalbe_retry=True)
```
If error occurred, it will return ```False```.

### Offline checker
- Return list as result by default:
```python
from status4hentai import hentai_status
status_list = hentai_status(disalbe_retry=True)

if type(status_list) is bool:
  if status_list is False:
    print("Error occurred when parsing.")
  elif status_list is True:
    print("Unable to login E-Hentai, Login retry is disable.")
elif type(status_list) is list:
  finder = "Offline"
  if any(finder in sub for sub in status_list):
    print("Server offline")
  else:
    print("Server online")
else:
  print("Data type should be list, please disable 'output_dataframe=True'.")
```
If the H@H client is offline, it will print:
```
Server offline
```
Otherwise, it will print:
```text
Server online
```

- If you wnat to return pandas DataFrame as result:
```python
import pandas
from status4hentai import hentai_status
status_frame = hentai_status(output_dataframe=True, disalbe_retry=True)

if type(status_frame) is bool:
  if status_frame is False:
    print("Error occurred when parsing.")
  elif status_frame is True:
    print("Unable to login E-Hentai, Login retry is disable.")
elif type(status_frame) is list:
  print("Data type should be DataFrame, please set 'output_dataframe=True'.")
else:
  finder = "Offline"
  if finder in status_frame.values:
    print("Server offline")
  else:
    print("Server online")
```
If the H@H client is offline, it will print:
```
Server offline
```
Otherwise, it will print:
```text
Server online
```

### Offline notification
```python
import pandas
import status4hentai
status_frame = status4hentai.hentai_status(output_dataframe=True)

mail_spoon = ["Created","Files Served","Client IP","Port","Version","Max Speed","Trust","Quality","Hitrate","Hathrate","Country"]

if type(status_frame) is bool:
  if status_frame is False:
    print("Error occurred when parsing.")
  elif status_frame is True:
    print("Unable to login E-Hentai, Login retry is disable.")
elif type(status_frame) is list:
  print("Data type should be DataFrame, please set 'output_dataframe=True'.")
else:
  finder = "Offline"
  if finder in status_frame.values:
    filtering = status_frame.loc[status_frame["Status"] == finder].drop(mail_spoon, axis=1).to_string(header=False, index=False)
    soup_menu =filtering.replace("\n"," ; ")
    status4hentai.soup_alert(soup_menu)
    print("Server offline")
  else:
    print("Server online")
```
If the H@H client is offline, it will print meaasge and sending mail.
```
Server offline
```
Otherwise, it will print:
```text
Server online
```

### Status recorder
- Using list mode  
Recommend for single Hentai@Home client condition.
```python
import csv
from status4hentai import hentai_status

status_list = hentai_status()

if type(status_list) is bool:
  if status_list is False:
    print("Error occurred when parsing.")
  elif status_list is True:
    print("Unable to login E-Hentai, Login retry is disable.")
elif type(status_list) is list:
  with open("status_recoder.csv", "a") as soup_list:
    for line in status_list:
      soup_list.write(";".join([str(i) for i in line]))
      soup_list.write("\n")
else:
  print("Data type should be list, please disable 'output_dataframe=True'.")
```
- Using pandas DataFrame mode  
Recommend for multi Hentai@Home client condition. You can easily separate DataFrame by client or ID.
```python
import pandas
from status4hentai import hentai_status

status_frame = hentai_status(output_dataframe=True)

if type(status_frame) is bool:
  if status_frame is False:
    print("Error occurred when parsing.")
  elif status_frame is True:
    print("Unable to login E-Hentai, Login retry is disable.")
elif type(status_frame) is list:
  print("Data type should be DataFrame, please set 'output_dataframe=True'.")
else:
  #Separate by client name.
  #Server_1
  server_enis = status_frame.loc[status_frame["Client"] == "Server_Enis"]
  server_enis.to_csv("status_recoder_01.csv", mode="a", index=False, header=False)
  #Server_2
  server_zwei = status_frame.loc[status_frame["Client"] == "Server_Zwei"]
  server_zwei.to_csv("status_recoder_02.csv", mode="a",index=False, header=False)
```

### Web Based Monitor
```status_monitor.php``` is a simple php script to view the status file generated by ```status_notification.py```.

See the [Example](https://takahashi65.info/page/status_monitor.php), and the [Screenshot](https://gist.github.com/Suzhou65/b0632fcf8e179c5e58e96b2de127cbcc).

## Dependencies
### Python version
- Python 3.6 or above
### Python module
- beautifulsoup4
- csv
- datetime
- email
- getpass
- json
- logging
- pandas
- requests
- smtplib
- schedule
- time

### Webpage
- apache2, verson 2.4.46 or above
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
