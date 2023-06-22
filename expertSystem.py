# import
import pandas as pd
import copy
import app

inputs = pd.read_csv("csv/input.csv", header=0)
data_input = inputs["input"]
data_description = inputs["desc"]
data_type = inputs["type"]

measurements = pd.read_csv("csv/measurement.csv", header=0)
measurement_input = measurements["measurement"]
measurement_desc = measurements["desc"]

print("----measure on testing----")
print(measurement_input)
print(type(measurement_input))
print(measurement_desc)
print(len(measurement_input))

# getting rules and user output to send on FE
rules = pd.read_csv('csv/rules.csv')
output = pd.read_csv('csv/output.csv')

# temp memory for input
evident_data_value = []
evident_data_desc = []

infeasible_data_value = []
infeasible_data_desc = []

history_data_value = []
history_data_desc = []

intolerant_data_value = []
intolerant_data_desc = []

unmarked_data_value = []
unmarked_data_desc = []

# sorting input into temp memory
for i in range(len(data_input)):
    current_type = data_type[i]
    if current_type == "History":
        history_data_value.append(data_input[i])
        history_data_desc.append(data_description[i])

    elif current_type == "evident":
        evident_data_value.append(data_input[i])
        evident_data_value.append(data_description[i])

    elif current_type == "intolerant":
        intolerant_data_value.append(data_input[i])
        intolerant_data_desc.append(data_description[i])

    elif current_type == "infeasible":
        infeasible_data_value.append(data_input[i])
        infeasible_data_desc.append(data_description[i])

    else:
        evident_data_value.append(data_input[i])
        evident_data_desc.append(data_description[i])

# getting selected input from user on FE
evidences = app.evidences
measurements = app.measurements
intolerance = app.intolerance
infeasible = app.infeasible
sex = app.sex


# adding index from cvs rules
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


# join all csv for text, COR leve, LOE level and Type of recommendation per recommendation
def append_text(output_list):
  pd.set_option('display.max_colwidth', 100)
  
  final_output = []

  for item in output_list:
    for key, values in item.items():
      dictionary = {}
      dictionary['output'] = output[output['output'] == key]['desc'].to_string(index=False)

      temp_list = []
      for value in values:
        temp_list.append({'text': rules.iloc[value-1].Recommendations,
                            'COR': rules.iloc[value-1].COR,
                            'LOE': rules.iloc[value-1].LOE,
                            'Type': output[output['output'] == key]['type'].to_string(index=False)})

      dictionary['detail'] = temp_list

      final_output.append(dictionary)

  return final_output


# initiate prolog
def generate_recommendation(evidences_prolog_input,
                            measurements_prolog_input,
                            intolerance_prolog_input,
                            infeasible_prolog_input,
                            sex_prolog_input):
    from pyswip import Prolog
    import pyswip_alt
    prolog = pyswip_alt.PrologMT()
    prolog.consult('rules1.pl')

    # return infeasible_prolog_input
    #
    # return [evidences_prolog_input,
    #         intolerance_prolog_input,
    #         infeasible_prolog_input,
    #         # sex_prolog_input,
    #         measurements_prolog_input]

    # Assert facts on prolog and set default fact if input is null
    if evidences_prolog_input:
        for evidence in evidences_prolog_input:
            prolog.assertz(f"evidence({evidence})")
    else:
        prolog.assertz("evidence(.)")

    if measurements_prolog_input:
        for measurement in measurements_prolog_input:
            for key, value in measurement.items():
                prolog.assertz(f"measurement({key}, {value})")
    else:
        prolog.assertz("measurement(., .)")

    if intolerance_prolog_input:
        for intolerant in intolerance_prolog_input:
            prolog.assertz(f"intolerant({intolerant})")
    else:
        prolog.assertz("intolerant(.)")

    if infeasible_prolog_input == '':
        prolog.assertz("infeasible(.)")
    else:
        prolog.assertz(f"infeasible({infeasible_prolog_input})")

    if sex_prolog_input == '':
        prolog.assertz("sex(.)")
    else:
        prolog.assertz(f"sex({sex_prolog_input})")

    # initiate getting recommendation from prolog
    print('-----Recommendation------')
    recommendation_query = "recommendation(X, _)"
    recommendations = list(prolog.query(recommendation_query))

    rules_num_query = "recommendation(_, X)"
    rules_nums = list(prolog.query(rules_num_query))

    recommendation_outputs = output_and_rule_num(recommendations, rules_nums)
    print(recommendation_outputs)

    # initiate getting contraindication from prolog
    print('\n------Contraindication------')
    contraindication_query = "contraindication(X, _)"
    contraindications = list(prolog.query(contraindication_query))

    contra_rules_num_query = "contraindication(_, X)"
    contra_rules_nums = list(prolog.query(contra_rules_num_query))

    contradiction_outputs = output_and_rule_num(contraindications, contra_rules_nums)
    print(contradiction_outputs)

    # initiate getting No Benefit  from prolog
    print('\n-------No Benefit-------')
    no_benefit_query = "no_benefit(X, _)"
    no_benefits = list(prolog.query(no_benefit_query))

    no_benefit_rules_num_query = "no_benefit(_, X)"
    no_benefit_rules_nums = list(prolog.query(no_benefit_rules_num_query))

    no_benefit_outputs = output_and_rule_num(no_benefits, no_benefit_rules_nums)
    print(no_benefit_outputs)

    # resting all input for next run
    prolog.retractall("evidence(_)")
    prolog.retractall("measurement(_, _)")
    prolog.retractall("infeasible(_)")
    prolog.retractall("intolerant(_)")
    prolog.retractall("sex(_)")

    # temp var for all recommendations, contraindications, no_benefits result
    # return recommendation_outputs

    # return recommendation_outputs
    final_recommendations = append_text(recommendation_outputs)
    # return final_recommendations

    final_contraindications = append_text(contradiction_outputs)
    final_no_benefits = append_text(no_benefit_outputs)

    # log
    print(final_recommendations)
    print(final_contraindications)
    print(final_no_benefits)

    return [final_recommendations, final_contraindications, final_no_benefits]
