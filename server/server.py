from flask import Flask
from flask import render_template, url_for
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/components/<file>')
def get_component(file="home.html"):
    return render_template("components/" + file)

@app.route('/<file>')
def get_html(file="home.html"):
    return render_template(file)
