import json
import datetime

# sample = {
#     "events": "hiking",
#     "users": ["id","name"],
#     "groups": {
#         "id": "123",
#         "book": "python study"
#     }
# }
# sample_json = json.dumps(sample)
# wfile = open('database.json', 'w')
# wfile.write(sample_json)
# wfile.close()

# print(sample_json)

# rfile = open('./database.json', 'r')
# content = rfile.read()
# data = json.loads(content)
# rfile.close()
# data["users"][1]["groupID"] = "1"
# new_json = json.dumps(data, indent=4)
# wfile = open('./database.json', 'w')
# wfile.write(new_json)
# wfile.close()
# print(data["users"][1])

# conversation_id = "6110406512402871"
# rfile = open('./database.json', 'r')
# content = rfile.read()
# data = json.loads(content)
# rfile.close()
# for user in data["users"]:
#     if user["chatID"] == conversation_id:
#         userID = user["id"]
#         break
# data["events"][1]["participants"][userID] = "affirm"
# new_json = json.dumps(data, indent=4)
# wfile = open('./database.json', 'w')
# wfile.write(new_json)
# wfile.close()
# print(data["events"][1])

today_date = datetime.datetime.now().strftime("%Y-%m-%d")
print(today_date)
tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=1)
print(tomorrow_date.strftime("%Y-%m-%d"))

# conversation_id = "6110406512402871"
# rfile = open('./database.json', 'r')
# content = rfile.read()
# data = json.loads(content)
# rfile.close()
# for user in data["users"]:
#     if user["chatID"] == conversation_id:
#         userID = user["id"]
#         break
# data["events"][1]["participants"][userID] = tomorrow_date.strftime("%Y-%m-%d")
# new_json = json.dumps(data, indent=4)
# wfile = open('./database.json', 'w')
# wfile.write(new_json)
# wfile.close()
# print(data["events"][1])

# str_day = today_date[-2:]
# int_day = int(str_day)
# print(int_day)
# new_date = tomorrow_date.strftime("%Y-") + str(tomorrow_date.month+1).zfill(2) + "-" + str(int_day).zfill(2)
# print(new_date)
import re
# test = "2023-7-19"
# a = []
# a = re.findall("\d+", test)
# print(a)

week_ls = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# print(week_ls[datetime.date(2023, 7, 12).weekday()])

# if "Wednesday" in week_ls:
#     print("in")
# else:
#     print("not in")
# ddays = week_ls.index("Saturday") - tomorrow_date.weekday()
# new_date = (tomorrow_date + datetime.timedelta(days=ddays)).strftime("%Y-%m-%d")
# print(new_date)

# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# next_event_date = datetime.datetime.strptime('2023-07-19','%Y-%m-%d')
# print(next_event_date)
# # date = datetime.datetime(next_event_date - datetime.timedelta(days=1), 23, 20, 10)
# date = next_event_date - datetime.timedelta(days=1)
# print(date)
# send_time = datetime.time(10, 30)
# print(send_time)
# print(datetime.datetime.combine(date,send_time))

# import requests
# access_token = "EABcR4tIrngQBAEeVwoWPsJz2TRcc3ZAwdvXXdJas1b1Xk4zvl1oAxvAVTJUrOzTgzAzgcnWfVA2G0f1PRNU0IzjBtjXJOFX5GQ07kSZBOmbkOfr6FFhvpaXiEck3HJfIemJplWznAFv0X95hSUeIaHLZB1M2IxtmVvDiBuyOx7jPSX1e4cs"
# def send_facebook_message(user_psid, message_text):
#     url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token

#     headers = {
#         'Content-Type': 'application/json'
#     }

#     data = {
#         'messaging_type': 'UPDATE',
#         'recipient': {
#             'id': user_psid
#         },
#         'message': {
#             'text': message_text
#         }
#     }

#     response = requests.post(url, headers=headers, json=data)

#     return response.json()

# user_psid = "6110406512402871"
# message_text = "Message test update"
# send_facebook_message(user_psid, message_text)

# rfile = open('./database.json', 'r')
# content = rfile.read()
# data = json.loads(content)
# rfile.close()
# participants = data["events"][1]["participants"]
# for rp in participants:
#     print(rp)
#     if re.findall("\d+", participants[rp]) != []:
#         change_user_ID = rp
#         new_event_date = participants[rp]
#         print(change_user_ID, new_event_date)

rfile = open('./database.json', 'r')
content = rfile.read()
data = json.loads(content)
rfile.close()
potential_dates = data["events"][1]["potential_date"]
print(list(potential_dates.keys()))
potential_dates[list(potential_dates.keys())[0]] += 1
print(potential_dates)
# potential_dates = sorted(potential_dates.items())
# print(potential_dates[0][0])
# print(potential_dates[0][1])
# print(potential_dates.get("2023-08-14") == None)
# data["events"][1]["potential_date"] = potential_dates
# new_json = json.dumps(data, indent=4)
# wfile = open('./database.json', 'w')
# wfile.write(new_json)
# wfile.close()

# def identify_date(day_text):
#     digit_date = []
#     digit_date = re.findall("\d+", day_text)
#     if digit_date != []:   # if user give the specific date
#         new_day = int(digit_date[0])
#         if new_day > tomorrow_date.day:   # compare the month
#             # new_date = tomorrow_date.strftime("%Y-%m-") + str(new_day).zfill(2)
#             new_date = datetime.date(tomorrow_date.year, tomorrow_date.month, new_day)
#         else:
#             # new_date = tomorrow_date.strftime("%Y-") + str(tomorrow_date.month+1).zfill(2) + "-" + str(new_day).zfill(2)
#             new_date = datetime.date(tomorrow_date.year, tomorrow_date.month+1, new_day)
#     elif day_text == "tommorow":
#         new_date = tomorrow_date
#     elif day_text == "day after tomorrow":
#         new_date = (datetime.datetime.now() + datetime.timedelta(days=2))
#     elif day_text in week_ls:   # if user give the weekday
#         # match the weekday with the date (assume in this week)
#         ddays = week_ls.index(day_text) - tomorrow_date.weekday()
#         new_date = (tomorrow_date + datetime.timedelta(days=ddays))
#     else:
#         # deal with other situation
#         new_date = tomorrow_date
#     return new_date

# new_date = identify_date("12th")
# print(new_date.weekday())
# weekdayIdx = new_date.weekday()
# dates = []
# for i in range(weekdayIdx, 6):
#     new_date += datetime.timedelta(days=1)
#     dates.append(new_date.strftime("%Y-%m-%d"))
# print(dates)

# def summary_info(data):
#     participants = data["events"][0]["participants"]
#     unknown = []
#     refuse = []
#     users_change = []
#     change_time = []
#     approve_change = []
#     affirm_count = 0
#     for p in participants:
#         if participants[p] == "unknown":
#             unknown.append(p)
#         elif participants[p] == "refuse":
#             refuse.append(p)
#         elif re.findall("\d+", participants[p]) != []:
#             users_change.append(p)
#             change_time.append(participants[p])
#         elif participants[p] == "approve_change":
#             approve_change.append(p)
#         else:
#             affirm_count += 1
#     results = ""
#     if unknown != []:
#         str_unknown = ""
#         if len(unknown) >= 2:
#             for i in range(len(unknown)-1):
#                 str_unknown += unknown[i] + ", "
#             str_unknown = str_unknown[:-2] + " and " + unknown[-1]
#         else:
#             str_unknown += unknown[0]
#         results += str_unknown + " didn't reply. "
#     if refuse != []:
#         str_refuse = ""
#         if len(refuse) >= 2:
#             for i in range(len(refuse)-1):
#                 str_refuse += refuse[i] + ", "
#             str_refuse = str_refuse[:-2] + " and " + refuse[-1]
#         else:
#             str_refuse += refuse[0]
#         results += str_refuse + " refused to attend. "
#     if users_change != []:
#         str_change = ""
#         for i in range(len(users_change)):
#             str_change += users_change[i] + " suggested to reschedule the event on " + change_time[i] + ". "
#         results += str_change
#     if approve_change != []:
#         str_approve_change = ""
#         if len(approve_change) >= 2:
#             for i in range(len(approve_change)-1):
#                 str_approve_change += approve_change[i] + ", "
#             str_approve_change = str_approve_change[:-2] + " and " + approve_change[-1]
#         else:
#             str_approve_change += approve_change[0]
#         results += str_approve_change + " approved to reschedule the event. "
#     if results == "":
#         results += "everyone affirmed to attend the event!"
#     elif affirm_count > 0:
#         results += "And the others affirmed to attend the event!"
#     return results

# rfile = open('./database.json', 'r')
# content = rfile.read()
# data = json.loads(content)
# rfile.close()
# message = summary_info(data)
# print(type(message))
# print(message)
