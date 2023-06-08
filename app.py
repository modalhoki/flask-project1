from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import deepLearning
import vector
import expertSystem
import heart_prediction_default_input
import pandas as pd
from pyswip import Prolog
import copy

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
def output_and_rule_num(outputs, rule_nums):
    temp_outputs = []

    for output, num in zip(outputs, rule_nums):
        temp_outputs.append({output['X']: [num['X']]})

    outputs = []
    key_values = {}

    for item in temp_outputs:
        for key, value in item.items():
            if key in key_values:
                key_values[key].update(value)
            else:
                key_values[key] = set(value)

    for key, value in key_values.items():
        outputs.append({key: list(value)})

    return outputs


prolog = Prolog()
prolog.consult('stage_a_and_b.pl')

# input
evidences = ['accf_stage_b']
measurements = [{'lvef': 35}]
intolerants = ['.']

# Assert facts
for evidence in evidences:
    prolog.assertz(f"evidence({evidence})")

for measurement in measurements:
    for key, value in measurement.items():
        prolog.assertz(f"measurement({key}, {value})")

for intolerant in intolerants:
    prolog.assertz(f"intolerant({intolerant})")

# --- Recommendation ----
print('Recommendation')

recommendation_query = "recommendation(X, _)"
recommendations = list(prolog.query(recommendation_query))

rules_num_query = "recommendation(_, X)"
rules_nums = list(prolog.query(rules_num_query))

recommendation_outputs = output_and_rule_num(recommendations, rules_nums)
print(recommendation_outputs)

# --- Contraindication ---
print('\nContraindication')
contraindication_query = "contraindication(X, _)"
contraindications = list(prolog.query(contraindication_query))

contra_rules_num_query = "contraindication(_, X)"
contra_rules_nums = list(prolog.query(contra_rules_num_query))

contradiction_outputs = output_and_rule_num(contraindications, contra_rules_nums)
print(contradiction_outputs)


# Remove asserted facts
prolog.retractall("evidence(_)")
prolog.retractall("measurement(_, _)")
prolog.retractall("intolerant(_)")

# Read file.csv terlebih dahulu
rules_df = pd.read_csv('stage_a_and_b.csv')
output_df = pd.read_csv('output.csv')


def append_text(output_list):
    output_with_text = copy.deepcopy(output_list)

    for data in output_with_text:
        for key, values in data.items():
            temp_list = []
            for value in values:
                # ganti nama file
                temp_list.append({'text': rules_df.iloc[value - 1].Recommendations,
                                  'COR': rules_df.iloc[value - 1].COR,
                                  'LOE': rules_df.iloc[value - 1].LOE,
                                  'Type': output_df[output_df['output'] == key]['type'].item()})
            data[key] = temp_list

    return output_with_text


final_recommendations = append_text(recommendation_outputs)
final_contraindications = append_text(contradiction_outputs)
# final_no_benefits = append_text(no_benefit_outputs)

print(final_recommendations)
print(final_contraindications)
# print(final_no_benefits)

# cara akses
for item in final_recommendations:
    for key, values in item.items():
        print(key)
        for value in values:
            print(value['text'])
            print('COR: ' + value['COR'])
            print('LOE: ' + value['LOE'])
            print('Type: ' + value['Type'])
            print("\n")


# cara akses
for item in final_contraindications:
    for key, values in item.items():
        print(key)
        for value in values:
            print(value['text'])
            print('COR: ' + value['COR'])
            print('LOE: ' + value['LOE'])
            print('Type: ' + value['Type'])
            print("\n")


# on testing

@app.route('/expert_system', methods=['POST', 'GET'])
def expert_system():
    if request.method == 'POST':
        # ------ selected data ------
        selected_evident = request.form.getlist('selected_evident')
        selected_diagnose = request.form.getlist('selected_diagnose')
        selected_history = request.form.getlist('selected_history')
        selected_intolerant = request.form.getlist('selected_intolerant')
        selected_intolerant = request.form.getlist('selected_intolerant')
        # ------- selected data ------

        return selected_evident + selected_history + selected_diagnose + selected_intolerant
    else:
        # render page and assign data for selection
        # --> please do another check
        return render_template('/expert_system.html',
                               all_selection_option=expertSystem.data_testing,
                               eveident_selection=expertSystem.evident_data,
                               diagonse_selection=expertSystem.diagnose_data,
                               history_selection=expertSystem.history_data,
                               intolearant_selection=expertSystem.intolerant_data,
                               final_on_testing= final_recommendations)




if __name__ == '__main__':
    app.run(debug=True)
