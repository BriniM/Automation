# Automation
A set of programs that automate certain tasks, this project relies on a set of dependencies; run:
```
pip install -r requirements.txt
```

## @everyone in groups
Edit the `get_session.py` file to include your mail and password, and then run the script once.
Fire up `everyone.py` and you're good to go, whenever @everyone is sent in a group, you'll quote the participants.

## Internet stresser
The `internet_stresser.py` script relies on the CURL Library for downloading files.
You may need to set it up via either of these commands:
```
sudo apt update && sudo apt upgrade
sudo apt install curl
```

```
choco install curl
```

## GMeet
The script records meeting sessions found in the User's calendar.
First of all start by adding your events to your Google Calendar and attribute a description.
The description can be the URL to the Meet session or you can store those locally which is the case here ```meet links.txt```
Next, you want to enable the Google Calendar API from [here](https://developers.google.com/calendar/quickstart/python) and download the credentials.json file, place it in the root directory of the script.
Download ShareX (An Open source [C# Recording software](https://github.com/ShareX/ShareX)) and leave it open while you run the script.
If your screen resolution is 1366x768, the script will work right off the bat, otherwise you will need to modify the (X,Y) Coordinates used while turning off the mic, camera and joining the meeting session.


