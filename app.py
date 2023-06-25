from flask import Flask, render_template, url_for, request, redirect
import expertSystem
import heart_prediction_default_input

from flask import Flask, render_template, request
# from flask_cors import CORS, cross_origin
import joblib
import numpy as np

app = Flask(__name__)


# post csv ke database
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")


# input csv
heart_diseases_input = heart_prediction_default_input.value


@app.route("/heart_disease_prediction", methods=["POST", "GET"])
# @cross_origin()
def heart_disease():
    if request.method == "POST":

        # get input
        age = int(request.form['age'])
        sex = int(request.form['sex'])
        chest_paint_type = int(request.form['chestPainType'])
        resting_bps = int(request.form['restingBloodPressure'])
        fasting_blood_sugar = int(request.form['fastingBloodSugar'])
        max_heart_rate = int(request.form['maxHeartRate'])
        exercise_angina = int(request.form['exerciseAngina'])
        old_peak = float(request.form['oldpeak'])
        st_slope = int(request.form['stSlope'])
        
        # prepare input
        pred_input = [age,
                      sex,
                      chest_paint_type,
                      resting_bps,
                      fasting_blood_sugar,
                      max_heart_rate,
                      exercise_angina,
                      old_peak,
                      st_slope]
        

        # return pred_input
        # return render_template("/prediction_result.html", prediction=1, probability=92.04)

        # load the model from disk
        filename = 'model.pkl'
        load_model = joblib.load(filename)

        # append input here
        # age, sex, chest pain type, fasting blood sugar, max heart rate, exercise angine, oldpeak, ST slope
        pred_prob = load_model.predict([pred_input])
        predict = (pred_prob >= 0.43).astype(int).reshape(-1)

        return render_template("/prediction_result.html", prediction=predict, probability=pred_prob[0][0])
    else:
        return render_template("/heart-disease-prediction.html")


# --set global variable for expert system
evidences = ['']
measurements = []
intolerance = ['']
infeasible = ['']
sex = ''
history = ''


@app.route('/expert_system', methods=['POST', 'GET'])
def expert_system():
    if request.method == 'POST':
        
        patient_sex = request.form.get('patient_sex')
        patient_diagnoses = request.form.get('patient_diagonose_result')
        
        return [patient_sex, patient_diagnoses]
        
        
        # --getting global variable
        global evidences
        global history
        global measurements
        global intolerance
        global infeasible
        global sex

        # --resting measurement value
        measurements = []

        # --getting value
        evidences = request.form.getlist('selected_evident')
        history = request.form.getlist('selected_history')
        intolerance = request.form.getlist('selected_intolerance')
        infeasible = request.form.getlist('selected_infeasible')
        sex = request.form.get('selected_sex')

        # --infeasible data fix
        if not infeasible:
            infeasible = ''
        else:
            infeasible = infeasible[0]

        # return [evidences, history, intolerance, infeasible, sex]

        # --getting measurement
        for i in range(6):
            current_measurement_value = request.form.get(expertSystem.measurement_input[i])
            if current_measurement_value == '':
                break

            measurements.append(
                {expertSystem.measurement_input[i]: int(current_measurement_value)}
            )

        # --merging history into evidence
        for current_history in history:
            evidences.append(current_history)

        # initiate prolog
        prolog_final_result = expertSystem.generate_recommendation(evidences,
                                                                   measurements,
                                                                   intolerance,
                                                                   infeasible,
                                                                   sex)

        recommendation_result = prolog_final_result[0]
        contraindications_result = prolog_final_result[1]
        no_benefits_result = prolog_final_result[2]

        return render_template('/expert_system_result.html',
                               recommendation_result=recommendation_result,
                               contraindications_result=contraindications_result,
                               no_benefits_result=no_benefits_result)

    else:

        return render_template('/expert_system.html',
                               eveident_selection_value=expertSystem.evident_data_value,
                               eveident_selection_desc=expertSystem.evident_data_desc,
                               total_eveident_selection=len(expertSystem.evident_data_value),

                               infeasible_selection_value=expertSystem.infeasible_data_value,
                               infeasible_selection_desc=expertSystem.infeasible_data_desc,
                               total_infeasible_selection=len(expertSystem.infeasible_data_value),

                               history_selection_value=expertSystem.history_data_value,
                               history_selection_desc=expertSystem.history_data_desc,
                               total_history_selection=len(expertSystem.history_data_value),

                               intolearant_selection_value=expertSystem.intolerant_data_value,
                               intolearant_selection_desc=expertSystem.intolerant_data_desc,
                               total_intolearant_selection=len(expertSystem.intolerant_data_value),

                               measurement_value=expertSystem.measurement_input,
                               measurement_desc=expertSystem.measurement_desc,
                               total_measurement=len(expertSystem.measurement_input),

                               unmark_selection_value=expertSystem.unmarked_data_value,
                               unmark_selection_desc=expertSystem.unmarked_data_desc,
                               )


if __name__ == "__main__":
    def reshape(arr):
        return np.array(arr).reshape(-1, 1, arr.shape[1])


    app.run(debug=True)
