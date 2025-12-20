from flask import Flask

app = Flask(__name__)

#rotas
@app.route("/")
def homepage():
    return "Meu site no Flask"

if __name__ == "__main__":
    app.run()