from flask import Flask, request, render_template, session

from langchain_community.llms.ollama import Ollama

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

mode_num = 1
mode_count = 4
chat_prompts = []
for i in range(mode_count):
    sp_name = "system_prompt_" + str(i+1) + ".txt"
    with open(sp_name, "r") as p_file:
        sys_prompt = p_file.read()
    chat_prompts.append([SystemMessage(content = sys_prompt)])
# chat_prompt = [SystemMessage(content = sys_prompts[mode_num-1])]

mode_descriptions = []
mode_descriptions.append("Check the user's status")
mode_descriptions.append("Advice for group selection")
mode_descriptions.append("Training to be supportive")
mode_descriptions.append("Group scenario: Schedule a meeting")
mode_descriptions.append("Group scenario: Caution on inappropriate behaviour")
mode_descriptions.append("Group → one-to-one: Check the user's status")

start_bot_texts = []
start_bot_texts.append("Hi! I notice you haven't been active lately and want to check in. How's it going these days?")
start_bot_texts.append("Hi newcomer! I'm Ferrybot, an intelligent chatbot for you to find a suitable peer support group in Glasgow!")
start_bot_texts.append("Hi! I'm Ferrybot, an intelligent chatbot for you to better cope with others in a peer support group. Ask me anything or simply prompt me to give some guidance for you!")
start_bot_texts.append("Hello everyone! We’re planning a fun offline event for our group and would love to find a time that works for everyone. Could you please share when you are generally free over the next week?")

other_user_texts = []
other_user_texts.append("I'm okay with Wednesday and Thursday")
other_user_texts.append("Oh but Thursday gonna be better for me")
other_user_texts.append("I'll be free after 2pm on Thursday")
chat_prompts[3].append(HumanMessage(content = "UserA: " + other_user_texts[0]))
chat_prompts[3].append(HumanMessage(content = "UserB: " + other_user_texts[1]))
chat_prompts[3].append(HumanMessage(content = "UserC: " + other_user_texts[2]))

app = Flask(__name__)
app.secret_key = 'a_secret_key'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/check_status')
def check_status():
    session['modeNum'] = 1
    return render_template("private.html", start_bot_text=start_bot_texts[mode_num-1], mode_num=str(mode_num), mode_description=mode_descriptions[mode_num-1])

@app.route('/ask_group_advice')
def ask_group_advice():
    session['modeNum'] = 2
    mode_num = session.get('modeNum', 1)
    return render_template("private.html", start_bot_text=start_bot_texts[mode_num-1], mode_num=str(mode_num), mode_description=mode_descriptions[mode_num-1])

@app.route('/support_train')
def support_train():
    session['modeNum'] = 3
    mode_num = session.get('modeNum', 1)
    return render_template("private.html", start_bot_text=start_bot_texts[mode_num-1], mode_num=str(mode_num), mode_description=mode_descriptions[mode_num-1])

@app.route('/schedule')
def schedule():
    session['modeNum'] = 4
    mode_num = session.get('modeNum', 1)
    return render_template("group.html", start_bot_text=start_bot_texts[mode_num-1], mode_num=str(mode_num), mode_description=mode_descriptions[mode_num-1], start_userA_text=other_user_texts[0], start_userB_text=other_user_texts[1], start_userC_text=other_user_texts[2])

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/get_chat_history')
def get_chat_history():
    chat_history = list()
    with open("chat_history.txt", "r") as h_file:
        for line in h_file:
            chat_history.append(line.strip())
    return chat_history

@app.route('/get')
def get_bot_response():
    user_input = request.args.get("input_text")
    mode_num = session.get('modeNum', 1)
    chat_prompts[mode_num-1].append(HumanMessage(content = user_input))
    llm = Ollama(model="dolphin-phi")   # llm = ChatOpenAI(temperature=0.1, openai_api_key=OPENAI_API_KEY)
    response = llm.invoke(chat_prompts[mode_num-1])
    chat_prompts[mode_num-1].append(AIMessage(content = response))
    # print(chat_prompt)
    with open("chatlog.txt","a") as l_file:
        l_file.write(str(chat_prompts[mode_num-1]))
    if response.startswith("AI: "):
        response = response[4:]
    return response
    # return user_input

@app.route('/get_in_group')
def get_bot_response_in_group():
    user_input = request.args.get("input_text")
    cur_user_input = "The active user: " + user_input
    mode_num = session.get('modeNum', 1)
    chat_prompts[mode_num-1].append(HumanMessage(content = user_input))
    llm = Ollama(model="dolphin-phi")   # llm = ChatOpenAI(temperature=0.1, openai_api_key=OPENAI_API_KEY)
    response = llm.invoke(chat_prompts[mode_num-1])
    chat_prompts[mode_num-1].append(AIMessage(content = response))
    # print(chat_prompt)
    with open("chatlog0.txt","w") as l_file:
        l_file.write(str(chat_prompts[mode_num-1]))
    if response.startswith("AI: "):
        response = response[4:]
    return response
    # response = "Roger that! I'll message the manager for the final decision."
    # return response

if __name__ == '__main__':
    app.run()