import json
import os
import gradio as gr
import requests

USERS_PATH = os.path.join(os.path.dirname(__file__), 'users.json')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')

with open(USERS_PATH, 'r') as f:
    USERS = json.load(f)


def authenticate(username, password):
    user = USERS.get(username)
    if user and user.get('password') == password:
        return True
    return False


def chat(user_input, history):
    resp = requests.post(
        'http://localhost:11434/api/generate',
        json={'model': OLLAMA_MODEL, 'prompt': user_input, 'stream': False},
        timeout=10
    )
    answer = resp.json().get('response', '') if resp.ok else 'Error'
    history = history + [[user_input, answer]]
    return history, history


def main():
    with gr.Blocks() as demo:
        gr.Markdown('# Leon Dashboard')
        with gr.Tab('Login'):
            user = gr.Textbox(label='Username')
            pwd = gr.Textbox(label='Password', type='password')
            login_btn = gr.Button('Login')
            login_out = gr.Text()

        with gr.Tab('Chat'):
            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            send = gr.Button('Send')

        with gr.Tab('Upload'):
            file = gr.File()

        with gr.Tab('Report'):
            generate_btn = gr.Button('Generate report')
            report_out = gr.File()

        def do_login(u, p):
            ok = authenticate(u, p)
            return 'Success' if ok else 'Invalid credentials'

        login_btn.click(do_login, [user, pwd], login_out)
        send.click(chat, [msg, chatbot], [chatbot, chatbot])
        generate_btn.click(lambda: 'report.docx', None, report_out)
    demo.launch()


if __name__ == '__main__':
    main()
