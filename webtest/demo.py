from flask import Flask, request, render_template

from langchain_community.llms.ollama import Ollama

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

mode_num = 2
sp_name = "system_prompt_" + str(mode_num) + ".txt"
# --- multiple round chat ---
with open(sp_name, "r") as p_file:
    sys_prompt = p_file.read()
chat_prompt = [SystemMessage(content = sys_prompt)]

start_bot_texts = []
start_bot_texts.append("Hi! I notice you haven't been active lately and want to check in. How's it going these days?")
start_bot_texts.append("Hi newcomer! I'm Ferrybot, an intelligent chatbot for you to find a suitable peer support group in Glasgow!")
start_bot_texts.append("Hi! I'm Ferrybot, an intelligent chatbot for you to better cope with others in a peer support group. Ask me anything or simply prompt me to give some guidance for you!")
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", start_bot_text=start_bot_texts[mode_num-1])

@app.route('/get')
def get_bot_response():
    user_input = request.args.get("input_text")
    llm = Ollama(model="dolphin-phi")   # llm = ChatOpenAI(temperature=0.1, openai_api_key=OPENAI_API_KEY)
    chat_prompt.append(HumanMessage(content = user_input))
    response = llm.invoke(chat_prompt)
    chat_prompt.append(AIMessage(content = response))
    # print(chat_prompt)
    with open("chatlog.txt","a") as l_file:
        l_file.write(str(chat_prompt))
    if response.startswith("AI: "):
        response = response[4:]
    return response
    # return user_input

if __name__ == '__main__':
    app.run()