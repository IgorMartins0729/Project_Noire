from main import app
from flask import render_template

#rotas
@app.route("/")
def homepage():
    return render_template("./index.html")