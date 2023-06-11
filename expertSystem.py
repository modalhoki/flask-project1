# import
import pandas as pd
from pyswip import Prolog
import copy
import app

# get data for input list
df = pd.read_csv("db.csv", header=0)
data_testing = df["input"]
data_type = df["type"]

# temp memory for input
history_data = []
diagnose_data = []
evident_data = []
intolerant_data = []
unmarked_data = []

# sorting input into temp memory
for i in range(len(data_testing)):
    current_type = data_type[i]
    if current_type == "History":
        history_data.append(data_testing[i])
    elif current_type == "diagnose":
        diagnose_data.append(data_testing[i])
    elif current_type == "evident":
        evident_data.append(data_testing[i])
    elif current_type == "intolereant":
        intolerant_data.append(data_testing[i])
    else:
        unmarked_data.append(data_testing[i])


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


# join all data for text, COR leve, LOE level and Type of recommendation per recommendation
def append_text(output_list):
    output_with_text = copy.deepcopy(output_list)

    for item in output_with_text:
        for key, values in item.items():
            temp_list = []
            for value in values:
                # ganti nama file
                temp_list.append({'text': rules.iloc[value - 1].Recommendations,
                                  'COR': rules.iloc[value - 1].COR,
                                  'LOE': rules.iloc[value - 1].LOE,
                                  'Type': output[output['output'] == key]['type'].item()})
            item[key] = temp_list

    return output_with_text


# initiate prolog
prolog = Prolog()
prolog.consult('rules.pl')

# input
# evidences = ['accf_stage_d', 'permanent_persistent_paroxysmal_af']
# measurements = []
# intolerants = ['']
# infeasible = ''
# sex = ''

# getting selected input from user on FE
evidences = app.evidences
measurements = app.measurements
intolerance = app.intolerance
infeasible = app.infeasible
sex = app.sex

# Assert facts on prolog and set default fact if input is null
if evidences:
    for evidence in evidences:
        prolog.assertz(f"evidence({evidence})")
else:
    prolog.assertz("evidence(.)")

if measurements:
    for measurement in measurements:
        for key, value in measurement.items():
            prolog.assertz(f"measurement({key}, {value})")
else:
    prolog.assertz("measurement(., .)")

if intolerance:
    for intolerant in intolerance:
        prolog.assertz(f"intolerant({intolerant})")
else:
    prolog.assertz("intolerant(.)")

if infeasible == '':
    prolog.assertz("infeasible(.)")
else:
    prolog.assertz(f"infeasible({infeasible})")

if sex == '':
    prolog.assertz("sex(.)")
else:
    prolog.assertz(f"sex({sex})")

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

# getting rules and user output to send on FE
rules = pd.read_csv('rules.csv')
output = pd.read_csv('output.csv')

# temp var for all recommendations, contraindications, no_benefits result
final_recommendations = append_text(recommendation_outputs)
final_contraindications = append_text(contradiction_outputs)
final_no_benefits = append_text(no_benefit_outputs)

# log
print(final_recommendations)
print(final_contraindications)
print(final_no_benefits)

# how to access each data
# for item in final_recommendations:
#   for key, values in item.items():
#     print(key)
#     for value in values:
#       print(value['text'])
#       print('COR: ' + value['COR'])
#       print('LOE: ' + value['LOE'])
#       print('Type: ' + value['Type'])
#     print("\n")
