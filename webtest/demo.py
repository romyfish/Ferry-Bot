from flask import Flask, request, render_template, session

# from langchain_community.llms.ollama import Ollama

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from langchain_openai import ChatOpenAI

import os
api_key = os.getenv('OPENAI_API_KEY')
# print("API Key:", api_key)

import re
import csv
from datetime import datetime

mode_num = 1
mode_count = 6
chat_prompts = []
for i in range(mode_count):
    sp_name = "texts/system_prompt_" + str(i+1) + ".txt"
    with open(sp_name, "r") as p_file:
        sys_prompt = p_file.read()
    chat_prompts.append([SystemMessage(content = sys_prompt)])
# chat_prompt = [SystemMessage(content = sys_prompts[mode_num-1])]

mode_descriptions = []
mode_descriptions.append("Check in with Inactive Users on Their Wellbeing")
mode_descriptions.append("Match Newcomers with Suitable Peer Support Groups")
mode_descriptions.append("Coordinate Group Availability and Preferences for Upcoming Events")
mode_descriptions.append("Train Peer Supporters on Active Member Engagement")
mode_descriptions.append("Train Peer Supporters on Empathic Care by Simulation Exercise")
mode_descriptions.append("Train Peer Supporters on Conflict Management in Group Chats")

mode_profiles = []
mode_profiles.append("Ferrybot is an intelligent agent within a peer support group, taking care of all the members. Its role is to provide emotional support and encourage members to engage with the peer support group. As a CARE INTERMEDIARY, it initiates conversations with inactive members to inquire about their mental and physical well-being.")
mode_profiles.append("Ferrybot is an intelligent agent within a peer support organization. It serves as an ASSISTANT to help newcomers find the most appropriate group in this big organization which involves a variety of affiliated groups.")
mode_profiles.append("This Group-chat consists of all members of a peer support group and Ferrybot, an intelligent agent for the group. Normally the group chat is the communication channel for the members. Here, Ferrybot, as an assistant, facilitates discussions within the group to determine the best time and type of activity that suits the majority.")
mode_profiles.append("Ferrybot is an intelligent agent within a peer support group. It serves as a MENTOR for peer supporters to teach them the necessary skills and strategies to effectively engage with other group members, focusing on how to sensitively inquire about members' feelings, health, and personal interests, and how to encourage participation in group activities.")
mode_profiles.append("Ferrybot is an intelligent agent within a peer support group. It serves as a TRAINER for peer supporters, instructing them to care someone upset by simulation exercises. It will pretend to be a very frustrated people and needs comfort from the supporter.")
mode_profiles.append("This Group-chat consists of all members of a peer support group and Ferrybot, an intelligent agent for the group. Normally Ferrybot acts as a mediator to manage conflicts among group members in this group. Here, Ferrybot, as a trainer, guides supporters on effectively managing and promoting positive interactions by specific crisis simulations.")

mode_hints = []
mode_hints.append("In this scenario, you will play the role of a member of a peer support group who hasn't interacted with Ferrybot or participated in the group chat recently. You might hesitate to discuss your issues with real people, but could feel more comfortable opening up if a chatbot initiates contact.")
mode_hints.append("In this scenario, you will play the role of a new member of a peer support organization in Glasgow, which has a variety of affiliated groups. Your goal is to find the group that best matches your personal characteristics, such as demographics and interests.")
mode_hints.append("In this scenario, you will play the role of Lisa, a member of a peer support group that regularly organizes weekly activities such as coffee chats, hiking, sports, picnics, crafting, and gardening. Feel free to discuss your availability and preferred activities for the upcoming week, providing information that will help Ferrybot suggest suitable options for the group.")
mode_hints.append("In this scenario, you will play the role of a supporter within a peer support group. Through interactions with Ferrybot, you'll receive guidance to enhance your ability to offer valuable support and cultivate a welcoming community atmosphere.")
mode_hints.append("In this scenario, you will play the role of a supporter in a peer support group and might be unsure about how to effectively assist others. Ferrybot will help you practice providing care by simulating a situation where it acts as someone who is extremely upset and needs comforting. After the simulation, Ferrybot will review your performance and offer feedback to help improve your support skills.")
mode_hints.append("In this scenario, you will play the role of Joe, a member in a peer support group where someone suddenly made aggressive remarks and heightened tensions. Try to intervene in the group conversation to help de-escalate any rising tensions and restore positive dialogue flow, similar to how Ferrybot demonstrated in sample messages. Once the situation de-escalated, Ferrybot will provide feedback on your intervention techniques or offer guidance as needed to enhance your skills in maintaining a supportive and harmonious group environment.")

start_bot_texts = []
start_bot_texts.append("Hi! I notice you haven't been active lately and want to check in. How's it going these days?")
start_bot_texts.append("Hi newcomer! I'm Ferrybot, an intelligent chatbot for you to find a suitable peer support group in Glasgow!")
start_bot_texts.append("Hello everyone! We're planning a fun offline event for our group and would love to find a time that works for everyone. Could you please share when you are generally free over the next week?")
start_bot_texts.append("Hi! I'm Ferrybot, an intelligent chatbot for you to better cope with others in a peer support group. Ask me anything or simply prompt me to give some guidance for you!")
start_bot_texts.append("Hello! Today, we're going to practice a very important skill — comforting someone who is feeling extremely upset. It's crucial for a peer supporter to offer empathy, listen actively, and respond thoughtfully. I'll simulate a scenario where I am a support seeker going through a tough time. Your task is to respond in a way that shows care and support. Are you ready to start?")

app = Flask(__name__)
app.secret_key = 'a_secret_key'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/check_status')
def check_status():
    session['modeNum'] = 1
    return render_template("private.html", mode_profile=mode_profiles[mode_num-1], start_bot_text=start_bot_texts[mode_num-1], mode_num=str(mode_num), mode_description=mode_descriptions[mode_num-1], hint_text=mode_hints[mode_num-1], next_text=mode_descriptions[mode_num], next_url='ask_group_advice')

@app.route('/ask_group_advice')
def ask_group_advice():
    session['modeNum'] = 2
    mode_num = session.get('modeNum', 1)
    return render_template("private.html", mode_profile=mode_profiles[mode_num-1], start_bot_text=start_bot_texts[mode_num-1], mode_num=str(mode_num), mode_description=mode_descriptions[mode_num-1], hint_text=mode_hints[mode_num-1], next_text=mode_descriptions[mode_num], next_url='schedule')

@app.route('/schedule')
def schedule():
    session['modeNum'] = 3
    mode_num = session.get('modeNum', 1)
    return render_template("group.html", mode_profile=mode_profiles[mode_num-1], mode_num=str(mode_num), mode_description=mode_descriptions[mode_num-1], hint_text=mode_hints[mode_num-1], next_text=mode_descriptions[mode_num], next_url='support_train')

@app.route('/support_train')
def support_train():
    session['modeNum'] = 4
    mode_num = session.get('modeNum', 1)
    return render_template("private.html", mode_profile=mode_profiles[mode_num-1], start_bot_text=start_bot_texts[mode_num-1], mode_num=str(mode_num), mode_description=mode_descriptions[mode_num-1], hint_text=mode_hints[mode_num-1], next_text=mode_descriptions[mode_num], next_url='simulate_train')

@app.route('/simulate_train')
def simulate_train():
    session['modeNum'] = 5
    mode_num = session.get('modeNum', 1)
    return render_template("private_simul.html", mode_profile=mode_profiles[mode_num-1], start_bot_text=start_bot_texts[mode_num-1], mode_num=str(mode_num), mode_description=mode_descriptions[mode_num-1], hint_text=mode_hints[mode_num-1], next_text=mode_descriptions[mode_num], next_url='train_in_group')

@app.route('/train_in_group')
def train_in_group():
    session['modeNum'] = 6
    mode_num = session.get('modeNum', 1)
    return render_template("group_chat.html", mode_profile=mode_profiles[mode_num-1], mode_num=str(mode_num), mode_description=mode_descriptions[mode_num-1], hint_text=mode_hints[mode_num-1])

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/get_chat_history')
def get_chat_history():
    mode_num = session.get('modeNum', 1)
    ch_name = "texts/chat_history_" + str(mode_num) + ".txt"
    chat_history = list()
    with open(ch_name, "r") as h_file:
        for line in h_file:
            chat_history.append(line.strip())
    # reset the prompt
    sp_name = "texts/system_prompt_" + str(mode_num) + ".txt"
    with open(sp_name, "r") as p_file:
        sys_prompt = p_file.read()
    chat_prompts[mode_num-1] = [SystemMessage(content = sys_prompt)]
    return chat_history

@app.route('/initial_group_chat')
def initial_group_chat():
    mode_num = session.get('modeNum', 1)
    sp_name = "texts/system_prompt_3.txt"   # reset the prompt
    with open(sp_name, "r") as p_file:
        sys_prompt = p_file.read()
    chat_prompts[mode_num-1] = [SystemMessage(content = sys_prompt)]
    # print(chat_prompts[mode_num-1])
    llm = ChatOpenAI(temperature=0.1, openai_api_key=api_key)
    response = llm.invoke(chat_prompts[mode_num-1])
    raw_text = response.content
    chat_prompts[mode_num-1].append(AIMessage(content = raw_text))
    # print(chat_prompts[mode_num-1])
    text_parts = re.split(r"Ferrybot:|Bruce:|Carly:", re.sub(r'\([^)]*\)', '', raw_text))
    responses = list()
    for statement in text_parts[1:]:
        clean_statement = statement.strip().strip("'")
        responses.append(clean_statement)
    return responses

@app.route('/set_group_chat')
def set_group_chat():
    mode_num = session.get('modeNum', 1)
    sp_name = "texts/system_prompt_6.txt"   # reset the prompt
    with open(sp_name, "r") as p_file:
        sys_prompt = p_file.read()
    chat_prompts[mode_num-1] = [SystemMessage(content = sys_prompt)]
    # print(chat_prompts[mode_num-1])
    llm = ChatOpenAI(temperature=0.1, openai_api_key=api_key, model="gpt-4-turbo")
    response = llm.invoke(chat_prompts[mode_num-1])
    raw_text = response.content
    chat_prompts[mode_num-1].append(AIMessage(content = raw_text))
    print(chat_prompts[mode_num-1])
    if raw_text[0] == '*':
        text_parts = re.split(r"\**Carly\**:|\**Dan\**:", re.sub(r'\([^)]*\)', '', raw_text))
    else:
        text_parts = re.split(r"Carly:|Dan:", re.sub(r'\([^)]*\)', '', raw_text))
    responses = list()
    for statement in text_parts[1:]:
        clean_statement = statement.strip("*").strip().strip("'")
        responses.append(clean_statement)
    return responses

@app.route('/get')
def get_bot_response():
    user_input = request.args.get("input_text")
    mode_num = session.get('modeNum', 1)
    chat_prompts[mode_num-1].append(HumanMessage(content = user_input))
    # llm = Ollama(model="dolphin-phi")
    llm = ChatOpenAI(temperature=0.1, openai_api_key=api_key)
    response = llm.invoke(chat_prompts[mode_num-1])
    chat_prompts[mode_num-1].append(AIMessage(content = response.content))
    # print(chat_prompts[mode_num-1])
    now = datetime.now()
    cl_name = "data/chatlog_" + str(now.strftime("%Y%m%d%H%M")) + ".txt"
    with open(cl_name,"w") as l_file:
        l_file.write(str(chat_prompts[mode_num-1]))
    # if response.startswith("AI: "):
    #     response = response[4:]
    return response.content
    # return user_input

@app.route('/get_in_group')
def get_bot_response_in_group():
    user_input = request.args.get("input_text")
    # cur_user_input = "UserA: " + user_input
    mode_num = session.get('modeNum', 1)
    chat_prompts[mode_num-1].append(HumanMessage(content = user_input))
    # llm = Ollama(model="dolphin-phi")
    llm = ChatOpenAI(temperature=0.1, openai_api_key=api_key)
    response = llm.invoke(chat_prompts[mode_num-1])
    raw_text = response.content
    chat_prompts[mode_num-1].append(AIMessage(content = raw_text))
    # print(chat_prompts[mode_num-1])
    # print(chat_prompt)
    now = datetime.now()
    cl_name = "data/chatlog_" + str(now.strftime("%Y%m%d%H%M")) + ".txt"
    with open(cl_name,"w") as l_file:
        l_file.write(str(chat_prompts[mode_num-1]))
    text_parts = re.split(r"Ferrybot:|Bruce:|Carly:", re.sub(r'\([^)]*\)', '', raw_text))
    responses = list()
    for statement in text_parts[1:]:
        clean_statement = statement.strip().strip("'")
        responses.append(clean_statement)
    return responses

@app.route('/get_in_group_chat')
def get_bot_response_in_group_chat():
    user_input = request.args.get("input_text")
    # cur_user_input = "UserA: " + user_input
    mode_num = session.get('modeNum', 1)
    chat_prompts[mode_num-1].append(HumanMessage(content = user_input))
    llm = ChatOpenAI(temperature=0.1, openai_api_key=api_key, model="gpt-4-turbo")
    response = llm.invoke(chat_prompts[mode_num-1])
    raw_text = response.content
    chat_prompts[mode_num-1].append(AIMessage(content = raw_text))
    # print(chat_prompt)
    now = datetime.now()
    cl_name = "data/chatlog_" + str(now.strftime("%Y%m%d%H%M")) + ".txt"
    with open(cl_name,"w") as l_file:
        l_file.write(str(chat_prompts[mode_num-1]))
    if raw_text[0] == '*':
        text_parts = re.split(r"\**Bruce\**:|\**Carly\**:|\**Dan\**:|\**Ferrybot\**:", re.sub(r'\([^)]*\)', '', raw_text))
    else:
        text_parts = re.split(r"Bruce:|Carly:|Dan:|Ferrybot:", re.sub(r'\([^)]*\)', '', raw_text))
    responses = list()
    for statement in text_parts[1:]:
        clean_statement = statement.strip("*").strip().strip("'")
        responses.append(clean_statement)
    return responses
    # return raw_text

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        title = request.form.get('titleInput')
        name = request.form.get('nameInput')
        email = request.form.get('emailInput')
        type = request.form.get('typeInput')
        comment = request.form.get('commentInput')
        now = datetime.now()
        submit_time = now.strftime("%Y-%m-%d %H:%M:%S")

        with open('data/submissions.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            # Add head for the first writing
            if file.tell() == 0:
                writer.writerow(['Submit Time', 'Title', 'Name', 'Email', 'Type note', 'Comments'])
            writer.writerow([submit_time, title, name, email, type, comment])
    
    return render_template('contact.html', success_flag=1)

if __name__ == '__main__':
    app.run()