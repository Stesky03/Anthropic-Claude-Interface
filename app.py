from flask import Flask, render_template, request
import anthropic
from collections import defaultdict
import json

modello = "claude-3-7-sonnet-latest"
message_sequence = defaultdict(list)
prompt_file = open("data/prompt.json", "r")
all_prompts = json.load(prompt_file)


def forward_claude(id, message, mode):
    print(message)  # debug
    message_sequence[id].append({"role": "user", "content": message})

    risposta = anthropic.Anthropic().messages.create(
        model = modello,
        max_tokens = 2048,
        system = all_prompts[mode],
        messages = message_sequence[id]
    )

    testoRisposta = ""
    for i in risposta.content:
        testoRisposta += i.text
    message_sequence[id].append({"role": "assistant", "content": testoRisposta})

    return testoRisposta


app = Flask(__name__)
@app.route('/')
def index():
    if len(message_sequence) > 10:
        message_sequence.pop(next(iter(message_sequence)))
    return render_template("website.html")


@app.route(rule="/send-message", methods=["POST"])
def handle_request():
    if request.method == "POST":
        message = request.get_json()
        print(message) # debug
        answer = forward_claude(message["id"], message["msg"], message["mode"])
        # print(answer)
        return answer


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3302, threaded=True)
