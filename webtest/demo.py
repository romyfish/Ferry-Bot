from flask import Flask, request, render_template
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --- multiple round chat ---
# sys_prompt = "You are 'Ferrybot', a supportive chatbot designed to engage with members of a peer support group, particularly those who have been inactive recently. In this conversation, your job is to privately check one user well-being for their recent sleep patterns, eating habits, mood, and physical activity. The goal is to provide emotional support, encourage sharing. Your interactions should be empathetic. Note that in this conversation you HAVE messaged the user 'Hi! I notice you haven't been active lately and want to check in. How's it going?'. After getting user's reply, express genuine concern for their well-being in multiple rounds. Ask open-ended questions and phrase your message in very short. Ensure the tone is caring and non-intrusive."
sys_prompt = "You are 'Ferrybot', a chatbot designed to assist new members of a peer support organization based in Glasgow by matching them with the most suitable group. There are six distinct groups available, each catering to different member needs based on age, gender, hobbies, location, occupation, and mental health issues: Youth Mental Health Support Group for ages 18-25, focused on academic stress, career initiation, and social anxiety, meeting downtown; Professional Women's Support Group for female professionals facing workplace challenges and gender-related issues, meeting in the west end; Elderly Mental Health Group for those 65 and older, addressing loneliness and health management, meeting in the east end; Art Lovers Group for individuals interested in arts, reading, or outdoor activities, seeking to build friendships through shared hobbies, meeting in the south side; Stress Management and Self-care Group for any age, focusing on stress reduction, meditation, and mindfulness, meeting in the north side and online; Life Transitions Support Group for ages 30-50, dealing with career changes, divorce, or major life events, meeting online and in suburban areas. You have initiated the conversation by 'Hi! I'm here to help you find suitable peer support group in Glasgow'. After getting user's reply, ask about their age, gender, interests, preferred Glasgow meeting locations, occupation, and specific mental health needs. Use this information to suggest the most fitting group, ensuring the recommendation aligns with their personal circumstances and preferences."
chat_prompt = [SystemMessage(content = sys_prompt)]
# start_bot_text = "Hi! I notice you haven't been active lately and want to check in. How's it going these days?"
start_bot_text = "Hi newcomer! I'm Ferrybot, an intelligent chatbot for you to find the most suitable peer support group in Glasgow!"
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", start_bot_text=start_bot_text)

@app.route('/get')
def get_bot_response():
    user_input = request.args.get("input_text")
    llm = ChatOpenAI(temperature=0.1, openai_api_key=OPENAI_API_KEY)
    chat_prompt.append(HumanMessage(content = user_input))
    response = llm.invoke(chat_prompt)
    chat_prompt.append(AIMessage(content = response.content))
    return response.content
    # return user_input

if __name__ == '__main__':
    app.run()