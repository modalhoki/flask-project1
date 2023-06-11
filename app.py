from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
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


# data input ev
data_ev = ["evident1", "evident2", "evident3"]
# data input his
data_his = ["history1", "history2", "history3"]
# data input di
edata_di = ["diagnose1", "diagnose2", "diagnose3"]
# data input int
data_int = ["intolerant1", "intolerant2", "intolerant3"]

# input data
heart_diseases_input = heart_prediction_default_input.value


@app.route('/heart_diseases_prediction', methods=['POST', 'GET'])
def heart_diseases_prediction():
    # passing patient value
    if request.method == 'POST':
        hasil_hitungan = 0

        for tipe_input in heart_diseases_input:
            current_form_name = tipe_input[0]
            current_form_value = request.form[current_form_name]
            # handle null value
            if current_form_value == '':
                print("null value on " + tipe_input)
                continue

            # -------apply the model here---------
            nilai = int(current_form_value)
            hasil_hitungan = hasil_hitungan + nilai
            # -------apply the model here---------

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


# on testing
# expert system bellow
# on testing

evidences = ['accf_stage_d', 'permanent_persistent_paroxysmal_af']
measurements = []
intolerance = ['']
infeasible = ''
sex = ''


@app.route('/expert_system', methods=['POST', 'GET'])
def expert_system():
    if request.method == 'POST':
        # # ------ selected data ------
        # selected_evident = request.form.getlist('selected_evident')
        # selected_diagnose = request.form.getlist('selected_diagnose')
        # selected_history = request.form.getlist('selected_history')
        # selected_intolerant = request.form.getlist('selected_intolerant')
        # selected_intolerant = request.form.getlist('selected_intolerant')
        # # ------- selected data ------

        # data gateway
        evidences = request.form.getlist('selected_evident') + request.form.getlist('selected_history')
        measurements = []
        intolerants = request.form.getlist('selected_history')
        infeasible = ''
        sex = ''

        # final_temp = expertSystem.final_recommendations + expertSystem.final_contraindications + expertSystem.final_no_benefits

        testing_data = expertSystem.final_recommendations
        heh_data = testing_data[0]
        heh_data2 = testing_data[1]

#
        result_title = []
        result_text = []
        cor_level = []
        loe_level = []
        treatment_type = []
        final_result =[]



        for item in testing_data:
            for key, values in item.items():
                print(key)
                for value in values:
                    print(value['text'])
                    print('COR: ' + value['COR'])
                    print('LOE: ' + value['LOE'])
                    print('Type: ' + value['Type'])
                print("\n")

        for item in testing_data:
            for key, values in item.items():
                result_title.append(key)
                for value in values:
                    result_text.append(value['text'])
                    cor_level.append(value['COR'])
                    loe_level.append(value['LOE'])
                    treatment_type.append(value['Type'])

        return render_template('/expert_system_result.html',
                               result_title=result_title,
                               result_text=result_text,
                               cor_level=cor_level,
                               loe_level=loe_level,
                               treatment_type=treatment_type,
                               total_recommedation=len(result_title))
        # return final_temp
    else:
        # render page and assign data for selection
        # --> please do another check
        return render_template('/expert_system.html',
                               all_selection_option=expertSystem.data_testing,
                               # eveident_selection=expertSystem.evident_data,
                               eveident_selection=['accf_stage_d', 'permanent_persistent_paroxysmal_af'],
                               diagonse_selection=expertSystem.diagnose_data,
                               history_selection=expertSystem.history_data,
                               intolearant_selection=expertSystem.intolerant_data)


if __name__ == '__main__':
    app.run(debug=True)
