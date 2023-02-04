#initialize a flask app for hello world
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
