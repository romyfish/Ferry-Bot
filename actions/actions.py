# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import ReminderScheduled, ReminderCancelled, UserUtteranceReverted, ConversationPaused 

import json
import datetime
import re
import requests

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
    if datetime.datetime.now() < event_date and event["status"] != "canceled":
        # when find the event take place tomorrow or later
        next_event_ID = event["id"]
        next_event_date = event_date
        break
mng_psid = data["manager"]["chatID"]

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
        
        conversation_id = tracker.sender_id   # tracker.sender_id / "6490110454383266"

        # query from database for the event day and set the notifying datetime before
        # send_date = next_event_date - datetime.timedelta(days=1)
        # date = datetime.datetime.combine(send_date, send_time)
        # if conversation_id == mng_psid: date += datetime.timedelta(hours=1)
        date = datetime.datetime.now() + datetime.timedelta(seconds=15)
        str_date = datetime.datetime.strftime(date,'%Y-%m-%d %H:%M:%S')

        if conversation_id != mng_psid:
            dispatcher.utter_message("Confirmed. I will check with you at {}".format(str_date))
            # dispatcher.utter_message("Confirmed. I will check with you the day before the event every week.")

            reminder = ReminderScheduled(
                "EXTERNAL_notify",
                trigger_date_time=date,
                name="event_notify",
                kill_on_user_message=False,
            )
        else:
            dispatcher.utter_message("Confirmed. I will inform you the results from everyone at {}".format(str_date))

            reminder = ReminderScheduled(
                "EXTERNAL_inform",
                trigger_date_time=date,
                name="event_inform",
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

        # --- record the individual available ---
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

        # --- ! record the new time and ask to other users ---
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

        # trigger a reminder to ask other users
        date = datetime.datetime.now() + datetime.timedelta(seconds=5)
        reminder = ReminderScheduled(
            "EXTERNAL_time_change",
            trigger_date_time=date,
            name="event_time_change",
            kill_on_user_message=False,
        )

        return [reminder]

class ActionRecordProb(Action):

    def name(self) -> Text:
        return "action_record_prob"

    def run(self, dispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        problem = tracker.get_slot("problem")

        # --- ! record the problem and report to backend/manager ---
        conversation_id = tracker.sender_id   # tracker.sender_id / "6490110454383266"
        rfile = open('./database.json', 'r')
        content = rfile.read()
        data = json.loads(content)
        rfile.close()
        for user in data["users"]:
            if user["chatID"] == conversation_id:
                user["condition"] = problem
                break
        new_json = json.dumps(data, indent=4)
        wfile = open('./database.json', 'w')
        wfile.write(new_json)
        wfile.close()

        text_message = "Okay, I will keep your problem with {} in mind and look for some help for you. Hope you get better soon".format(problem)
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

class ActionGetChangeAgree(Action):

    def name(self) -> Text:
        return "action_get_change_agree"

    def run(self, dispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # --- ! record the user approve the time change ---
        conversation_id = tracker.sender_id   # tracker.sender_id / "6490110454383266"
        rfile = open('./database.json', 'r')
        content = rfile.read()
        data = json.loads(content)
        rfile.close()
        for user in data["users"]:
            if user["chatID"] == conversation_id:
                userID = user["id"]
                break
        data["events"][next_event_ID]["participants"][userID] = "approve_change"
        new_json = json.dumps(data, indent=4)
        wfile = open('./database.json', 'w')
        wfile.write(new_json)
        wfile.close()

        dispatcher.utter_message(text="Sure! I'll put it on the record.")

        return []
    
class ActionInformResult(Action):

    def name(self) -> Text:
        return "action_inform_result"

    def run(self, dispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # --- only tell the manager about results ---
        conversation_id = tracker.sender_id   # tracker.sender_id / "6490110454383266"
        if conversation_id == mng_psid:
            rfile = open('./database.json', 'r')
            content = rfile.read()
            data = json.loads(content)
            rfile.close()
            participants = data["events"][next_event_ID]["participants"]   # !! express with sentence or table
            refuse = []
            users_change = []
            change_time = []
            approve_change = []
            affirm_count = 0
            for p in participants:
                if participants[p] == "refuse":
                    refuse.append(p)
                elif re.findall("\d+", participants[p]) != []:
                    users_change.append(p)
                    change_time.append(participants[p])
                elif participants[p] == "approve_change":
                    approve_change.append(p)
                else:
                    affirm_count += 1
            results = ""
            if refuse != []:
                str_refuse = ""
                if len(refuse) >= 2:
                    for i in range(len(refuse)-1):
                        str_refuse += refuse[i] + ", "
                    str_refuse = str_refuse[:-2] + " and " + refuse[len(refuse)-1]
                else:
                    str_refuse += refuse[0]
                results += str_refuse + " refused to attend. "
            if users_change != []:
                str_change = ""
                for i in range(len(users_change)):
                    str_change += users_change[i] + " suggested to reschedule the event on " + change_time[i] + ". "
                results += str_change
            if approve_change != []:
                str_approve_change = ""
                if len(approve_change) >= 2:
                    for i in range(len(approve_change)-1):
                        str_approve_change += approve_change[i] + ", "
                    str_approve_change = str_approve_change[:-2] + " and " + approve_change[len(approve_change)-1]
                else:
                    str_approve_change += approve_change[0]
                results += str_approve_change + " approved to reschedule the event. "
            else:
                results += "no other one approved to reschedule the event."
            if results == "":
                results += "everyone affirmed to attend the event!"
            elif affirm_count > 0:
                results += "And the others affirmed to attend the event!"
            dispatcher.utter_message(text=results)
        else:
            dispatcher.utter_message(text="I'm afraid not sure for now")
        return []

class ActionRescheduleEvent(Action):
    """Manager reschedule next event"""

    def name(self) -> Text:
        return "action_reschedule_event"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        conversation_id = tracker.sender_id   # tracker.sender_id / "6490110454383266"
        if conversation_id != mng_psid:
            dispatcher.utter_message(text="Sorry, only the manager can reschedule the event.")
            return [UserUtteranceReverted()]
        dispatcher.utter_message(text="Sure, I'll record it in database and inform everyone.")
        rfile = open('./database.json', 'r')
        content = rfile.read()
        data = json.loads(content)
        rfile.close()
        participants = data["events"][next_event_ID]["participants"]
        for p in participants:
            if re.findall("\d+", participants[p]) != []:
                new_event_date = participants[p]
        data["events"][next_event_ID]["date"] = new_event_date
        new_json = json.dumps(data, indent=4)
        wfile = open('./database.json', 'w')
        wfile.write(new_json)
        wfile.close()
        # trigger a reminder to inform everyone the event rescheduled
        date = datetime.datetime.now() + datetime.timedelta(seconds=5)
        reminder = ReminderScheduled(
            "EXTERNAL_inform_reschedule",
            trigger_date_time=date,
            name="event_inform_reschedule",
            kill_on_user_message=False,
        )

        return [reminder]

class ActionCancelEvent(Action):
    """Manager cancel next event"""

    def name(self) -> Text:
        return "action_cancel_event"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        conversation_id = tracker.sender_id   # tracker.sender_id / "6490110454383266"
        if conversation_id != mng_psid:
            dispatcher.utter_message(text="Sorry, only the manager can cancel the event.")
            return [UserUtteranceReverted()]
        dispatcher.utter_message(text="Okay, I'll record it in database and inform everyone.")
        rfile = open('./database.json', 'r')
        content = rfile.read()
        data = json.loads(content)
        rfile.close()
        data["events"][next_event_ID]["status"] = "canceled"
        new_json = json.dumps(data, indent=4)
        wfile = open('./database.json', 'w')
        wfile.write(new_json)
        wfile.close()
        # trigger a reminder to inform everyone the event canceled
        date = datetime.datetime.now() + datetime.timedelta(seconds=5)
        reminder = ReminderScheduled(
            "EXTERNAL_inform_cancel",
            trigger_date_time=date,
            name="event_inform_cancel",
            kill_on_user_message=False,
        )

        return [reminder]
    
access_token = "EABcR4tIrngQBAEeVwoWPsJz2TRcc3ZAwdvXXdJas1b1Xk4zvl1oAxvAVTJUrOzTgzAzgcnWfVA2G0f1PRNU0IzjBtjXJOFX5GQ07kSZBOmbkOfr6FFhvpaXiEck3HJfIemJplWznAFv0X95hSUeIaHLZB1M2IxtmVvDiBuyOx7jPSX1e4cs"
def send_FBmessage(user_psid, message_text):
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'messaging_type': 'UPDATE',
        'recipient': {
            'id': user_psid
        },
        'message': {
            'text': message_text
        }
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()

class ActionTimeChangeChecking(Action):
    """Check the new event time with other user"""

    def name(self) -> Text:
        return "action_time_change_checking"

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
        participants = data["events"][next_event_ID]["participants"]
        for p in participants:
            if re.findall("\d+", participants[p]) != []:
                change_user_ID = p
                new_event_date = participants[p]
        message_text="Sorry, someone has asked for rescheduling tomorrow's offline group {} for {}. Are you okay with that?".format(event_name, new_event_date)
        for p in participants:
            if p != change_user_ID and participants[p] != "refuse":
                for user in data["users"]:
                    if user["id"] == p:
                        user_psid = user["chatID"]
                        break
                send_FBmessage(user_psid, message_text)

        return []

class ActionInformReschedule(Action):
    """inform every user the event rescheduled"""

    def name(self) -> Text:
        return "action_inform_reschedule"

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
        new_event_date = data["events"][next_event_ID]["date"]
        participants = data["events"][next_event_ID]["participants"]
        message_text="Hi, tomorrow's offline group {} is rescheduled to {}. Hope to see you!".format(event_name, new_event_date)
        for p in participants:
            for user in data["users"]:
                if user["id"] == p:
                    user_psid = user["chatID"]
                    break
            send_FBmessage(user_psid, message_text)

        return []
    
class ActionInformCancel(Action):
    """inform every user the event canceled"""

    def name(self) -> Text:
        return "action_inform_cancel"

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
        participants = data["events"][next_event_ID]["participants"]
        status = data["events"][next_event_ID]["status"]
        message_text="Hi, tomorrow's offline group {} is {}. Hope to see you next week!".format(event_name, status)
        for p in participants:
            for user in data["users"]:
                if user["id"] == p:
                    user_psid = user["chatID"]
                    break
            send_FBmessage(user_psid, message_text)

        return []
    
class ActionDefaultFallback(Action):
    """ultimate fallback action to handoff to a human manager"""

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Sorry, I can't help you. I am passing you to the manager...")
        
        # message to manager with the situation asking for handoff
        conversation_id = tracker.sender_id   # tracker.sender_id / "6490110454383266"
        rfile = open('./database.json', 'r')
        content = rfile.read()
        data = json.loads(content)
        rfile.close()
        for user in data["users"]:
            if user["chatID"] == conversation_id:
                user_name = user["name"]
                break
        message_text="Hi manager, I can't handle {}'s request. Please log in to response...".format(user_name)
        send_FBmessage(mng_psid, message_text)

        return [ConversationPaused(), UserUtteranceReverted()]
    