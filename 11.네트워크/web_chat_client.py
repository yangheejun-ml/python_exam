from flask import Flask
from flask import render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connected")
def connect_handler():
    socketio.emit("response", {"nickname": "서버", "message": "새로운 유저 입장"})

@socketio.on("chat")
def event_handler(json):
    json["nickname"] = json["nickname"].encode("latin1").decode("utf-8")
    json["message"] = json["message"].encode("latin1").decode("utf-8")

    socketio.emit("response", {"nickname": json["nickname"], "message": json["message"]})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=14000, debug=True)