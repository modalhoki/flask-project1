%%file stage_a_and_b.pl

% Stage A
recommendation(blood_pressure_control, 1):-
        evidence(accf_stage_a),
        evidence(hypertension).

recommendation(sglt2i, 2):-
        evidence(accf_stage_a),
        evidence(type_2_diabetes),
        (evidence(cvd); evidence(high_risk_cvd)).

recommendation(regular_physical_activity, 3):- evidence(accf_stage_a).
recommendation(normal_weight_control, 3):- evidence(accf_stage_a).
recommendation(healthy_diet, 3):- evidence(accf_stage_a).
recommendation(avoid_smoking, 3):- evidence(accf_stage_a).

recommendation(natriuretic_peptide_biomarker_screening, 4):- evidence(accf_stage_a).
recommendation(validated_multivariable_risk_score, 4):- evidence(accf_stage_a).

recommendation(validated_multivariable_risk_score, 5):- evidence(accf_stage_a).

% Stage B
recommendation(acei, 6):-
        evidence(accf_stage_b),
        measurement(lvef, X), X =< 40,
        \+ intolerant(acei).

recommendation(statins, 7):-
        evidence(accf_stage_b),
        (evidence(myocardial_infarction); evidence(acute_coronary_syndrome)).

recommendation(arb, 8):-
        evidence(accf_stage_b),
        evidence(myocardial_infarction),
        measurement(lvef, X), X =< 40,
        intolerant(acei).

recommendation(beta_blockers, 9):-
        evidence(accf_stage_b),
        measurement(lvef, X), X =< 40,
        (evidence(myocardial_infarction); evidence(acute_coronary_sindrome)).

recommendation(icd_therapy, 10):-
        evidence(accf_stage_b),
        evidence(mi_post_40_days),
        measurement(lvef, X), X =< 30,
        evidence(nyha_class_1),
        evidence(survival_year_greater_than_1).

recommendation(beta_blockers, 11):-
        evidence(accf_stage_b),
        measurement(lvef, X), X =< 40.

contraindication(thiazolidinediones, 12):-
        evidence(accf_stage_b),
        measurement(lvef, X), X =< 50.

contraindication(nondihydropyridine_ccb, 13):-
        evidence(accf_stage_b),
        measurement(lvef, X), X =< 50.