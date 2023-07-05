import pyswip_alt
import pandas as pd

# getting rules and user output to send on FE
rules = pd.read_csv('csv/rules.csv')
output = pd.read_csv('csv/output.csv')

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
                temp_list.append({'text': rules.iloc[value - 1].Recommendations,
                                  'COR': rules.iloc[value - 1].COR,
                                  'LOE': rules.iloc[value - 1].LOE,
                                  'Type': output[output['output'] == key]['type'].to_string(index=False)})

            dictionary['detail'] = temp_list

            final_output.append(dictionary)

    return final_output


# initiate prolog
def inference(evidences = ["."],
  measurements = [{".": 0}],
  intolerants = ["."],
  sex = "."
):
    prolog = pyswip_alt.PrologMT()
    prolog.consult('prolog/rules.pl')

    #Assert facts
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

    if intolerants:
      for intolerant in intolerants:
          prolog.assertz(f"intolerant({intolerant})")
    else:
          prolog.assertz("intolerant(.)")

    if sex == '':
      prolog.assertz("sex(.)")
    else:
      prolog.assertz(f"sex({sex})")

    # initiate getting recommendation from prolog
    recommendation_query = "recommendation(X, _)"
    recommendations = list(prolog.query(recommendation_query))

    rules_num_query = "recommendation(_, X)"
    rules_nums = list(prolog.query(rules_num_query))

    recommendation_outputs = output_and_rule_num(recommendations, rules_nums)

    # initiate getting contraindication from prolog
    contraindication_query = "contraindication(X, _)"
    contraindications = list(prolog.query(contraindication_query))

    contra_rules_num_query = "contraindication(_, X)"
    contra_rules_nums = list(prolog.query(contra_rules_num_query))

    contradiction_outputs = output_and_rule_num(contraindications, contra_rules_nums)

    # initiate getting No Benefit  from prolog
    no_benefit_query = "no_benefit(X, _)"
    no_benefits = list(prolog.query(no_benefit_query))

    no_benefit_rules_num_query = "no_benefit(_, X)"
    no_benefit_rules_nums = list(prolog.query(no_benefit_rules_num_query))

    no_benefit_outputs = output_and_rule_num(no_benefits, no_benefit_rules_nums)

    # resting all input for next run
    prolog.retractall("evidence(_)")
    prolog.retractall("measurement(_, _)")
    prolog.retractall("intolerant(_)")
    prolog.retractall("sex(_)")

    # temp var for all recommendations, contraindications, no_benefits result
    # return recommendation_outputs

    # return recommendation_outputs
    final_recommendations = append_text(recommendation_outputs)
    final_contraindications = append_text(contradiction_outputs)
    final_no_benefits = append_text(no_benefit_outputs)
    
    final_results = final_recommendations + final_contraindications + final_no_benefits

    return final_results
