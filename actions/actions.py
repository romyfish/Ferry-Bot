# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import ReminderScheduled, ReminderCancelled

import json
import datetime
import re

today_date = datetime.datetime.now().strftime("%Y-%m-%d")
tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=1)
week_ls = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# get the id and the date of the next event
rfile = open('./database.json', 'r')
content = rfile.read()
data = json.loads(content)
rfile.close()
for event in data["events"]:
    event_date = datetime.datetime.strptime(event["date"],'%Y-%m-%d')
    if datetime.datetime.now() < event_date:
        # when find the event take place tomorrow or later
        next_event_ID = event["id"]
        next_event_date = event_date
        break

# the time to send the checking notification to users
send_time = datetime.time(10, 30)

class ActionSetNotify(Action):
    """Schedules a notification to checking if the user will attend events"""

    def name(self) -> Text:
        return "action_set_notify"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # query from database for the event day and set the notifying datetime before
        # send_date = next_event_date - datetime.timedelta(days=1)
        # date = datetime.datetime.combine(send_date, send_time)
        date = datetime.datetime.now() + datetime.timedelta(seconds=30)
        str_date = datetime.datetime.strftime(date,'%Y-%m-%d %H:%M:%S')
        dispatcher.utter_message("Confirmed. I will check with you at {}".format(str_date))
        # dispatcher.utter_message("Confirmed. I will check with you the day before the event every week.")

        reminder = ReminderScheduled(
            "EXTERNAL_notify",
            trigger_date_time=date,
            name="event_notify",
            kill_on_user_message=False,
        )

        return [reminder]
    
class ActionNotifyTriggered(Action):
    """Check the event time with user"""

    def name(self) -> Text:
        return "action_notify_triggered"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        rfile = open('./database.json', 'r')
        content = rfile.read()
        data = json.loads(content)
        rfile.close()
        event_name = data["events"][next_event_ID]["content"]
        dispatcher.utter_message(text="Are you free to attend the offline group {} tomorrow?".format(event_name))

        return []

class ActionGetAffirm(Action):

    def name(self) -> Text:
        return "action_get_affirm"

    def run(self, dispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # --- record the individual available and report to backend/manager ---
        conversation_id = tracker.sender_id   # tracker.sender_id / "6490110454383266"
        rfile = open('./database.json', 'r')
        content = rfile.read()
        data = json.loads(content)
        rfile.close()
        for user in data["users"]:
            if user["chatID"] == conversation_id:
                userID = user["id"]
                break
        data["events"][next_event_ID]["participants"][userID] = "affirm"
        new_json = json.dumps(data, indent=4)
        wfile = open('./database.json', 'w')
        wfile.write(new_json)
        wfile.close()

        dispatcher.utter_message(text="Lovely! See you then!")

        return []
    
class ActionRecordUnwill(Action):

    def name(self) -> Text:
        return "action_record_unwilling"

    def run(self, dispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # --- ! record the individual unavailable and report to backend/manager ---
        conversation_id = tracker.sender_id
        rfile = open('./database.json', 'r')
        content = rfile.read()
        data = json.loads(content)
        rfile.close()
        for user in data["users"]:
            if user["chatID"] == conversation_id:
                userID = user["id"]
                break
        data["events"][next_event_ID]["participants"][userID] = "refuse"
        new_json = json.dumps(data, indent=4)
        wfile = open('./database.json', 'w')
        wfile.write(new_json)
        wfile.close()

        dispatcher.utter_message(text="Okay, no worries. Hope to see you soon!")

        return []
    
class ActionRecordTime(Action):

    def name(self) -> Text:
        return "action_record_time"

    def run(self, dispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        day_text = tracker.get_slot("day")

        # --- ! record the new time and report to backend/manager ---
        # identify the new date
        digit_date = []
        digit_date = re.findall("\d+", day_text)
        if digit_date != []:   # if user give the specific date
            new_day = digit_date[0]
            if int(new_day) > tomorrow_date.day:   # compare the month
                new_date = tomorrow_date.strftime("%Y-%m-") + str(new_day).zfill(2)
            else:
                new_date = tomorrow_date.strftime("%Y-") + str(tomorrow_date.month+1).zfill(2) + "-" + str(new_day).zfill(2)
        elif day_text == "tommorow":
            new_date = tomorrow_date.strftime("%Y-%m-%d")
        elif day_text == "day after tomorrow":
            new_date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        elif day_text in week_ls:   # if user give the weekday
            # match the weekday with the date (assume in this week)
            ddays = week_ls.index(day_text) - tomorrow_date.weekday()
            new_date = (tomorrow_date + datetime.timedelta(days=ddays)).strftime("%Y-%m-%d")
        else:
            # deal with other situation
            new_date = "2001-01-01"
        conversation_id = tracker.sender_id   # tracker.sender_id / "6490110454383266"
        rfile = open('./database.json', 'r')
        content = rfile.read()
        data = json.loads(content)
        rfile.close()
        for user in data["users"]:
            if user["chatID"] == conversation_id:
                userID = user["id"]
                break
        data["events"][next_event_ID]["participants"][userID] = new_date
        new_json = json.dumps(data, indent=4)
        wfile = open('./database.json', 'w')
        wfile.write(new_json)
        wfile.close()

        text_message = "Sure! I'm checking the new event date {} with other participants. I'll let you know when it's confirmed. Hope to see you soon!".format(new_date)
        # dispatcher.utter_message(text="Sure! I'm checking with other participants. I'll let you know when it's confirmed. Hope to see you soon!")
        dispatcher.utter_message(text=text_message)

        return []
    

sleep_ls = ["insomnia", "sleep", "asleep", "sleeping", "slept"]
breath_ls = ["breath", "breathing", "breathe"]
class ActionRecordProb(Action):

    def name(self) -> Text:
        return "action_record_prob"

    def run(self, dispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        problem_text = tracker.get_slot("problem")

        # --- ! record the problem and report to backend/manager ---
        # ! try to use rase intent to sort out
        if problem_text in sleep_ls:
            problem_name = "sleep"
        elif problem_text in breath_ls:
            problem_name = "breath"
        else:
            problem_name = problem_text
        
        conversation_id = tracker.sender_id   # tracker.sender_id / "6490110454383266"
        rfile = open('./database.json', 'r')
        content = rfile.read()
        data = json.loads(content)
        rfile.close()
        for user in data["users"]:
            if user["chatID"] == conversation_id:
                user["condition"] = problem_name
                break
        new_json = json.dumps(data, indent=4)
        wfile = open('./database.json', 'w')
        wfile.write(new_json)
        wfile.close()

        text_message = "Okay, I will keep your problem with {} in mind and look for some help for you. Hope you get better soon".format(problem_name)
        # dispatcher.utter_message(text="Okay, I will keep in mind and look for some help for you. Hope you get better soon")
        dispatcher.utter_message(text=text_message)

        return []
    
class ActionEventTime(Action):

    def name(self) -> Text:
        return "action_event_time"

    def run(self, dispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        rfile = open('./database.json', 'r')
        content = rfile.read()
        data = json.loads(content)
        rfile.close()
        event_name = data["events"][next_event_ID]["content"]
        # if it is tomorrow, change the expressing
        if tomorrow_date.date() == next_event_date.date():
            event_day = "tomorrow"
        else:
            event_day = "on " + next_event_date.strftime("%Y-%m-%d")
        dispatcher.utter_message(text="The offline group {} event takes place {}.".format(event_name, event_day))

        return []