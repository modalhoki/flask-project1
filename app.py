from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Fact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    information = db.Column(db.String(200), nullable = False)
    value = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<information added on %r>" % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method() == 'POST':
        pass
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(port=8888)
    app.run(debug=True)
