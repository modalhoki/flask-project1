# inserting data
import pandas as pd
from pyswip import Prolog
import copy

df = pd.read_csv("db.csv", header=0)
data_testing = df["input"]
data_type = df["type"]

# set temp memory
history_data = []
diagnose_data = []
evident_data = []
intolerant_data = []
unmarked_data = []

# raw data sorting into temp memory
# --> please do another check
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


# # expert system bellow
# def output_and_rule_num(outputs, rule_nums):
#     temp_outputs = []
#
#     for output, num in zip(outputs, rule_nums):
#         temp_outputs.append({output['X']: [num['X']]})
#
#     outputs = []
#     key_values = {}
#
#     for item in temp_outputs:
#         for key, value in item.items():
#             if key in key_values:
#                 key_values[key].update(value)
#             else:
#                 key_values[key] = set(value)
#
#     for key, value in key_values.items():
#         outputs.append({key: list(value)})
#
#     return outputs
#
#
# prolog = Prolog()
# prolog.consult("stage_a_and_b.pl")
#
# # input
# evidences = ['accf_stage_b']
# measurements = [{'lvef': 35}]
# intolerants = ['.']
#
# # Assert facts
# for evidence in evidences:
#     prolog.assertz(f"evidence({evidence})")
#
# for measurement in measurements:
#     for key, value in measurement.items():
#         prolog.assertz(f"measurement({key}, {value})")
#
# for intolerant in intolerants:
#     prolog.assertz(f"intolerant({intolerant})")
#
# # --- Recommendation ----
# print('Recommendation')
#
# recommendation_query = "recommendation(X, _)"
# recommendations = list(prolog.query(recommendation_query))
#
# rules_num_query = "recommendation(_, X)"
# rules_nums = list(prolog.query(rules_num_query))
#
# recommendation_outputs = output_and_rule_num(recommendations, rules_nums)
# print(recommendation_outputs)
#
# # --- Contraindication ---
# print('\nContraindication')
# contraindication_query = "contraindication(X, _)"
# contraindications = list(prolog.query(contraindication_query))
#
# contra_rules_num_query = "contraindication(_, X)"
# contra_rules_nums = list(prolog.query(contra_rules_num_query))
#
# contradiction_outputs = output_and_rule_num(contraindications, contra_rules_nums)
# print(contradiction_outputs)
#
#
# # Remove asserted facts
# prolog.retractall("evidence(_)")
# prolog.retractall("measurement(_, _)")
# prolog.retractall("intolerant(_)")
#
# # Read file.csv terlebih dahulu
# rules_df = pd.read_csv('stage_a_and_b.csv')
# output_df = pd.read_csv('output.csv')
#
#
# def append_text(output_list):
#     output_with_text = copy.deepcopy(output_list)
#
#     for data in output_with_text:
#         for key, values in data.items():
#             temp_list = []
#             for value in values:
#                 # ganti nama file
#                 temp_list.append({'text': rules_df.iloc[value - 1].Recommendations,
#                                   'COR': rules_df.iloc[value - 1].COR,
#                                   'LOE': rules_df.iloc[value - 1].LOE,
#                                   'Type': output_df[output_df['output'] == key]['type'].item()})
#             data[key] = temp_list
#
#     return output_with_text
#
#
# final_recommendations = append_text(recommendation_outputs)
# final_contraindications = append_text(contradiction_outputs)
# # final_no_benefits = append_text(no_benefit_outputs)
#
# print(final_recommendations)
# print(final_contraindications)
# # print(final_no_benefits)
#
# # cara akses
# for item in final_recommendations:
#     for key, values in item.items():
#         print(key)
#         for value in values:
#             print(value['text'])
#             print('COR: ' + value['COR'])
#             print('LOE: ' + value['LOE'])
#             print('Type: ' + value['Type'])
#             print("\n")
#
#
# # cara akses
# for item in final_contraindications:
#     for key, values in item.items():
#         print(key)
#         for value in values:
#             print(value['text'])
#             print('COR: ' + value['COR'])
#             print('LOE: ' + value['LOE'])
#             print('Type: ' + value['Type'])
#             print("\n")
