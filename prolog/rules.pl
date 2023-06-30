
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

recommendation(validated_multivariable_risk_score, 5):- evidence(accf_stage_a).


% Stage B
recommendation(acei, 6):-
        evidence(accf_stage_b),
        measurement(lvef, X), X =< 40,
        \+ intolerant(acei).

recommendation(statins, 7):- 
        evidence(accf_stage_b),
        evidence(myocardial_infarction).

recommendation(arb, 8):-
        evidence(accf_stage_b),
        evidence(myocardial_infarction), 
        measurement(lvef, X), X =< 40,
        intolerant(acei).

recommendation(beta_blockers, 9):-
        evidence(accf_stage_b),
        measurement(lvef, X), X =< 40,
        evidence(myocardial_infarction).

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


%Stage C
recommendation(multidisciplinary_teams_care, 14):- evidence(accf_stage_c).

recommendation(patient_education_and_support, 15):- evidence(accf_stage_c).

recommendation(respiratory_illnesses_vactination, 16):- evidence(accf_stage_c).

recommendation(depression_screening, 17):- evidence(accf_stage_c).

recommendation(sodium_restriction, 18):- evidence(accf_stage_c).

recommendation(regular_physical_activity, 19):- evidence(accf_stage_c).

recommendation(cardiac_rehabilitation, 20):- evidence(accf_stage_c).
                                                      
recommendation(diuretics, 21):- 
        evidence(accf_stage_c),
        evidence(fluid_retention).

recommendation(thiazide, 22):-
        evidence(accf_stage_c),
        evidence(congestive_symptomps),
        evidence(does_not_respond_to_loop_diuretics).

recommendation(arni, 23):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40,
        (evidence(nyha_class_2);evidence(nyha_class_3)),
        \+ infeasible(arni).

recommendation(acei, 24):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40,
        (evidence(nyha_class_2);evidence(nyha_class_3)),
        infeasible(arni),
        \+ intolerant(acei).

recommendation(arb, 25):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40,
        (evidence(nyha_class_2);evidence(nyha_class_3)),
        intolerant(acei),
        infeasible(arni).

recommendation(arni, 27):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40,
        (evidence(nyha_class_2);evidence(nyha_class_3)),
        \+ infeasible(arni),
        \+ intolerant(acei),
        \+ intolerant(arb).

contraindication(acei, 29):- 
        evidence(accf_stage_c),
        (recommendation(arni, 10); recommendation(arni, 14)).

contraindication(arni, 30):- 
        evidence(accf_stage_c),
        evidence(angioderma).

contraindication(acei, 31):- 
        evidence(accf_stage_c),
        evidence(angioderma).

recommendation(beta_blockers, 32):- 
        evidence(accf_stage_c), 
        measurement(lvef, X), X =< 40,
        (evidence(nyha_class_2);evidence(nyha_class_3)).

recommendation(mra, 34):-
        evidence(accf_stage_c),
        (evidence(nyha_class_2);evidence(nyha_class_3);evidence(nyha_class_4)),
        measurement(gfr, X), X > 30,
        measurement(potassium, Y), Y < 5.

contraindication(mra_precaution, 36):-
        evidence(accf_stage_c),
        (evidence(nyha_class_2);evidence(nyha_class_3);evidence(nyha_class_4)),
        measurement(gfr, X), X > 30,
        measurement(potassium, Y), Y < 5.

recommendation(sglt2i, 37):- 
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40,
        (evidence(nyha_class_2);evidence(nyha_class_3)).

recommendation(pufa, 42):-
        evidence(accf_stage_c),
        (evidence(nyha_class_2);evidence(nyha_class_3);evidence(nyha_class_4)).

recommendation(potassium_binder, 43):-
        evidence(accf_stage_c),
        (evidence(hyperkalemia);measurement(potassium, X), X >= 5.5).

no_benefit(anticoagulant, 44):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40,
        \+ (evidence(vte);evidence(atrial_fibrillation)).

no_benefit(dihydropyrinde_ccb, 45):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40.

no_benefit(vitamins, 46):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40.

no_benefit(nutritional_supplements, 46):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40.

no_benefit(hormonal_therapy, 46):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40.

contraindication(nondihydropyridine_ccb, 47):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40.

contraindication(class_ic_antiarrhythmic, 48):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40.

contraindication(dronedarone, 48):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40.

contraindication(thiazolidinediones, 49):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40.

contraindication(saxagliptin, 50):-
        evidence(accf_stage_c),
        evidence(type_2_diabetes),
        evidence(high_risk_cvd).

contraindication(alogliptin, 50):-
        evidence(accf_stage_c),
        evidence(type_2_diabetes),
        evidence(high_risk_cvd).

contraindication(nsaids, 51):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40.

recommendation(medication_titration, 52):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40.

recommendation(weekly_titration, 53):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40.

recommendation(ivabradine, 54):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40,
        (evidence(nyha_class_2);evidence(nyha_class_3)),
        measurement(lvef, X), X =< 35,
        measurement(resting_heart_rate, Y), Y >= 70,
        evidence(sinus_rhythm).

recommendation(digoxin, 55):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40.

recommendation(vericiguat, 56):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40,
        evidence(worsen_hf).

recommendation(icd_therapy, 57):-
        evidence(accf_stage_c),
        (evidence(nyha_class_2);evidence(nyha_class_3)),
        measurement(lvef, X), X =< 35,
        (evidence(nonschemic_dcm) ;evidence(ichemic_heart_disease)),
        evidence(survival_year_greater_than_1),
        evidence(mi_post_40_day).

recommendation(icd_therapy, 59):-
        evidence(accf_stage_c),
        evidence(nyha_class_1),
        measurement(lvef, X), X =< 30,
        evidence(survival_year_greater_than_1),
        evidence(mi_post_40_day).

recommendation(crt, 60):-
        evidence(accf_stage_c),
        evidence(sinus_rhythm),
        (evidence(nyha_class_2);evidence(nyha_class_3); evidence(nyha_class_4)),
        measurement(lvef, X), X =< 35,
        evidence(lbbb),
        measurement(qrs, Y), Y >= 150.

recommendation(crt, 62):-
        evidence(accf_stage_c),
        evidence(sinus_rhythm),
        (evidence(nyha_class_2);evidence(nyha_class_3), evidence(nyha_class_4)),
        measurement(lvef, X), X =< 35,
        evidence(non_lbbb),
        measurement(qrs, Y), Y >= 150.

recommendation(crt, 63):-
        evidence(accf_stage_c),
        measurement(lvef, X), X >= 36, X =< 50,
        (evidence(second_degree_av_block); evidence(third_degree_av_block)).

recommendation(crt, 64):-
        evidence(accf_stage_c),
        evidence(sinus_rhythm),
        (evidence(nyha_class_2);evidence(nyha_class_3), evidence(nyha_class_4)),
        measurement(lvef, X), X =< 35,
        evidence(lbbb),
        measurement(qrs, Y), Y > 120, Y =< 149.

recommendation(crt, 65):-
        evidence(accf_stage_c),
        evidence(atrial_fibrillation),
        measurement(lvef, X), X =< 35,
        evidence(requires_ventricular_pacing).

recommendation(crt, 66):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 35,
        evidence(requires_ventricular_pacing).

recommendation(icd_therapy, 67):-
        evidence(accf_stage_c),
        evidence(arrhythmogenic_cardiomyopathy), 
        measurement(lvef, X), X =< 45.

recommendation(crt, 68):-
        evidence(accf_stage_c),
        evidence(sinus_rhythm),
        (evidence(nyha_class_3), evidence(nyha_class_4)),
        measurement(lvef, X), X =< 35,
        evidence(non_lbbb),
        measurement(qrs, Y), Y > 120, Y =< 149.

recommendation(crt, 69):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 30,
        evidence(ischemic_hf),
        evidence(sinus_rhythm),
        evidence(lbbb),
        measurement(qrs, Y), Y >= 150,
        evidence(nyha_class_1).

no_benefit(crt, 70):-
        measurement(qrs, X), X < 120.

no_benefit(crt, 71):-
        (evidence(nyha_class_1);evidence(nyha_class_2)),
        evidence(non_lbbb),
        measurement(qrs, X), X < 150.

recommendation(surgical_revascularization, 73):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40,
        measurement(lvef, X), X =< 35.

recommendation(manage_vhd, 74):-
        evidence(accf_stage_c),
        evidence(valvular_hd).

recommendation(gmdt_optimization, 75):-
        evidence(accf_stage_c),
        evidence(secondary_mr),
        measurement(lvef, X), X =< 40.

recommendation(sglt2i, 76):-
        evidence(accf_stage_c),
        measurement(lvef, X), X > 40, X < 50.

recommendation(beta_blockers, 77):-
        evidence(accf_stage_c),
        (evidence(nyha_class_2);evidence(nyha_class_3)),
        measurement(lvef, X), X > 40, X < 50.

recommendation(continue_gdmt, 78):-
        evidence(accf_stage_c),
        evidence(hf_with_improved_ef).
                 
recommendation(medication_titrated, 79):-
        evidence(accf_stage_c),
        measurement(lvef, X), X >= 50,
        evidence(hypertension).

recommendation(sglt2i, 80):-
        evidence(accf_stage_c),
        measurement(lvef, X), X >= 50.

recommendation(af_management, 81):-
        evidence(accf_stage_c),
        measurement(lvef, X), X >= 50.

recommendation(mra, 82):-
        evidence(accf_stage_c),
        measurement(lvef, X), X >= 50.
                 
recommendation(arb, 83):-
        evidence(accf_stage_c),
        measurement(lvef, X), X >= 50,
        infeasible(arni),
        intolerant(acei),
        \+ intolerant(arb).

recommendation(arni, 84):-
        evidence(accf_stage_c),
        measurement(lvef, X), X >= 50,
        \+ infeasible(arni).

no_benefit(nitrates_or_pde_5, 85):-
        evidence(accf_stage_c),
        measurement(lvef, X), X >= 50.

recommendation(tafamidis, 89):-
        evidence(accf_stage_c),
        (evidence(attr_wt);evidence(attr_v)),
        (evidence(nyha_class_1);evidence(nyha_class_2);evidence(nyha_class_3)).

recommendation(anticoagulant, 91):-
        evidence(accf_stage_c),
        (evidence(attr_wt);evidence(attr_v)).


%Stage D
recommendation(fluid_restriction, 93):-
        evidence(accf_stage_d),
        evidence(hyponatremia).

recommendation(durable_lvad_implantation, 97):-
        evidence(accf_stage_c),
        measurement(lvef, X), X =< 40,
        evidence(nyha_class_4),
        (evidence(dependence_of_continuous_iv_inotropes);evidence(dependence_of_temporary_mcs)).

recommendation(durable_mcs, 98):-
        evidence(accf_stage_d),
        measurement(lvef, X), X =< 40,
        evidence(nyha_class_4).

recommendation(temporary_mcs, 100):-
        evidence(accf_stage_d),
        evidence(hemodynamic_compromise_and_shock).


%Hospitalized & Comorbidities
recommendation(iv_loop_diuretics, 110):-
        evidence(hospitalized),
        (evidence(accf_stage_c);evidence(accf_stage_d)),
        evidence(fluid_overload).

recommendation(diuretics_titration, 111):-
        evidence(hospitalized),
        (evidence(accf_stage_c);evidence(accf_stage_d)),
        evidence(congestion).

recommendation(iv_nitroglycerin_or_nitroprusside, 114):-
        evidence(hospitalized),
        evidence(decompensated_hf),
        \+ evidence(hypotension).

recommendation(prophylaxis, 115):-
        evidence(hospitalized),
        (evidence(accf_stage_c);evidence(accf_stage_d)).

recommendation(iv_inotropic_support, 116):-
        evidence(accf_stage_d),
        evidence(cardiogenic_shock).

recommendation(temporary_mcs, 117):-
        evidence(accf_stage_d),
        evidence(cardiogenic_shock),
        evidence(threatend_end_organ_function).

recommendation(multidisciplinary_management, 118):-
        evidence(accf_stage_d),
        evidence(cardiogenic_shock).

recommendation(pulmonary_artery_line, 119):-
        evidence(accf_stage_d),
        evidence(cardiogenic_shock).

recommendation(iv_iron_replacement, 125):-
        measurement(lvef, X), X =< 40,
        (evidence(accf_stage_c);evidence(accf_stage_d)),
        evidence(iron_deficiency).

contraindication(erythropoietin_stimulating_agents, 126):-
        (evidence(accf_stage_c);evidence(accf_stage_d)),
        evidence(anemia).

recommendation(uptitration, 127):-
        measurement(lvef, X), X =< 40,
        (evidence(accf_stage_c);evidence(accf_stage_d)),
        evidence(hypertension).

recommendation(sleep_assesment, 128):-
        (evidence(accf_stage_c);evidence(accf_stage_d)),
        evidence(sleep_disorder_breathing).

recommendation(continuous_positive_airways_pressure, 129):-
        (evidence(accf_stage_c);evidence(accf_stage_d)),
        evidence(obstructive_sleep_apnea).

contraindication(adaptive_servo_ventilation, 130):-
        measurement(lvef, X), X =< 40,
        (evidence(accf_stage_c);evidence(accf_stage_d)),
        (evidence(nyha_class_2);evidence(nyha_class_3);evidence(nyha_class_4)),
        evidence(central_sleep_apnea).

recommendation(sglt2i, 131):-
        (evidence(accf_stage_c);evidence(accf_stage_d)),
        evidence(type_2_diabetes).

recommendation(chronic_anticoagulant_therapy, 132):-
        sex(male),
        evidence(accf_stage_d),
        evidence(permanent_persistent_paroxysmal_af),
        measurement(cha2ds2_vasc, X), X >= 2.

recommendation(chronic_anticoagulant_therapy, 132):-
        sex(female),
        evidence(accf_stage_d),
        evidence(permanent_persistent_paroxysmal_af),
        measurement(cha2ds2_vasc, X), X >= 3.

recommendation(direct_acting_oral_anticoagulants, 133):-
        evidence(accf_stage_d),
        evidence(permanent_persistent_paroxysmal_af).

recommendation(af_ablation, 134):-
        (evidence(accf_stage_c),evidence(accf_stage_d)),
        evidence(atrial_fibrillation).

recommendation(av_node_ablation, 135):-
        (evidence(accf_stage_c);evidence(accf_stage_d)),
        evidence(atrial_fibrillation),
        measurement(lvef, X), X =< 50.

recommendation(crt, 135):-
        (evidence(accf_stage_c);evidence(accf_stage_d)),
        evidence(atrial_fibrillation),
        measurement(lvef, X), X =< 50.

recommendation(chronic_anticoagulant_therapy, 136):-
        evidence(accf_stage_d),
        evidence(permanent_persistent_paroxysmal_af).
