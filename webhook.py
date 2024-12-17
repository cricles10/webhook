#!/usr/bin/env python
# coding: utf-8

# In[2]:


from fastapi import FastAPI, Request, HTTPException
import requests
from threading import Thread
from settings import TOKEN
from queue import Queue
import requests
import re
import uvicorn


# In[ ]:


app = FastAPI()
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


# In[1]:


def f(n):
    res=0
    for i in range(n):
        res+=1
    return res


# In[ ]:


OFFSET = 1
task_queue = Queue()


# In[ ]:


def process_tasks(chat_id,n):
    result = f(n)
    send_message(chat_id, 'Вычислил f('+str(n)+'): '+str(result))


# In[ ]:


@app.post("/webhook")
async def telegram_webhook(request):
    update = await request.json()
    if "message" in update:
        OFFSET = update["update_id"] + 1
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        response_text = handle_message(text)
        send_message(chat_id, response_text)
    return {"status": "ok"}


# In[ ]:


def handle_message(text)
    if not chat_id or not text:
        continue
    if len(re.findall(r'[0-9]+[e]?[0-9]*',text))==1:
        n = int(text)
        send_message(chat_id, 'Сейчас вычислю f('+text+')')
        Thread(target=process_tasks, args=(chat_id,n), daemon=True).start()
    else:
        send_message(chat_id, "Что-то не так с твоим числом")


# In[ ]:


def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(TELEGRAM_API_URL, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка отправки сообщения: {response.status_code}, {response.text}")

