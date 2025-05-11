% Hệ thống chuyên gia y tế
% Chuyển đổi từ Python experta sang Prolog

% Khai báo động
:- dynamic fact/1.
:- dynamic symptom/2.
:- dynamic disease/2.

% Hàm chính để khởi động hệ thống
start :-
    write('Xin chào. Tôi là Hệ thống Chuyên gia có thể giúp bạn chẩn đoán bệnh.'), nl,
    write('Khi được hiển thị các lựa chọn, hãy nhập các số nguyên cách nhau bởi dấu cách tương ứng với tất cả các lựa chọn áp dụng cho bạn.'), nl,
    write('Vui lòng trả lời các câu hỏi sau để tìm ra bệnh và cách chữa trị'), nl,
    get_user_info,
    ask_basic_questions,
    analyze_symptoms,
    suggest_diseases.

% Thu thập thông tin cơ bản của người dùng
get_user_info :-
    write('Tên của bạn là gì? : '),
    read(Name),
    assert(fact(name(Name))),
    write('Giới tính của bạn là gì? (nam/nữ) : '),
    read(Gender),
    assert(fact(gender(Gender))).

% Thu thập các triệu chứng cơ bản
ask_basic_questions :-
    ask_yes_no('Bạn có bị đỏ mắt không?', red_eyes),
    ask_yes_no('Bạn có cảm thấy mệt mỏi không?', fatigue),
    ask_yes_no('Bạn có khó thở không?', short_breath),
    ask_yes_no('Bạn có bị mất cảm giác thèm ăn không?', appetite_loss),
    ask_fever.

% Hỏi về tình trạng sốt
ask_fever :-
    write('Bạn có bị sốt không? (1: Sốt Thường, 2: Sốt Nhẹ, 3: Sốt Cao, 0: Không có)'), nl,
    write('Nhập lựa chọn của bạn: '),
    read(FeverChoice),
    process_fever(FeverChoice).

% Xử lý các loại sốt
process_fever(0) :-
    assert(symptom(fever, no)).
process_fever(1) :-
    assert(symptom(fever, yes)),
    assert(symptom(fever_normal, yes)).
process_fever(2) :-
    assert(symptom(fever, yes)),
    assert(symptom(fever_mild, yes)).
process_fever(3) :-
    assert(symptom(fever, yes)),
    assert(symptom(fever_high, yes)).

% Phân tích triệu chứng và đặt thêm câu hỏi dựa vào đó
analyze_symptoms :-
    check_appetite_loss,
    check_fatigue,
    check_short_breath,
    check_red_eyes,
    check_fever.

% Kiểm tra và hỏi thêm về mất cảm giác thèm ăn
check_appetite_loss :-
    symptom(appetite_loss, yes),
    symptom(fever, no),
    symptom(short_breath, no),
    symptom(fatigue, no),
    !,
    ask_yes_no('Bạn có đau khớp không?', joint_pain),
    ask_vomit.
check_appetite_loss.

% Hỏi về tình trạng nôn
ask_vomit :-
    write('Bạn có bị nôn không? (1: Nôn Nhiều, 2: Nôn Thường, 0: Không có)'), nl,
    write('Nhập lựa chọn của bạn: '),
    read(VomitChoice),
    process_vomit(VomitChoice).

% Xử lý các loại nôn
process_vomit(0) :-
    assert(symptom(vomit, no)).
process_vomit(1) :-
    assert(symptom(vomit, yes)),
    assert(symptom(vomit_severe, yes)).
process_vomit(2) :-
    assert(symptom(vomit, yes)),
    assert(symptom(vomit_normal, yes)).

% Kiểm tra và hỏi thêm nếu có triệu chứng viêm khớp
check_arthritis :-
    symptom(appetite_loss, yes),
    symptom(fever, no),
    symptom(short_breath, no),
    symptom(fatigue, no),
    symptom(joint_pain, yes),
    !,
    ask_yes_no('Bạn có bị cứng khớp không?', stiff_joint),
    ask_yes_no('Bạn có bị sưng khớp không?', swell_joint),
    ask_yes_no('Da quanh khớp có chuyển sang màu đỏ không?', red_skin_around_joint),
    ask_yes_no('Phạm vi cử động ở các khớp có giảm không?', decreased_range),
    ask_yes_no('Bạn có cảm thấy mệt mỏi ngay cả khi đi bộ quãng đường ngắn không?', tired).
check_arthritis.

% Kiểm tra và hỏi thêm về mệt mỏi
check_fatigue :-
    symptom(fatigue, yes),
    symptom(fever, no),
    symptom(short_breath, no),
    !,
    ask_yes_no('Bạn có cảm thấy khát nước nhiều hơn bình thường không?', extreme_thirst),
    ask_yes_no('Bạn có cảm thấy đói nhiều hơn bình thường không?', extreme_hunger),
    ask_yes_no('Bạn có cảm thấy chóng mặt không?', dizziness),
    ask_yes_no('Cơ bắp của bạn có yếu hơn trước không?', muscle_weakness).
check_fatigue.

% Kiểm tra và hỏi thêm về khó thở
check_short_breath :-
    symptom(short_breath, yes),
    symptom(fever, no),
    !,
    ask_yes_no('Bạn có đau lưng và đau khớp không?', back_joint_pain),
    ask_yes_no('Bạn có đau ngực không?', chest_pain),
    ask_yes_no('Bạn có ho thường xuyên không?', cough),
    ask_yes_no('Bạn có cảm thấy mệt mỏi không?', fatigue),
    ask_yes_no('Bạn có bị đau đầu không?', headache),
    ask_yes_no('Bạn có đau ở cánh tay và vai không?', pain_arms).
check_short_breath.

% Kiểm tra và hỏi thêm về đỏ mắt
check_red_eyes :-
    symptom(red_eyes, yes),
    !,
    ask_yes_no('Bạn có cảm giác nóng rát ở mắt không?', eye_burn),
    ask_yes_no('Bạn có bị chảy mủ hoặc đóng vảy ở mắt không?', eye_crusting),
    ask_yes_no('Bạn có bị kích ứng mắt không?', eye_irritation).
check_red_eyes.

% Kiểm tra và hỏi thêm về sốt
check_fever :-
    symptom(fever_normal, yes),
    !,
    ask_yes_no('Bạn có bị đau ngực không?', chest_pain),
    ask_yes_no('Bạn có bị đau bụng không?', abdominal_pain),
    ask_yes_no('Bạn có bị đau họng không?', sore_throat),
    ask_yes_no('Bạn có bị rùng mình ớn lạnh không?', chills),
    ask_yes_no('Bạn có bị phát ban trên da không?', rashes),
    ask_yes_no('Bạn có nôn hoặc cảm thấy buồn nôn không?', nausea).
check_fever :-
    symptom(fever_high, yes),
    !,
    ask_dengue.
check_fever :-
    symptom(fever_mild, yes),
    !,
    ask_bronchitis.
check_fever.

% Hỏi về sốt xuất huyết
ask_dengue :-
    ask_yes_no('Bạn có đau đầu dữ dội không?', headache),
    ask_yes_no('Bạn có đau sau mắt không?', eyes_pain),
    ask_yes_no('Bạn có đau cơ dữ dội không?', muscle_pain),
    ask_yes_no('Bạn có đau khớp dữ dội không?', joint_pain),
    ask_yes_no('Bạn có nôn hoặc cảm thấy buồn nôn không?', nausea),
    ask_yes_no('Bạn có bị phát ban trên da xuất hiện từ hai đến năm ngày sau khi bắt đầu sốt không?', rashes),
    ask_yes_no('Bạn có bị chảy máu nhẹ như chảy máu mũi, chảy máu nướu răng, hoặc dễ bị bầm tím không?', bleeding).

% Hỏi về viêm phế quản
ask_bronchitis :-
    ask_yes_no('Bạn có ho dai dẳng, có thể tạo ra đờm màu vàng xám không?', cough),
    ask_yes_no('Bạn có bị thở khò khè không?', wheezing),
    ask_yes_no('Bạn có cảm thấy ớn lạnh không?', chills),
    ask_yes_no('Bạn có cảm giác thắt ngực không?', chest_tightness),
    ask_yes_no('Bạn có đau họng không?', sore_throat),
    ask_yes_no('Bạn có đau nhức cơ thể không?', body_aches),
    ask_yes_no('Bạn có cảm thấy khó thở không?', breathlessness),
    ask_yes_no('Bạn có đau đầu không?', headache),
    ask_yes_no('Bạn có bị nghẹt mũi hoặc xoang không?', nose_blocked).

% Hàm để đề xuất các bệnh dựa trên triệu chứng
suggest_diseases :-
    check_conjunctivitis,
    check_eye_allergy,
    check_arthritis_disease,
    check_peptic_ulcer,
    check_gastritis,
    check_diabetes,
    check_dehydration,
    check_hypothyroidism,
    check_obesity,
    check_anemia,
    check_cad,
    check_asthma,
    check_dengue_disease,
    check_bronchitis_disease,
    check_tb,
    check_influenza,
    check_hepatitis,
    check_pneumonia,
    check_malaria,
    check_hiv,
    check_pancreatitis,
    check_corona.

% Kiểm tra và đề xuất bệnh viêm kết mạc
check_conjunctivitis :-
    (symptom(eye_crusting, yes); symptom(eye_burn, yes)),
    !,
    add_disease('Viêm Kết Mạc', ['Cảm giác nóng rát ở mắt', 'Đóng vảy ở mắt', 'Đỏ mắt']).
check_conjunctivitis.

% Kiểm tra và đề xuất bệnh dị ứng mắt
check_eye_allergy :-
    symptom(eye_irritation, yes),
    !,
    add_disease('Dị Ứng Mắt', ['Kích ứng mắt', 'Đỏ mắt']).
check_eye_allergy.

% Kiểm tra và đề xuất bệnh viêm khớp
check_arthritis_disease :-
    count_symptoms([stiff_joint, swell_joint, red_skin_around_joint, decreased_range, tired], Count),
    Count >= 3,
    !,
    add_disease('Viêm Khớp', ['Cứng khớp', 'Sưng khớp', 'Đau khớp', 'Da đỏ quanh khớp', 'Mệt mỏi',
                             'Giảm khả năng cử động ở khớp', 'Mất cảm giác thèm ăn']).
check_arthritis_disease.

% Kiểm tra và đề xuất bệnh loét dạ dày
check_peptic_ulcer :-
    symptom(appetite_loss, yes),
    symptom(fever, no),
    symptom(short_breath, no),
    symptom(fatigue, no),
    symptom(vomit_severe, yes),
    !,
    ask_yes_no('Dạ dày của bạn có cảm giác nóng rát không?', burning_stomach),
    ask_yes_no('Bạn có cảm giác đầy hơi, chướng bụng hoặc ợ hơi không?', bloating),
    ask_yes_no('Bạn có buồn nôn nhẹ không?', mild_nausea),
    ask_yes_no('Bạn có bị sụt cân không?', weight_loss),
    ask_yes_no('Bạn có đau bụng dữ dội và tập trung ở một vùng không?', abdominal_pain),
    count_symptoms([burning_stomach, bloating, mild_nausea, weight_loss, abdominal_pain], Count),
    (Count >= 3 ->
        add_disease('Loét Dạ Dày', ['Mất cảm giác thèm ăn', 'Nôn nhiều', 'Cảm giác nóng rát ở dạ dày', 
                                   'Đầy hơi dạ dày', 'Buồn nôn', 'Sụt cân', 'Đau bụng']);
        true).
check_peptic_ulcer.

% Kiểm tra và đề xuất bệnh viêm dạ dày
check_gastritis :-
    symptom(appetite_loss, yes),
    symptom(fever, no),
    symptom(short_breath, no),
    symptom(fatigue, no),
    symptom(vomit_normal, yes),
    !,
    ask_yes_no('Bạn có cảm giác buồn nôn không?', nausea),
    ask_yes_no('Bạn có cảm giác đầy ở vùng bụng trên không?', fullness),
    ask_yes_no('Bạn có cảm thấy chướng bụng không?', bloating),
    ask_yes_no('Bạn có đau gần vùng bụng không?', abdominal_pain),
    ask_yes_no('Bạn có gặp vấn đề về tiêu hóa không?', indigestion),
    ask_yes_no('Bạn có cảm giác đau âm ỉ hoặc nóng rát ở bụng trên mà có thể trở nên tốt hơn hoặc tồi tệ hơn khi ăn không?', gnawing),
    count_symptoms([nausea, fullness, bloating, abdominal_pain, indigestion, gnawing], Count),
    (Count >= 4 ->
        add_disease('Viêm Dạ Dày', ['Mất cảm giác thèm ăn', 'Nôn', 'Buồn nôn', 'Cảm giác đầy ở vùng bụng', 
                                   'Chướng bụng', 'Đau bụng', 'Khó tiêu', 'Đau âm ỉ ở vùng bụng']);
        true).
check_gastritis.

% Kiểm tra và đề xuất bệnh tiểu đường
check_diabetes :-
    symptom(fatigue, yes),
    symptom(fever, no),
    symptom(short_breath, no),
    symptom(extreme_thirst, yes),
    symptom(extreme_hunger, yes),
    !,
    ask_yes_no('Bạn có đi tiểu thường xuyên hơn trước không?', frequent_urination),
    ask_yes_no('Bạn có bị sụt cân không chủ ý không?', weight_loss),
    ask_yes_no('Bạn có dễ cáu gắt hơn gần đây không?', irritability),
    ask_yes_no('Thị lực của bạn có bị mờ không?', blurred_vision),
    ask_yes_no('Bạn có bị nhiễm trùng thường xuyên như nhiễm trùng nướu răng hoặc da không?', frequent_infections),
    ask_yes_no('Các vết thương của bạn có lâu lành không?', sores),
    count_symptoms([frequent_urination, weight_loss, irritability, blurred_vision, frequent_infections, sores], Count),
    (Count >= 4 ->
        add_disease('Tiểu Đường', ['Mệt mỏi', 'Khát nước nhiều', 'Đói nhiều', 'Sụt cân', 'Thị lực mờ', 
                                  'Nhiễm trùng thường xuyên', 'Đi tiểu thường xuyên', 'Dễ cáu gắt', 'Vết thương lâu lành']);
        true).
check_diabetes.

% Kiểm tra và đề xuất bệnh mất nước
check_dehydration :-
    symptom(fatigue, yes),
    symptom(fever, no),
    symptom(short_breath, no),
    symptom(extreme_thirst, yes),
    symptom(dizziness, yes),
    !,
    ask_yes_no('Bạn có đi tiểu ít hơn bình thường không?', less_frequent_urination),
    ask_yes_no('Nước tiểu của bạn có bị sẫm màu không?', dark_urine),
    ask_yes_no('Bạn có cảm thấy uể oải không?', lethargy),
    ask_yes_no('Miệng của bạn có khô đáng kể không?', dry_mouth),
    count_symptoms([less_frequent_urination, dark_urine, lethargy, dry_mouth], Count),
    (Count >= 2 ->
        add_disease('Mất Nước', ['Mệt mỏi', 'Khát nước nhiều', 'Chóng mặt', 'Nước tiểu sẫm màu', 
                               'Cảm giác uể oải', 'Khô miệng', 'Đi tiểu ít hơn']);
        true).
check_dehydration.

% Kiểm tra và đề xuất bệnh suy giáp
check_hypothyroidism :-
    symptom(fatigue, yes),
    symptom(fever, no),
    symptom(short_breath, no),
    symptom(muscle_weakness, yes),
    !,
    ask_yes_no('Bạn có cảm thấy trầm cảm gần đây không?', depression),
    ask_yes_no('Bạn có bị táo bón không?', constipation),
    ask_yes_no('Bạn có cảm thấy lạnh không?', feeling_cold),
    ask_yes_no('Da của bạn có trở nên khô hơn không?', dry_skin),
    ask_yes_no('Tóc của bạn có trở nên khô và mỏng hơn không?', dry_hair),
    ask_yes_no('Bạn có tăng cân đáng kể không?', weight_gain),
    ask_yes_no('Bạn có đổ mồ hôi ít hơn trước không?', decreased_sweating),
    ask_yes_no('Nhịp tim của bạn có chậm lại không?', slowed_heartrate),
    ask_yes_no('Bạn có cảm thấy đau và cứng ở các khớp không?', pain_joints),
    ask_yes_no('Giọng của bạn có thay đổi bất thường không?', hoarseness),
    count_symptoms([depression, constipation, feeling_cold, dry_skin, dry_hair, weight_gain, 
                  decreased_sweating, slowed_heartrate, pain_joints, hoarseness], Count),
    (Count >= 7 ->
        add_disease('Suy Giáp', ['Mệt mỏi', 'Cơ bắp yếu', 'Trầm cảm', 'Táo bón', 'Cảm giác lạnh', 
                              'Da khô', 'Tóc khô', 'Tăng cân', 'Đổ mồ hôi giảm', 
                              'Nhịp tim chậm', 'Đau khớp', 'Khàn giọng']);
        true).
check_hypothyroidism.

% Kiểm tra và đề xuất bệnh béo phì
check_obesity :-
    symptom(short_breath, yes),
    symptom(fever, no),
    symptom(back_joint_pain, yes),
    !,
    ask_yes_no('Bạn có đổ mồ hôi nhiều hơn bình thường không?', sweating),
    ask_yes_no('Bạn có phát triển thói quen ngáy không?', snoring),
    ask_yes_no('Bạn có khó đối phó với hoạt động thể chất đột ngột không?', sudden_physical),
    ask_yes_no('Bạn có cảm thấy mệt mỏi mỗi ngày mà không cần làm việc nhiều không?', tired),
    ask_yes_no('Bạn có cảm thấy bị cô lập không?', isolated),
    ask_yes_no('Bạn có cảm thấy thiếu tự tin và lòng tự trọng thấp trong các hoạt động hàng ngày không?', confidence),
    count_symptoms([sweating, snoring, sudden_physical, tired, isolated, confidence], Count),
    (Count >= 4 ->
        add_disease('Béo Phì', ['Khó thở', 'Đau lưng và khớp', 'Đổ mồ hôi nhiều', 
                              'Thói quen ngáy', 'Mệt mỏi', 'Thiếu tự tin']);
        true).
check_obesity.

% Kiểm tra và đề xuất bệnh thiếu máu
check_anemia :-
    symptom(short_breath, yes),
    symptom(fever, no),
    symptom(chest_pain, yes),
    symptom(fatigue, yes),
    symptom(headache, yes),
    !,
    ask_yes_no('Bạn có nhịp tim không đều không?', irregular_heartbeat),
    ask_yes_no('Bạn có cảm thấy yếu không?', weakness),
    ask_yes_no('Da của bạn có chuyển sang màu nhợt nhạt hoặc hơi vàng không?', pale_skin),
    ask_yes_no('Bạn có bị chóng mặt hoặc cảm giác choáng váng không?', lightheadedness),
    ask_yes_no('Bạn có bị lạnh tay và chân không?', cold_hands_feet),
    count_symptoms([irregular_heartbeat, weakness, pale_skin, lightheadedness, cold_hands_feet], Count),
    (Count >= 3 ->
        add_disease('Thiếu Máu', ['Khó thở', 'Đau ngực', 'Mệt mỏi', 'Đau đầu', 'Nhịp tim không đều', 
                                'Yếu ớt', 'Da nhợt nhạt', 'Chóng mặt', 'Tay chân lạnh']);
        true).
check_anemia.

% Kiểm tra và đề xuất bệnh xơ vữa động mạch vành
check_cad :-
    symptom(short_breath, yes),
    symptom(fever, no),
    symptom(chest_pain, yes),
    symptom(fatigue, yes),
    symptom(pain_arms, yes),
    !,
    ask_yes_no('Bạn có cảm giác nặng nề hoặc thắt ngực, thường ở vùng trung tâm của ngực, có thể lan ra cánh tay, cổ, hàm, lưng hoặc dạ dày không?', heaviness),
    ask_yes_no('Bạn có đổ mồ hôi thường xuyên không?', sweating),
    ask_yes_no('Bạn có cảm thấy chóng mặt không?', dizziness),
    ask_yes_no('Bạn có cảm giác nóng rát gần tim không?', burning),
    count_symptoms([heaviness, sweating, dizziness, burning], Count),
    (Count >= 2 ->
        add_disease('Xơ Vữa Động Mạch Vành', ['Khó thở', 'Đau ngực', 'Mệt mỏi', 'Đau cánh tay', 
                                           'Cảm giác nặng nề', 'Đổ mồ hôi', 'Chóng mặt', 'Cảm giác nóng rát gần tim']);
        true).
check_cad.

% Kiểm tra và đề xuất bệnh hen suyễn
check_asthma :-
    symptom(short_breath, yes),
    symptom(fever, no),
    symptom(chest_pain, yes),
    symptom(cough, yes),
    !,
    ask_yes_no('Bạn có âm thanh thở khò khè khi thở ra không?', wheezing),
    ask_yes_no('Bạn có khó ngủ do khó thở, ho hoặc thở khò khè không?', sleep_trouble),
    count_symptoms([wheezing, sleep_trouble], Count),
    (Count >= 1 ->
        add_disease('Hen Suyễn', ['Khó thở', 'Đau ngực', 'Ho', 'Thở khò khè khi thở ra', 
                                'Khó ngủ do ho hoặc thở khò khè']);
        true).
check_asthma.

% Kiểm tra và đề xuất bệnh sốt xuất huyết
check_dengue_disease :-
    symptom(fever_high, yes),
    count_symptoms([headache, eyes_pain, muscle_pain, joint_pain, nausea, rashes, bleeding], Count),
    (Count >= 5 ->
        add_disease('Sốt Xuất Huyết', ['Sốt cao', 'Đau đầu', 'Đau mắt', 'Đau cơ', 
                                     'Đau khớp', 'Buồn nôn', 'Phát ban', 'Chảy máu']);
        true).
check_dengue_disease.

% Kiểm tra và đề xuất bệnh viêm phế quản
check_bronchitis_disease :-
    symptom(fever_mild, yes),
    count_symptoms([cough, wheezing, chills, chest_tightness, sore_throat, body_aches, breathlessness, headache, nose_blocked], Count),
    (Count >= 7 ->
        add_disease('Viêm Phế Quản', ['Sốt nhẹ', 'Ho', 'Thở khò khè', 'Ớn lạnh', 'Thắt ngực', 
                                    'Đau họng', 'Đau nhức cơ thể', 'Đau đầu', 'Khó thở', 'Nghẹt mũi']);
        true).
check_bronchitis_disease.

% Kiểm tra và đề xuất bệnh lao
check_tb :-
    symptom(fever_normal, yes),
    symptom(chest_pain, yes),
    symptom(fatigue, yes),
    symptom(chills, yes),
    !,
    ask_yes_no('Bạn có bị ho dai dẳng kéo dài hơn 2 đến 3 tuần không?', persistent_cough),
    ask_yes_no('Bạn có bị sụt cân không chủ ý không?', weight_loss),
    ask_yes_no('Bạn có bị đổ mồ hôi đêm không?', night_sweats),
    ask_yes_no('Bạn có ho ra máu không?', cough_blood),
    count_symptoms([persistent_cough, weight_loss, night_sweats, cough_blood], Count),
    (Count >= 2 ->
        add_disease('Bệnh Lao', ['Sốt', 'Đau ngực', 'Mệt mỏi', 'Mất cảm giác thèm ăn', 'Ho dai dẳng']);
        true).
check_tb.

% Kiểm tra và đề xuất bệnh cúm
check_influenza :-
    symptom(fever_normal, yes),
    symptom(fatigue, yes),
    symptom(sore_throat, yes),
    !,
    ask_yes_no('Bạn có cảm thấy yếu ớt không?', weakness),
    ask_yes_no('Bạn có bị ho khan dai dẳng không?', dry_cough),
    ask_yes_no('Bạn có đau nhức cơ, đặc biệt là ở lưng, cánh tay và chân không?', muscle_ache),
    ask_yes_no('Bạn có bị đổ mồ hôi cùng với ớn lạnh không?', chills_sweats),
    ask_yes_no('Bạn có bị nghẹt mũi không?', nasal_congestion),
    ask_yes_no('Bạn có bị đau đầu không?', headache),
    count_symptoms([weakness, dry_cough, muscle_ache, chills_sweats, nasal_congestion, headache], Count),
    (Count >= 4 ->
        add_disease('Cúm', ['Sốt', 'Mệt mỏi', 'Đau họng', 'Yếu ớt', 'Ho khan', 'Đau nhức cơ', 
                          'Ớn lạnh', 'Nghẹt mũi', 'Đau đầu']);
        true).
check_influenza.

% Kiểm tra và đề xuất bệnh viêm gan
check_hepatitis :-
    symptom(fever_normal, yes),
    symptom(fatigue, yes),
    symptom(abdominal_pain, yes),
    !,
    ask_yes_no('Bạn có triệu chứng giống như cúm không?', flu_like),
    ask_yes_no('Nước tiểu của bạn có sẫm màu không?', dark_urine),
    ask_yes_no('Bạn có phân nhạt màu không?', pale_stool),
    ask_yes_no('Bạn có bị sụt cân không chủ ý không?', weight_loss),
    ask_yes_no('Da và mắt của bạn có chuyển sang màu vàng không?', jaundice),
    count_symptoms([flu_like, dark_urine, pale_stool, weight_loss, jaundice], Count),
    (Count >= 3 ->
        add_disease('Viêm Gan', ['Sốt', 'Mệt mỏi', 'Đau bụng', 'Triệu chứng giống cúm', 'Nước tiểu sẫm màu', 
                              'Phân nhạt màu', 'Sụt cân', 'Da và mắt vàng (Vàng da)']);
        true).
check_hepatitis.

% Kiểm tra và đề xuất bệnh viêm phổi
check_pneumonia :-
    symptom(fever_normal, yes),
    symptom(chest_pain, yes),
    symptom(short_breath, yes),
    symptom(nausea, yes),
    !,
    ask_yes_no('Bạn có cảm thấy khó thở khi làm các hoạt động bình thường hoặc thậm chí khi nghỉ ngơi không?', severe_short_breath),
    ask_yes_no('Bạn có bị đổ mồ hôi cùng với ớn lạnh không?', sweat),
    ask_yes_no('Bạn có thở nhanh không?', rapid_breath),
    ask_yes_no('Bạn có ho ngày càng nặng hơn có thể tạo ra đờm màu vàng/xanh hoặc có máu không?', cough_phlegm),
    ask_yes_no('Bạn có bị tiêu chảy không?', diarrhea),
    count_symptoms([severe_short_breath, sweat, rapid_breath, cough_phlegm, diarrhea], Count),
    (Count >= 3 ->
        add_disease('Viêm Phổi', ['Sốt', 'Đau ngực', 'Khó thở', 'Buồn nôn', 'Đổ mồ hôi kèm ớn lạnh', 
                               'Thở nhanh', 'Ho có đờm', 'Tiêu chảy']);
        true).
check_pneumonia.

% Kiểm tra và đề xuất bệnh sốt rét
check_malaria :-
    symptom(fever_normal, yes),
    symptom(chills, yes),
    symptom(abdominal_pain, yes),
    symptom(nausea, yes),
    !,
    ask_yes_no('Bạn có bị đau đầu không?', headache),
    ask_yes_no('Bạn có đổ mồ hôi thường xuyên không?', sweat),
    ask_yes_no('Bạn có ho thường xuyên không?', cough),
    ask_yes_no('Bạn có cảm thấy yếu ớt không?', weakness),
    ask_yes_no('Bạn có đau nhức cơ dữ dội không?', muscle_pain),
    ask_yes_no('Bạn có đau lưng dưới không?', back_pain),
    count_symptoms([headache, sweat, weakness, cough, muscle_pain, back_pain], Count),
    (Count >= 4 ->
        add_disease('Sốt Rét', ['Sốt', 'Ớn lạnh', 'Đau bụng', 'Buồn nôn', 'Đau đầu', 'Đổ mồ hôi', 
                              'Ho', 'Yếu ớt', 'Đau nhức cơ', 'Đau lưng']);
        true).
check_malaria.

% Kiểm tra và đề xuất bệnh HIV/AIDS
check_hiv :-
    symptom(fever_normal, yes),
    symptom(rashes, yes),
    !,
    ask_yes_no('Bạn có bị đau đầu không?', headache),
    ask_yes_no('Bạn có bị đau nhức cơ và đau khớp không?', muscle_ache),
    ask_yes_no('Bạn có bị đau họng và lở loét miệng đau không?', sore_throat),
    ask_yes_no('Bạn có bị sưng hạch bạch huyết, đặc biệt là ở cổ không?', lymph),
    ask_yes_no('Bạn có bị tiêu chảy không?', diarrhea),
    ask_yes_no('Bạn có ho thường xuyên không?', cough),
    ask_yes_no('Bạn có bị sụt cân không chủ ý không?', weight_loss),
    ask_yes_no('Bạn có bị đổ mồ hôi đêm không?', night_sweats),
    count_symptoms([headache, muscle_ache, sore_throat, lymph, diarrhea, cough, weight_loss, night_sweats], Count),
    (Count >= 6 ->
        add_disease('AIDS', ['Sốt', 'Phát ban', 'Đau đầu', 'Đau nhức cơ', 'Đau họng', 'Sưng hạch bạch huyết', 
                           'Tiêu chảy', 'Ho', 'Sụt cân', 'Đổ mồ hôi đêm']);
        true).
check_hiv.

% Kiểm tra và đề xuất bệnh viêm tụy
check_pancreatitis :-
    symptom(fever_normal, yes),
    symptom(nausea, yes),
    !,
    ask_yes_no('Bạn có bị đau bụng trên không?', upper_abdominal_pain),
    ask_yes_no('Cơn đau bụng có trở nên tồi tệ hơn sau khi ăn không?', abdominal_eat),
    ask_yes_no('Nhịp tim của bạn có cao hơn bình thường không?', heartbeat),
    ask_yes_no('Bạn có bị sụt cân không chủ ý không?', weight_loss),
    ask_yes_no('Bạn có phân nhờn và có mùi khó chịu không?', oily_stool),
    count_symptoms([upper_abdominal_pain, abdominal_eat, heartbeat, weight_loss, oily_stool], Count),
    (Count >= 3 ->
        add_disease('Viêm Tụy', ['Buồn nôn', 'Sốt', 'Đau bụng trên', 'Nhịp tim cao', 'Sụt cân', 'Phân nhờn và có mùi']);
        true).
check_pancreatitis.

% Kiểm tra và đề xuất bệnh COVID-19
check_corona :-
    symptom(fever_normal, yes),
    symptom(fatigue, yes),
    symptom(short_breath, yes),
    symptom(nausea, yes),
    !,
    ask_yes_no('Bạn có bị ớn lạnh đôi khi kèm theo rùng mình không?', chills),
    ask_yes_no('Bạn có ho thường xuyên không?', cough),
    ask_yes_no('Bạn có bị đau nhức cơ thể không?', body_aches),
    ask_yes_no('Bạn có bị đau đầu không?', headache),
    ask_yes_no('Bạn có bị đau họng và lở loét miệng đau không?', sore_throat),
    ask_yes_no('Bạn có bị mất vị giác và khứu giác đáng kể không?', lose_smell),
    ask_yes_no('Bạn có bị tiêu chảy không?', diarrhea),
    count_symptoms([chills, body_aches, headache, sore_throat, lose_smell, diarrhea], Count),
    (Count >= 4 ->
        add_disease('Vi-rút Corona', ['Sốt', 'Mệt mỏi', 'Khó thở', 'Buồn nôn', 'Ớn lạnh', 'Ho', 
                                    'Đau nhức cơ thể', 'Đau đầu', 'Đau họng', 'Tiêu chảy', 'Mất vị giác/khứu giác']);
        true).
check_corona.

% Thêm bệnh và triệu chứng của nó vào cơ sở dữ liệu
add_disease(Disease, Symptoms) :-
    assert(disease(Disease, Symptoms)),
    format('~n~n--------- CHẨN ĐOÁN BỆNH ---------~n'),
    format('Dựa trên các triệu chứng của bạn, có thể bạn đang bị ~w.~n', [Disease]),
    format('Triệu chứng chính của bệnh này bao gồm:~n'),
    print_symptoms(Symptoms),
    suggest_doctor(Disease).

% In danh sách triệu chứng
print_symptoms([]).
print_symptoms([H|T]) :-
    format('- ~w~n', [H]),
    print_symptoms(T).

% Gợi ý bác sĩ dựa trên bệnh
suggest_doctor(Disease) :-
    format('~nBạn nên đến gặp bác sĩ chuyên khoa để kiểm tra và điều trị.~n'),
    ask_yes_no('Bạn có muốn tìm hiểu thêm về bệnh này không?', more_info),
    (symptom(more_info, yes) -> web_search(Disease); true).

% Hàm để tìm kiếm thông tin trên web
web_search(Disease) :-
    format('~nĐang tìm kiếm thông tin về ~w...~n', [Disease]),
    format('Hãy truy cập vào các trang web y tế uy tín để biết thêm thông tin.~n').

% Hàm tiện ích để hỏi câu hỏi yes/no
ask_yes_no(Question, Symptom) :-
    format('~w (có/không): ', [Question]),
    read(Answer),
    (Answer = có -> 
        assert(symptom(Symptom, yes));
        assert(symptom(Symptom, no))
    ).

% Đếm số lượng triệu chứng có giá trị "yes"
count_symptoms([], 0).
count_symptoms([H|T], Count) :-
    count_symptoms(T, TempCount),
    (symptom(H, yes) -> Count is TempCount + 1; Count = TempCount).

% Hàm chính để khởi động hệ thống
:- initialization(start). 