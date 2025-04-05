#//////////////////////////////////////////////// with tkinter ui ////////////////////////////////////////////////
'''
import tkinter as tk
from tkinter import scrolledtext
import requests
import json

def get_code_from_qwen(prompt):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "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"  # جایگزین کنید
    }
    data = {
        "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def send_request():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        return
    response = get_code_from_qwen(user_input)
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"\nUser: {user_input}\nBot: {response}\n" + "-"*50)
    output_text.config(state=tk.DISABLED)
    input_text.delete("1.0", tk.END)

# ایجاد پنجره اصلی
root = tk.Tk()
root.title("Code Chatbot")
root.geometry("600x400")

# ورودی کاربر
input_text = tk.Text(root, height=5, width=70)
input_text.pack(pady=5)

# دکمه ارسال
send_button = tk.Button(root, text="Send", command=send_request)
send_button.pack()

# نمایش خروجی
output_text = scrolledtext.ScrolledText(root, height=15, width=70, state=tk.DISABLED)
output_text.pack(pady=5)

# اجرای برنامه
root.mainloop()
'''


#//////////////////////////////////////////////// with html test1 ////////////////////////////////////////////////
'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # فعال‌سازی CORS برای ارتباط فرانت‌اند

API_KEY = "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"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_prompt = data.get("prompt", "")
    if not user_prompt:
        return jsonify({"error": "Empty prompt"}), 400

    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "messages": [{"role": "user", "content": user_prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return jsonify(response.json()["choices"][0]["message"])
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
'''



#//////////////////////////////////////////////// with html test2 ////////////////////////////////////////////////

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# تنظیمات API
API_KEY = "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"  # api code here
BASE_URL = "https://integrate.api.nvidia.com/v1"

# تنظیم کلاینت OpenAI
client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_prompt = data.get("prompt", "")
    if not user_prompt:
        return jsonify({"error": "Empty prompt"}), 400

    try:
        # ارسال درخواست به NVIDIA API
        response = client.chat.completions.create(
            model="qwen/qwen2.5-coder-32b-instruct",
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False  # اگر نمی‌خواهید Streaming استفاده کنید، این پارامتر را False قرار دهید
        )

        # استخراج پاسخ
        content = response.choices[0].message.content
        return jsonify({"content": content})

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)






#//////////////////////////////////////////////// with html test3 chat history ////////////////////////////////////////////////
'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# تنظیمات API
API_KEY = "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"  # کلید API خود را قرار دهید
BASE_URL = "https://integrate.api.nvidia.com/v1"

# تنظیم کلاینت OpenAI
client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)

# تاریخچه پیام‌ها
chat_history = []

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history
    data = request.json

    # دریافت داده‌ها از درخواست
    user_prompt = data.get("prompt", "")
    temperature = data.get("temperature", 0.7)
    max_tokens = data.get("max_tokens", 1024)
    top_p = data.get("top_p", 0.9)
    presence_penalty = data.get("presence_penalty", 0.0)
    frequency_penalty = data.get("frequency_penalty", 0.0)

    if not user_prompt:
        return jsonify({"error": "Empty prompt"}), 400

    try:
        # اضافه کردن پیام کاربر به تاریخچه
        chat_history.append({"role": "user", "content": user_prompt})

        # ارسال درخواست به NVIDIA API
        response = client.chat.completions.create(
            model="qwen/qwen2.5-coder-32b-instruct",
            messages=chat_history,  # ارسال تاریخچه به عنوان زمینه
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stream=False  # اگر نمی‌خواهید Streaming استفاده کنید، این پارامتر را False قرار دهید
        )

        # استخراج پاسخ
        content = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": content})  # اضافه کردن پاسخ به تاریخچه

        return jsonify({"content": content})

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/clear-history", methods=["POST"])
def clear_history():
    global chat_history
    chat_history = []  # پاک کردن تاریخچه پیام‌ها
    return jsonify({"message": "Chat history cleared successfully."}), 200

if __name__ == "__main__":
    app.run(debug=True)
'''






#//////////////////////////////////////////////// with html test4 chat history ////////////////////////////////////////////////
'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import uuid

app = Flask(__name__)
CORS(app)

# تنظیمات API
API_KEY = "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"  # کلید API خود را قرار دهید
BASE_URL = "https://integrate.api.nvidia.com/v1"

# تنظیم کلاینت OpenAI
client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)

# تاریخچه چت‌ها
chat_sessions = {}  # ساختار: {session_id: [{"role": "user", "content": "..."}, ...]}

@app.route("/start-session", methods=["POST"])
def start_session():
    session_id = str(uuid.uuid4())  # ایجاد یک شناسه منحصر به فرد برای چت
    chat_sessions[session_id] = []
    return jsonify({"session_id": session_id}), 200

@app.route("/generate-title", methods=["POST"])
def generate_title():
    data = request.json
    user_prompt = data.get("prompt", "")

    if not user_prompt:
        return jsonify({"error": "Empty prompt"}), 400

    try:
        response = client.chat.completions.create(
            model="qwen/qwen2.5-coder-32b-instruct",
            messages=[
                {"role": "system", "content": "Generate a short title for the following prompt:"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=16,
            top_p=0.9,
            stream=False
        )
        title = response.choices[0].message.content.strip()
        return jsonify({"title": title})

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id")
    user_prompt = data.get("prompt", "")
    temperature = data.get("temperature", 0.7)
    max_tokens = data.get("max_tokens", 1024)
    top_p = data.get("top_p", 0.9)
    presence_penalty = data.get("presence_penalty", 0.0)
    frequency_penalty = data.get("frequency_penalty", 0.0)

    if not session_id or session_id not in chat_sessions:
        return jsonify({"error": "Invalid session ID"}), 400

    if not user_prompt:
        return jsonify({"error": "Empty prompt"}), 400

    try:
        chat_sessions[session_id].append({"role": "user", "content": user_prompt})

        response = client.chat.completions.create(
            model="qwen/qwen2.5-coder-32b-instruct",
            messages=chat_sessions[session_id],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stream=False
        )

        content = response.choices[0].message.content
        chat_sessions[session_id].append({"role": "assistant", "content": content})
        return jsonify({"content": content})

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/get-session-history", methods=["POST"])
def get_session_history():
    data = request.json
    session_id = data.get("session_id")

    if session_id not in chat_sessions:
        return jsonify({"error": "Session not found"}), 404

    return jsonify({"history": chat_sessions[session_id]}), 200

@app.route("/update-message", methods=["POST"])
def update_message():
    data = request.json
    session_id = data.get("session_id")
    message_index = data.get("message_index")
    new_content = data.get("new_content")

    if session_id not in chat_sessions:
        return jsonify({"error": "Session not found"}), 404

    if message_index >= len(chat_sessions[session_id]):
        return jsonify({"error": "Message index out of range"}), 400

    chat_sessions[session_id][message_index]["content"] = new_content
    return jsonify({"message": "Message updated successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
'''