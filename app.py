from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Fact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    information = db.Column(db.String(200), nullable=False)
    value = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<information on {self.information}>'


# post data ke database
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # pass
        # return "hello this is post method"
        task_information = request.form['information_input']
        task_value = request.form['value_input']

        print("----debugging1----")
        print(task_information)
        print(task_value)

        print("----debugging2----")
        new_task = Fact(information=task_information, value=task_value)
        print(new_task.information)
        print(new_task.value)

        try:
            print("----trying----")
            app.app_context().push()
            db.session.add(new_task)
            print("----1st is added----")
            db.session.commit()
            print("----1st is committed----")
            return redirect('/')
        except:
            return "there is an issue bro"


    else:
        tasks = Fact.query.order_by(Fact.date_created).all()
        return render_template("index.html", tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    # get current data
    information_to_delete = Fact.query.get_or_404(id)
    print(information_to_delete)

    # delete data
    try:
        db.session.delete(information_to_delete)
        print("is deleted")
        db.session.commit()
        print("is committed")
        return redirect('/')
    except:
        return "there is an issue while deleting the information"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    # get data
    information_to_update = Fact.query.get_or_404(id)

    if request.method == 'POST':
        information_to_update.information = request.form['information_input_updated']
        information_to_update.value = request.form['value_input_updated']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there is an issue ma man'

    else:
        return render_template('update.html', task=information_to_update)


if __name__ == '__main__':
    app.run(debug=True)
