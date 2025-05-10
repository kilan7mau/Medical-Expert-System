% Các luật chẩn đoán bệnh

% Luật cho viêm khớp
rule(arthritis, [
    appetite_loss(yes),
    fever(no),
    short_breath(no),
    fatigue(no),
    joint_pain(yes),
    stiff_joint(yes),
    swell_joint(yes),
    red_skin_around_joint(yes),
    decreased_range(yes),
    tired(yes)
]).

% Luật cho loét dạ dày
rule(peptic_ulcer, [
    appetite_loss(yes),
    fever(no),
    short_breath(no),
    fatigue(no),
    vomit_many(yes),
    burning_stomach(yes),
    bloating(yes),
    mild_nausea(yes),
    weight_loss(yes),
    abdominal_pain(yes)
]).

% Luật cho viêm dạ dày
rule(gastritis, [
    appetite_loss(yes),
    fever(no),
    short_breath(no),
    fatigue(no),
    vomit_normal(yes),
    nausea(yes),
    fullness(yes),
    bloating(yes),
    abdominal_pain(yes),
    indigestion(yes),
    gnawing(yes)
]).

% Luật cho tiểu đường
rule(diabetes, [
    fatigue(yes),
    fever(no),
    short_breath(no),
    extreme_thirst(yes),
    extreme_hunger(yes),
    frequent_urination(yes),
    weight_loss(yes),
    irratabiliry(yes),
    blurred_vision(yes),
    frequent_infections(yes),
    sores(yes)
]).

% Luật cho mất nước
rule(dehydration, [
    fatigue(yes),
    fever(no),
    short_breath(no),
    extreme_thirst(yes),
    dizziness(yes),
    less_frequent_urination(yes),
    dark_urine(yes),
    lethargy(yes),
    dry_mouth(yes)
]).

% Luật cho suy giáp
rule(hypothyroidism, [
    fatigue(yes),
    fever(no),
    short_breath(no),
    muscle_weakness(yes),
    depression(yes),
    constipation(yes),
    feeling_cold(yes),
    dry_skin(yes),
    dry_hair(yes),
    weight_gain(yes),
    decreased_sweating(yes),
    slowed_heartrate(yes),
    pain_joints(yes),
    hoarseness(yes)
]).

% Luật cho béo phì
rule(obesity, [
    short_breath(yes),
    fever(no),
    back_joint_pain(yes),
    sweating(yes),
    snoring(yes),
    sudden_physical(yes),
    tired(yes),
    isolated(yes),
    confidence(yes)
]).

% Luật cho thiếu máu
rule(anemia, [
    short_breath(yes),
    fever(no),
    chest_pain(yes),
    fatigue(yes),
    headache(yes),
    irregular_heartbeat(yes),
    weakness(yes),
    pale_skin(yes),
    lightheadedness(yes),
    cold_hands_feet(yes)
]).

% Luật cho xơ vữa động mạch vành
rule(cad, [
    short_breath(yes),
    fever(no),
    chest_pain(yes),
    fatigue(yes),
    pain_arms(yes),
    heaviness(yes),
    sweating(yes),
    dizziness(yes),
    burning(yes)
]).

% Luật cho hen suyễn
rule(asthma, [
    short_breath(yes),
    fever(no),
    chest_pain(yes),
    cough(yes),
    wheezing(yes),
    sleep_trouble(yes)
]).

% Luật cho sốt xuất huyết
rule(dengue, [
    fever_high(yes),
    headache(yes),
    eyes_pain(yes),
    muscle_pain(yes),
    joint_pain(yes),
    nausea(yes),
    rashes(yes),
    bleeding(yes)
]).

% Luật cho viêm phế quản
rule(bronchitis, [
    fever_mild(yes),
    cough(yes),
    wheezing(yes),
    chills(yes),
    chest_tightness(yes),
    sore_throat(yes),
    body_aches(yes),
    breathlessness(yes),
    headache(yes),
    nose_blocked(yes)
]).

% Luật cho viêm kết mạc
rule(conjunctivitis, [
    red_eyes(yes),
    eye_burn(yes),
    eye_crusting(yes)
]).

% Luật cho dị ứng mắt
rule(eye_allergy, [
    red_eyes(yes),
    eye_irritation(yes)
]).

% Luật cho bệnh lao
rule(tb, [
    fever_normal(yes),
    chest_pain(yes),
    fatigue(yes),
    chills(yes),
    persistent_cough(yes),
    weight_loss(yes),
    night_sweats(yes),
    cough_blood(yes)
]).

% Luật cho cúm
rule(influenza, [
    fever_normal(yes),
    fatigue(yes),
    sore_throat(yes),
    weakness(yes),
    dry_cough(yes),
    muscle_ache(yes),
    chills(yes),
    nasal_congestion(yes),
    headache(yes)
]).

% Luật cho viêm gan
rule(hepatitis, [
    fever_normal(yes),
    fatigue(yes),
    abdominal_pain(yes),
    flu_like(yes),
    dark_urine(yes),
    pale_stool(yes),
    weight_loss(yes),
    jaundice(yes)
]).

% Luật cho viêm phổi
rule(pneumonia, [
    fever_normal(yes),
    chest_pain(yes),
    short_breath(yes),
    nausea(yes),
    short_breath_severe(yes),
    sweat(yes),
    rapid_breath(yes),
    cough(yes),
    diarrhea(yes)
]).

% Luật cho sốt rét
rule(malaria, [
    fever_normal(yes),
    chills(yes),
    abdominal_pain(yes),
    nausea(yes),
    headache(yes),
    sweat(yes),
    cough(yes),
    weakness(yes),
    muscle_pain(yes),
    back_pain(yes)
]).

% Luật cho AIDS
rule(hiv, [
    fever_normal(yes),
    rashes(yes),
    headache(yes),
    muscle_ache(yes),
    sore_throat(yes),
    lymph(yes),
    diarrhea(yes),
    cough(yes),
    weight_loss(yes),
    night_sweats(yes)
]).

% Luật cho viêm tụy
rule(pancreatitis, [
    fever_normal(yes),
    nausea(yes),
    upper_abdominal_pain(yes),
    abdominal_eat(yes),
    heartbeat(yes),
    weight_loss(yes),
    oily_stool(yes)
]).

% Luật cho COVID-19
rule(corona, [
    fever_normal(yes),
    fatigue(yes),
    short_breath(yes),
    nausea(yes),
    chills(yes),
    cough(yes),
    body_aches(yes),
    headache(yes),
    sore_throat(yes),
    lose_smell(yes),
    diarrhea(yes)
]). 