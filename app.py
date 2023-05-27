from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import deepLearning
import vector
import expertSystem
import heart_prediction_default_input

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model.db'
db = SQLAlchemy(app)


class Fact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.Integer, nullable=False)
    resting_bp = db.Column(db.Integer, nullable=False)
    cholesterol = db.Column(db.Integer, nullable=False)
    fasting_blood_sugar = db.Column(db.Integer, nullable=False)
    resting_ecg = db.Column(db.Integer, nullable=False)
    max_heart_rate = db.Column(db.Integer, nullable=False)
    exercise_angina = db.Column(db.Integer, nullable=False)
    old_peak = db.Column(db.Float, nullable=False)
    st_slope = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<data on {self.id}>'


# post data ke database
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # get data from form

        age = request.form['age']
        sex = request.form['sex']
        chestPainType = request.form['chest_pain_type']
        resting_bp_s = request.form['resting_bp_s']
        cholesterol = request.form['cholesterol']
        fasting_blood_sugar = request.form['fasting_blood_sugar']
        resting_ecg = request.form['resting_ecg']
        max_heart_rate = request.form['max_heart_rate']
        exercise_angina = request.form['exercise_angina']
        old_peak = request.form['old_peak']
        st_slope = request.form['st_slope']

        print("----debugging2----")
        patient_fact1 = Fact(age=age,
                             sex=sex,
                             chestPainType=chestPainType,
                             resting_bp_s=resting_bp_s,
                             cholesterol=cholesterol,
                             fasting_blood_sugar=fasting_blood_sugar,
                             resting_ecg=resting_ecg,
                             max_heart_rate=max_heart_rate,
                             exercise_angina=exercise_angina,
                             old_peak=old_peak,
                             st_slope=st_slope)

        # patient_fact1 = Fact(age=1,sex=2,chest_pain_type=3,resting_bp_s=4,cholesterol=5,fasting_blood_sugar=6,resting_ecg=7,max_heart_rate=8,exercise_angina=9,old_peak=10,st_slope=11)

        try:
            app.app_context().push()
            db.session.add(patient_fact1)
            db.session.commit()
            return redirect('/')
        except:
            return "there is an issue bro"


    else:
        patient_fact = Fact.query.all()
        return render_template("index.html", patient_fact=patient_fact)


@app.route('/expert_system')
def expert_system():
    return render_template('/expert_system.html', task=[])


# input data
heart_diseases_input = heart_prediction_default_input.heart_diseases_input


@app.route('/heart_diseases_prediction', methods=['POST', 'GET'])
def heart_diseases_prediction():
    if request.method == 'POST':
        hasil_hitungan = 0

        for tipe_input in heart_diseases_input:
            current_data = request.form[tipe_input]
            # handle null value
            if current_data == '':
                print("null value on " + tipe_input)
                continue

            nilai = int(current_data)
            hasil_hitungan = hasil_hitungan + nilai

        return "total data adalah " + str(hasil_hitungan)

    else:
        # return render_template('/heart_diseases_prediction.html', inputs=heart_diseases_input)
        return render_template('/heart_diseases_prediction.html',
                               total_data=len(heart_diseases_input),
                               input=heart_diseases_input)

# @app.route('/delete/<int:id>')
# def delete(id):
#     # get current data
#     information_to_delete = Fact.query.get_or_404(id)
#     print(information_to_delete)
#
#     # delete data
#     try:
#         db.session.delete(information_to_delete)
#         print("is deleted")
#         db.session.commit()
#         print("is committed")
#         return redirect('/')
#     except:
#         return "there is an issue while deleting the information"


# @app.route('/update/<int:id>', methods=['POST', 'GET'])
# def update(id):
#     # get data
#     information_to_update = Fact.query.get_or_404(id)
#
#     if request.method == 'POST':
#         information_to_update.information = request.form['information_input_updated']
#         information_to_update.value = request.form['value_input_updated']
#
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'there is an issue ma man'
#
#     else:
#         return render_template('update.html', task=information_to_update)


if __name__ == '__main__':
    app.run(debug=True)
