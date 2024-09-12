from flask import Flask, render_template, request, redirect, url_for, jsonify
from collections import deque
import threading
from shared import prompts_queue  # Import from shared state

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prompts')
def get_prompts():
    # Convert prompts to JSON-serializable format
    serialized_prompts = [(str(user), text) for user, text in list(prompts_queue)]
    return jsonify({'prompts': serialized_prompts})

@app.route('/delete/<int:index>', methods=['POST'])
def delete_prompt(index):
    try:
        if 0 <= index < len(prompts_queue):
            del prompts_queue[index]
    except IndexError:
        pass
    return redirect(url_for('index'))

def run():
    app.run(host="0.0.0.0", port=8000)

def run_flask():
    threading.Thread(target=run).start()
