from flask import Flask, session
import os
from controller.Controller import Controller

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    #app.config.from_object("settings")
    Controller(app).initialRouter()
    return app

if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)