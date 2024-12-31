from flask import Flask, render_template, request
import anthropic
from collections import defaultdict
from re import sub
import json

modelli = ["claude-3-haiku-20240307", "claude-3-5-sonnet-latest"]
messageSequence = defaultdict(list)

def htmlToStr(message):
    message = str(message)
    message = message.replace("</div><div>", "\n")
    message = message.replace("<br>", "\n")
    message = message.replace("<div>", "")
    message = message.replace("</div>", "")
    message = message.replace("<font style=\"vertical-align: inherit;\">", "")
    message = message.replace("</font>", "")
    return message

def strToHtml(message):
    message = str(message)
    message = message.replace("\n", "<br>")
    return message

def prepareAnswer(message):
    sub('<', '&lt;', message)
    sub('>', '&gt;', message)
    return message
def forwardClaude(id, message):
    modello = modelli[1]  # usa di default il modello sonnet

    print(message)  # debug
    messageSequence[id].append({"role": "user", "content": message})

    risposta = anthropic.Anthropic().messages.create(
        model=modello,
        max_tokens=2048, # da rendere variabile, anche quello sotto
        system="You are interacting with a single user (so don't worry about being nice to me) who is a university student, with years of programming experience. Adjust your responses accordingly:\n1)Provide detailed, technical explanations without oversimplifying concepts unless explicitly asked to do so.\n2)Express uncertainty when you're not confident about an answer.\n3)Feel free to ask for additional information if it would help you provide a more comprehensive or accurate response.\n4)Assume a high level of technical knowledge across various fields, especially in programming\n5)When discussing code or technical concepts, you can go into advanced details without needing to explain basics.\n6)do not write code unless necessary\n7)Reply in english or italian",
        messages=messageSequence[id]
    )

    testoRisposta = ""
    for i in risposta.content:
        testoRisposta += i.text
    messageSequence[id].append({"role": "assistant", "content": testoRisposta})
    return testoRisposta

app = Flask(__name__)
@app.route('/')
def index():
    if len(messageSequence) > 100:
        messageSequence.pop(next(iter(messageSequence)))
    return render_template("website.html")

@app.route(rule="/send-message", methods=["POST"])
def handle_request():
    if request.method == "POST":
        message = request.get_json()
        print(message)
        message["question"] = htmlToStr(message["question"])
        answer = forwardClaude(message["id"], message["question"])
        # print(answer)
        # answer = strToHtml(answer)    questo va bene se l'output è puro html, non va bene se è MD (viene gestito in js)
        answer = prepareAnswer(answer) # risposta in MD
        return answer

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3302, threaded=True)
