from flask import Flask, render_template, url_for, request, redirect
import expertSystem
# import heart_prediction_default_input

from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)


# post csv ke database
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")


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

        # load the model from disk
        filename = 'model.pkl'
        load_model = joblib.load(filename)

        # append input here
        # age, sex, chest pain type, fasting blood sugar, max heart rate, exercise angina, old-peak, ST slope
        pred_prob = load_model.predict([pred_input])
        predict = (pred_prob >= 0.43).astype(int).reshape(-1)

        # --getting probability number
        probability_number = pred_prob[0][0]

        # --assign level based on probability number
        if 0 <= probability_number <= 0.43:
            probability_level = 1  # normal
        elif 0.44 <= probability_number <= 0.80:
            probability_level = 2  # gray area
        elif 0.81 <= probability_number <= 1.0:
            probability_level = 3  # high chance
        else:
            return "probability number '" + probability_number + "' should have been a number or between 0-100 please " \
                                                                 "check again"

        return render_template("/prediction-result.html",
                               probability_level=probability_level,
                               probability_number=probability_number,
                               sex=sex)
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

        return render_template('/expert-system-result.html',
                               recommendation_result=recommendation_result,
                               contraindications_result=contraindications_result,
                               no_benefits_result=no_benefits_result)

    else:

        return render_template('/expert-system.html',
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
                               measurement_unit=expertSystem.measurement_unit,
                               total_measurement=len(expertSystem.measurement_input),

                               unmark_selection_value=expertSystem.unmarked_data_value,
                               unmark_selection_desc=expertSystem.unmarked_data_desc,
                               )


# bridge from expert system result result
@app.route('/bridge', methods=['POST'])
def bridge():
    if request.method == 'POST':
        try:
            ps_patient_sex = request.form.get('ps_patient_sex')
            ps_patient_diagnoses = request.form.get('ps_patient_diagnose_result')

            if ps_patient_sex == '1':
                ps_patient_sex = 'male'
            elif ps_patient_sex == '0':
                ps_patient_sex = 'female'
            else:
                return "ps_patient_sex value does not fit the requirement should be string" \
                       " '0' or '1'"
        #     fix sex from number into string

        except():
            return "patient sex and patient diagnose value didn't pass"

        return render_template('/expert-system.html',
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
                               measurement_unit=expertSystem.measurement_unit,
                               total_measurement=len(expertSystem.measurement_input),

                               unmark_selection_value=expertSystem.unmarked_data_value,
                               unmark_selection_desc=expertSystem.unmarked_data_desc,

                               ps_patient_sex=ps_patient_sex,
                               ps_patient_diagnoses=ps_patient_diagnoses
                               )
    else:
        return "wrong use of route, meant to be from prediction result into expert system form"


if __name__ == "__main__":
    def reshape(arr):
        return np.array(arr).reshape(-1, 1, arr.shape[1])


    app.run(host='0.0.0.0', port=5000, debug=True)
