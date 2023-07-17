# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionAskAttend(Action):

    def name(self) -> Text:
        return "action_ask_attend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Are you free to attend the offline group event tomorrow?")

        return []

class ActionGetAffirm(Action):

    def name(self) -> Text:
        return "action_get_affirm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # --- ! record the individual available and report to backend/manager ---

        dispatcher.utter_message(text="Lovely! See you then!")

        return []
    
class ActionRecordProb(Action):

    def name(self) -> Text:
        return "action_record_prob"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        problem_name = tracker.get_slot("problem")

        # --- ! record the problem and report to backend/manager ---

        text_message = "Okay, I will keep your problem with {} in mind and look for some help for you. Hope you get better soon".format(problem_name)
        
        # dispatcher.utter_message(text="Okay, I will keep in mind and look for some help for you. Hope you get better soon")
        dispatcher.utter_message(text=text_message)

        return []
    
class ActionRecordUnwill(Action):

    def name(self) -> Text:
        return "action_record_unwilling"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # --- ! record the individual unavailable and report to backend/manager ---

        dispatcher.utter_message(text="Okay, no worries. Hope to see you soon!")

        return []
    
class ActionRecordTime(Action):

    def name(self) -> Text:
        return "action_record_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        day = tracker.get_slot("day")

        # --- ! record the new time and report to backend/manager ---

        text_message = "Sure! I'm checking the {} with other participants. I'll let you know when it's confirmed. Hope to see you soon!".format(day)

        # dispatcher.utter_message(text="Sure! I'm checking with other participants. I'll let you know when it's confirmed. Hope to see you soon!")
        dispatcher.utter_message(text=text_message)

        return []