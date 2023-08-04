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

# today_date = datetime.datetime.now().strftime("%Y-%m-%d")
# print(today_date)
# tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=1)
# print(tomorrow_date.strftime("%Y-%m-%d"))

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

# week_ls = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

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

import requests
access_token = "EABcR4tIrngQBAEeVwoWPsJz2TRcc3ZAwdvXXdJas1b1Xk4zvl1oAxvAVTJUrOzTgzAzgcnWfVA2G0f1PRNU0IzjBtjXJOFX5GQ07kSZBOmbkOfr6FFhvpaXiEck3HJfIemJplWznAFv0X95hSUeIaHLZB1M2IxtmVvDiBuyOx7jPSX1e4cs"
def send_facebook_message(user_psid, message_text):
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

user_psid = "6110406512402871"
message_text = "Message test update"
send_facebook_message(user_psid, message_text)

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