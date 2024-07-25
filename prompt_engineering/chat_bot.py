# chat_bot.py

import streamlit as st
from streamlit_chat import message
from zhipuai import ZhipuAI

from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 在代码中使用环境变量
import os
ZHIPUAI_API_KEY = os.getenv("ZHIPU_API_KEY")
 
client = ZhipuAI(api_key=ZHIPUAI_API_KEY)
 
if 'prompts' not in st.session_state:
    st.session_state['prompts'] = [{"role": "system", "content": "您是一个乐于助人的助手。尽量简洁明了地回答问题，并带有一点幽默表达。"}]
 
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
 
if 'past' not in st.session_state:
    st.session_state['past'] = []
 
 
def generate_response(prompt):
    st.session_state['prompts'].append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
        model="glm-4",
        messages=st.session_state['prompts'],
        max_tokens=1024,
        temperature=0.6
    )
    message = completion.choices[0].message.content
    return message
 
 
def end_click():
    st.session_state['prompts'] = [{"role": "system", "content": "您是一个乐于助人的助手。尽量简洁明了地回答问题，并带有一点幽默表达。"}]
    st.session_state['past'] = []
    st.session_state['generated'] = []
    st.session_state['user'] = ""
 
 
def chat_click():
    if st.session_state['user'] != '':
        chat_input = st.session_state['user']
        output = generate_response(chat_input)
        st.session_state['past'].append(chat_input)
        st.session_state['generated'].append(output)
        st.session_state['prompts'].append({"role": "assistant", "content": output})
        st.session_state['user'] = ""
 
 
st.title("我的聊天机器人")
 
user_input = st.text_input("输入:", key="user")
chat_button = st.button("发送", on_click=chat_click)
end_button = st.button("新聊天", on_click=end_click)
 
if st.session_state['generated']:
    for i in range(0, len(st.session_state['generated']), 1):
        message(st.session_state['past'][i], is_user=True)
        message(st.session_state['generated'][i], key=str(i))