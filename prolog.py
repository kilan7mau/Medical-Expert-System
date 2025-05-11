import webbrowser
from experta import *
from utils import yes_no, multi_input, suggest_disease

class HeThongChuanDoanYTe(KnowledgeEngine):

    @DefFacts()
    def _initial_action_(self):
        print("Xin chào. Tôi là Hệ thống Chuyên gia có thể giúp bạn chẩn đoán bệnh.")
        print(
            "Khi được hiển thị các lựa chọn, hãy nhập các số nguyên cách nhau bởi dấu cách tương ứng với tất cả các lựa chọn áp dụng cho bạn.")
        print("Vui lòng trả lời các câu hỏi sau để tìm ra bệnh và cách chữa trị")
        # trả về tất cả các facts bạn cần ở đây
        yield Fact(action="engine_start")

    @Rule(Fact(action="engine_start"))
    def getUserInfo(self):
        self.declare(Fact(name=input("Tên của bạn là gì? : ")))
        self.declare(Fact(gender=input("Giới tính của bạn là gì? (nam/nữ) : ")))
        # self.declare(Fact(type=input("Triệu chứng của bạn là thể chất hay tâm thần? : ")))
        self.declare(Fact(action="questionnaire"))

    @Rule(Fact(action="questionnaire"))
    def askBasicQuestions(self):
        self.declare(Fact(red_eyes=yes_no("Bạn có bị đỏ mắt không?")))
        self.declare(Fact(fatigue=yes_no("Bạn có cảm thấy mệt mỏi không?")))
        self.declare(Fact(short_breath=yes_no("Bạn có khó thở không?")))
        self.declare(Fact(appetite_loss=yes_no("Bạn có bị mất cảm giác thèm ăn không?")))
        fevers = multi_input("Bạn có bị sốt không?", ["Sốt Thường", "Sốt Nhẹ", "Sốt Cao"])
        if fevers[0] != "không có":
            self.declare(Fact(fever="có"))
            for f in fevers:
                f = f.replace(" ", "_")
                self.declare(Fact(f))
        else:
            self.declare(Fact(fever="không"))

    @Rule(AND(Fact(appetite_loss="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(fatigue="không")))
    def askRelatedToAppetiteLoss(self):
        self.declare(Fact(joint_pain=yes_no("Bạn có đau khớp không?")))
        vomits = multi_input("Bạn có bị nôn không?", ["Nôn Nhiều", "Nôn Thường"])
        if vomits[0] != "không có":
            self.declare(Fact(vomit="có"))
            for v in vomits:
                v = v.replace(" ", "_")
                self.declare(Fact(v))
        else:
            self.declare(Fact(vomit="không"))

    @Rule(AND(Fact(appetite_loss="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(fatigue="không"),
              Fact(joint_pain="có")))
    def askArthritis(self):
        stiff_joint = yes_no("Bạn có bị cứng khớp không?")
        swell_joint = yes_no("Bạn có bị sưng khớp không?")
        red_skin_around_joint = yes_no("Da quanh khớp có chuyển sang màu đỏ không?")
        decreased_range = yes_no("Phạm vi cử động ở các khớp có giảm không?")
        tired = yes_no("Bạn có cảm thấy mệt mỏi ngay cả khi đi bộ quãng đường ngắn không?")
        count = 0
        for string in [stiff_joint, swell_joint, red_skin_around_joint, decreased_range, tired]:
            if string == "có":
                count += 1

        if count >= 3:
            symptoms = ["Cứng khớp", "Sưng khớp", "Đau khớp", "Da đỏ quanh khớp", "Mệt mỏi",
                        "Giảm khả năng cử động ở khớp", "Mất cảm giác thèm ăn"]
            suggest_disease("Viêm Khớp", symptoms)

    @Rule(AND(Fact(appetite_loss="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(fatigue="không"),
              Fact("Nôn_Nhiều")))
    def askPepticUlcer(self):
        burning_stomach = yes_no("Dạ dày của bạn có cảm giác nóng rát không?")
        bloating = yes_no("Bạn có cảm giác đầy hơi, chướng bụng hoặc ợ hơi không?")
        mild_nausea = yes_no("Bạn có buồn nôn nhẹ không?")
        weight_loss = yes_no("Bạn có bị sụt cân không?")
        abdominal_pain = yes_no("Bạn có đau bụng dữ dội và tập trung ở một vùng không?")
        count = 0
        for string in [burning_stomach, bloating, mild_nausea, weight_loss, abdominal_pain]:
            if string == "có":
                count += 1

        if count >= 3:
            symptoms = ["Mất cảm giác thèm ăn", "Nôn nhiều", "Cảm giác nóng rát ở dạ dày", "Đầy hơi dạ dày", "Buồn nôn",
                        "Sụt cân", "Đau bụng"]
            suggest_disease("Loét Dạ Dày", symptoms)

    @Rule(AND(Fact(appetite_loss="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(fatigue="không"),
              Fact("Nôn_Thường")))
    def askGastritis(self):
        nausea = yes_no("Bạn có cảm giác buồn nôn không?")
        fullness = yes_no("Bạn có cảm giác đầy ở vùng bụng trên không?")
        bloating = yes_no("Bạn có cảm thấy chướng bụng không?")
        abdominal_pain = yes_no("Bạn có đau gần vùng bụng không?")
        indigestion = yes_no("Bạn có gặp vấn đề về tiêu hóa không?")
        gnawing = yes_no(
            "Bạn có cảm giác đau âm ỉ hoặc nóng rát ở bụng trên mà có thể trở nên tốt hơn hoặc tồi tệ hơn khi ăn không?")
        count = 0
        for string in [nausea, fullness, bloating, abdominal_pain, indigestion, gnawing]:
            if string == "có":
                count += 1

        if count >= 4:
            symptoms = ["Mất cảm giác thèm ăn", "Nôn", "Buồn nôn", "Cảm giác đầy ở vùng bụng", "Chướng bụng",
                        "Đau bụng", "Khó tiêu", "Đau âm ỉ ở vùng bụng"]
            suggest_disease("Viêm Dạ Dày", symptoms)

    @Rule(AND(Fact(fatigue="có"), Fact(fever="không"), Fact(short_breath="không")))
    def askRelatedToFatigue(self):
        self.declare(Fact(extreme_thirst=yes_no("Bạn có cảm thấy khát nước nhiều hơn bình thường không?")))
        self.declare(Fact(extreme_hunger=yes_no("Bạn có cảm thấy đói nhiều hơn bình thường không?")))
        self.declare(Fact(dizziness=yes_no("Bạn có cảm thấy chóng mặt không?")))
        self.declare(Fact(muscle_weakness=yes_no("Cơ bắp của bạn có yếu hơn trước không?")))

    @Rule(AND(Fact(fatigue="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(extreme_thirst="có"),
              Fact(extreme_hunger="có")))
    def askDiabetes(self):
        frequent_urination = yes_no("Bạn có đi tiểu thường xuyên hơn trước không?")
        weight_loss = yes_no("Bạn có bị sụt cân không chủ ý không?")
        irratabiliry = yes_no("Bạn có dễ cáu gắt hơn gần đây không?")
        blurred_vision = yes_no("Thị lực của bạn có bị mờ không?")
        frequent_infections = yes_no("Bạn có bị nhiễm trùng thường xuyên như nhiễm trùng nướu răng hoặc da không?")
        sores = yes_no("Các vết thương của bạn có lâu lành không?")
        count = 0
        for string in [frequent_urination, weight_loss, irratabiliry, blurred_vision, frequent_infections, sores]:
            if string == "có":
                count += 1

        if count >= 4:
            symptoms = ["Mệt mỏi", "Khát nước nhiều", "Đói nhiều", "Sụt cân", "Thị lực mờ", "Nhiễm trùng thường xuyên",
                        "Đi tiểu thường xuyên", "Dễ cáu gắt", "Vết thương lâu lành"]
            suggest_disease("Tiểu Đường", symptoms)

    @Rule(AND(Fact(fatigue="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(extreme_thirst="có"),
              Fact(dizziness="có")))
    def askDehydration(self):
        less_frequent_urination = yes_no("Bạn có đi tiểu ít hơn bình thường không?")
        dark_urine = yes_no("Nước tiểu của bạn có bị sẫm màu không?")
        lethargy = yes_no("Bạn có cảm thấy uể oải không?")
        dry_mouth = yes_no("Miệng của bạn có khô đáng kể không?")
        count = 0
        for string in [less_frequent_urination, dark_urine, lethargy, dry_mouth]:
            if string == "có":
                count += 1

        if count >= 2:
            symptoms = ["Mệt mỏi", "Khát nước nhiều", "Chóng mặt", "Nước tiểu sẫm màu", "Cảm giác uể oải", "Khô miệng",
                        "Đi tiểu ít hơn"]
            suggest_disease("Mất Nước", symptoms)

    @Rule(AND(Fact(fatigue="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(muscle_weakness="có")))
    def askHypothoroidism(self):
        depression = yes_no("Bạn có cảm thấy trầm cảm gần đây không?")
        constipation = yes_no("Bạn có bị táo bón không?")
        feeling_cold = yes_no("Bạn có cảm thấy lạnh không?")
        dry_skin = yes_no("Da của bạn có trở nên khô hơn không?")
        dry_hair = yes_no("Tóc của bạn có trở nên khô và mỏng hơn không?")
        weight_gain = yes_no("Bạn có tăng cân đáng kể không?")
        decreased_sweating = yes_no("Bạn có đổ mồ hôi ít hơn trước không?")
        slowed_heartrate = yes_no("Nhịp tim của bạn có chậm lại không?")
        pain_joints = yes_no("Bạn có cảm thấy đau và cứng ở các khớp không?")
        hoarseness = yes_no("Giọng của bạn có thay đổi bất thường không?")
        count = 0
        for string in [depression, constipation, feeling_cold, dry_skin, dry_hair, weight_gain, decreased_sweating,
                       slowed_heartrate, pain_joints, hoarseness]:
            if string == "có":
                count += 1

        if count >= 7:
            symptoms = ["Mệt mỏi", "Cơ bắp yếu", "Trầm cảm", "Táo bón", "Cảm giác lạnh", "Da khô", "Tóc khô",
                        "Tăng cân", "Đổ mồ hôi giảm", "Nhịp tim chậm", "Đau khớp", "Khàn giọng"]
            suggest_disease("Suy Giáp", symptoms)

    @Rule(AND(Fact(short_breath="có"), Fact(fever="không")))
    def askRelatedToShortBreath(self):
        self.declare(Fact(back_joint_pian=yes_no("Bạn có đau lưng và đau khớp không?")))
        self.declare(Fact(chest_pain=yes_no("Bạn có đau ngực không?")))
        self.declare(Fact(cough=yes_no("Bạn có ho thường xuyên không?")))
        self.declare(Fact(fatigue=yes_no("Bạn có cảm thấy mệt mỏi không?")))
        self.declare(Fact(headache=yes_no("Bạn có bị đau đầu không?")))
        self.declare(Fact(pain_arms=yes_no("Bạn có đau ở cánh tay và vai không?")))

    @Rule(AND(Fact(short_breath="có"), Fact(fever="không"), Fact(back_joint_pian="có")))
    def askObesity(self):
        sweating = yes_no("Bạn có đổ mồ hôi nhiều hơn bình thường không?")
        snoring = yes_no("Bạn có phát triển thói quen ngáy không?")
        sudden_physical = yes_no("Bạn có khó đối phó với hoạt động thể chất đột ngột không?")
        tired = yes_no("Bạn có cảm thấy mệt mỏi mỗi ngày mà không cần làm việc nhiều không?")
        isolatd = yes_no("Bạn có cảm thấy bị cô lập không?")
        confidence = yes_no("Bạn có cảm thấy thiếu tự tin và lòng tự trọng thấp trong các hoạt động hàng ngày không?")
        count = 0
        for string in [sweating, snoring, sudden_physical, tired, isolatd, confidence]:
            if string == "có":
                count += 1

        if count >= 4:
            symptoms = ["Khó thở", "Đau lưng và khớp", "Đổ mồ hôi nhiều", "Thói quen ngáy", "Mệt mỏi", "Thiếu tự tin"]
            suggest_disease("Béo Phì", symptoms)

    @Rule(AND(Fact(short_breath="có"), Fact(fever="không"), Fact(chest_pain="có"), Fact(fatigue="có"),
              Fact(headache="có")))
    def askAnemia(self):
        irregular_heartbeat = yes_no("Bạn có nhịp tim không đều không?")
        weakness = yes_no("Bạn có cảm thấy yếu không?")
        pale_skin = yes_no("Da của bạn có chuyển sang màu nhợt nhạt hoặc hơi vàng không?")
        lightheadedness = yes_no("Bạn có bị chóng mặt hoặc cảm giác choáng váng không?")
        cold_hands_feet = yes_no("Bạn có bị lạnh tay và chân không?")
        count = 0
        for string in [irregular_heartbeat, weakness, pale_skin, lightheadedness, cold_hands_feet]:
            if string == "có":
                count += 1

        if count >= 3:
            symptoms = ["Khó thở", "Đau ngực", "Mệt mỏi", "Đau đầu", "Nhịp tim không đều", "Yếu ớt", "Da nhợt nhạt",
                        "Chóng mặt", "Tay chân lạnh"]
            suggest_disease("Thiếu Máu", symptoms)

    @Rule(AND(Fact(short_breath="có"), Fact(fever="không"), Fact(chest_pain="có"), Fact(fatigue="có"),
              Fact(pain_arms="có")))
    def askCAD(self):
        heaviness = yes_no(
            "Bạn có cảm giác nặng nề hoặc thắt ngực, thường ở vùng trung tâm của ngực, có thể lan ra cánh tay, cổ, hàm, lưng hoặc dạ dày không?")
        sweating = yes_no("Bạn có đổ mồ hôi thường xuyên không?")
        dizziness = yes_no("Bạn có cảm thấy chóng mặt không?")
        burning = yes_no("Bạn có cảm giác nóng rát gần tim không?")
        count = 0
        for string in [heaviness, sweating, dizziness, burning]:
            if string == "có":
                count += 1

        if count >= 2:
            symptoms = ["Khó thở", "Đau ngực", "Mệt mỏi", "Đau cánh tay", "Cảm giác nặng nề", "Đổ mồ hôi", "Chóng mặt",
                        "Cảm giác nóng rát gần tim"]
            suggest_disease("Xơ Vữa Động Mạch Vành", symptoms)

    @Rule(AND(Fact(short_breath="có"), Fact(fever="không"), Fact(chest_pain="có"), Fact(cough="có")))
    def askAsthma(self):
        Wheezing = yes_no("Bạn có âm thanh thở khò khè khi thở ra không?")
        sleep_trouble = yes_no("Bạn có khó ngủ do khó thở, ho hoặc thở khò khè không?")
        count = 0
        for string in [Wheezing, sleep_trouble]:
            if string == "có":
                count += 1

        if count >= 1:
            symptoms = ["Khó thở", "Đau ngực", "Ho", "Thở khò khè khi thở ra", "Khó ngủ do ho hoặc thở khò khè"]
            suggest_disease("Hen Suyễn", symptoms)

    @Rule(Fact("Sốt_Cao"))
    def askDengue(self):
        headache = yes_no("Bạn có đau đầu dữ dội không?")
        eyes_pain = yes_no("Bạn có đau sau mắt không?")
        muscle_pain = yes_no("Bạn có đau cơ dữ dội không?")
        joint_pian = yes_no("Bạn có đau khớp dữ dội không?")
        nausea = yes_no("Bạn có nôn hoặc cảm thấy buồn nôn không?")
        rashes = yes_no("Bạn có bị phát ban trên da xuất hiện từ hai đến năm ngày sau khi bắt đầu sốt không?")
        bleeding = yes_no("Bạn có bị chảy máu nhẹ như chảy máu mũi, chảy máu nướu răng, hoặc dễ bị bầm tím không?")
        count = 0
        for string in [headache, eyes_pain, muscle_pain, joint_pian, nausea, rashes, bleeding]:
            if string == "có":
                count += 1

        if count >= 5:
            symptoms = ["Sốt cao", "Đau đầu", "Đau mắt", "Đau cơ", "Đau khớp", "Buồn nôn", "Phát ban", "Chảy máu"]
            suggest_disease("Sốt Xuất Huyết", symptoms)

    @Rule(Fact("Sốt_Nhẹ"))
    def askBronchitis(self):
        cough = yes_no("Bạn có ho dai dẳng, có thể tạo ra đờm màu vàng xám không?")
        wheezing = yes_no("Bạn có bị thở khò khè không?")
        chills = yes_no("Bạn có cảm thấy ớn lạnh không?")
        chest_tightness = yes_no("Bạn có cảm giác thắt ngực không?")
        sore_throat = yes_no("Bạn có đau họng không?")
        body_aches = yes_no("Bạn có đau nhức cơ thể không?")
        breathlessness = yes_no("Bạn có cảm thấy khó thở không?")
        headache = yes_no("Bạn có đau đầu không?")
        nose_blocked = yes_no("Bạn có bị nghẹt mũi hoặc xoang không?")
        count = 0
        for string in [headache, cough, wheezing, chills, chest_tightness, sore_throat, body_aches, breathlessness,
                       nose_blocked]:
            if string == "có":
                count += 1

        if count >= 7:
            symptoms = ["Sốt nhẹ", "Ho", "Thở khò khè", "Ớn lạnh", "Thắt ngực", "Đau họng", "Đau nhức cơ thể",
                        "Đau đầu", "Khó thở", "Nghẹt mũi"]
            suggest_disease("Viêm Phế Quản", symptoms)

    @Rule(Fact(red_eyes="có"))
    def askEyeStatus(self):
        self.declare(Fact(eye_burn=yes_no("Bạn có cảm giác nóng rát ở mắt không?")))
        self.declare(Fact(eye_crusting=yes_no("Bạn có bị chảy mủ hoặc đóng vảy ở mắt không?")))
        self.declare(Fact(eye_irritation=yes_no("Bạn có bị kích ứng mắt không?")))

    @Rule(OR(Fact(eye_crusting="có"), Fact(eye_burn="có")), salience=1000)
    def disease_Conjunctivitis(self):
        suggest_disease("Viêm Kết Mạc", ["Cảm giác nóng rát ở mắt", "Đóng vảy ở mắt", "Đỏ mắt"])

    @Rule(Fact(eye_irritation="có"), salience=900)
    def disease_EyeAllergy(self):
        suggest_disease("Dị Ứng Mắt", ["Kích ứng mắt", "Đỏ mắt"])

    @Rule(Fact("Sốt_Thường"))
    def askRelatedToFever(self):
        self.declare(Fact(chest_pain=yes_no("Bạn có bị đau ngực không?")))
        self.declare(Fact(abdominal_pain=yes_no("Bạn có bị đau bụng không?")))
        self.declare(Fact(sore_throat=yes_no("Bạn có bị đau họng không?")))
        self.declare(Fact(chills=yes_no("Bạn có bị rùng mình ớn lạnh không?")))
        self.declare(Fact(rashes=yes_no("Bạn có bị phát ban trên da không?")))
        self.declare(Fact(nausea=yes_no("Bạn có nôn hoặc cảm thấy buồn nôn không?")))

    @Rule(AND(Fact("Sốt_Thường"), Fact(chest_pain="có"), Fact(fatigue="có"), Fact(chills="có")))
    def askTB(self):
        count = 0
        persistent_cough = yes_no("Bạn có bị ho dai dẳng kéo dài hơn 2 đến 3 tuần không?")
        weigh_loss = yes_no("Bạn có bị sụt cân không chủ ý không?")
        night_sweats = yes_no("Bạn có bị đổ mồ hôi đêm không?")
        cough_blood = yes_no("Bạn có ho ra máu không?")
        for string in [persistent_cough, weigh_loss, night_sweats, cough_blood]:
            if string == "có":
                count += 1

        if count >= 2:
            suggest_disease("Bệnh Lao", ["Sốt", "Đau ngực", "Mệt mỏi", "Mất cảm giác thèm ăn", "Ho dai dẳng"])

    @Rule(AND(Fact("Sốt_Thường"), Fact(fatigue="có"), Fact(sore_throat="có")))
    def askInfluenza(self):
        count = 0
        weakness = yes_no("Bạn có cảm thấy yếu ớt không?")
        dry_cough = yes_no("Bạn có bị ho khan dai dẳng không?")
        muscle_ache = yes_no("Bạn có đau nhức cơ, đặc biệt là ở lưng, cánh tay và chân không?")
        chills = yes_no("Bạn có bị đổ mồ hôi cùng với ớn lạnh không?")
        nasal_congestion = yes_no("Bạn có bị nghẹt mũi không?")
        headache = yes_no("Bạn có bị đau đầu không?")
        for string in [weakness, dry_cough, muscle_ache, chills, nasal_congestion, headache]:
            if string == "có":
                count += 1

        if count >= 4:
            symptoms = ["Sốt", "Mệt mỏi", "Đau họng", "Yếu ớt", "Ho khan", "Đau nhức cơ", "Ớn lạnh", "Nghẹt mũi",
                        "Đau đầu"]
            suggest_disease("Cúm", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(fatigue="có"), Fact(abdominal_pain="có")))
    def askHepatitis(self):
        count = 0
        flu_like = yes_no("Bạn có triệu chứng giống như cúm không?")
        dark_urine = yes_no("Nước tiểu của bạn có sẫm màu không?")
        pale_stool = yes_no("Bạn có phân nhạt màu không?")
        weight_loss = yes_no("Bạn có bị sụt cân không chủ ý không?")
        jaundice = yes_no("Da và mắt của bạn có chuyển sang màu vàng không?")
        for string in [flu_like, dark_urine, pale_stool, weight_loss, jaundice]:
            if string == "có":
                count += 1

        if count >= 3:
            symptoms = ["Sốt", "Mệt mỏi", "Đau bụng", "Triệu chứng giống cúm", "Nước tiểu sẫm màu", "Phân nhạt màu",
                        "Sụt cân", "Da và mắt vàng (Vàng da)"]
            suggest_disease("Viêm Gan", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(chest_pain="có"), Fact(short_breath="có"), Fact(nausea="có")))
    def askPneumonia(self):
        count = 0
        short_breath = yes_no(
            "Bạn có cảm thấy khó thở khi làm các hoạt động bình thường hoặc thậm chí khi nghỉ ngơi không?")
        sweat = yes_no("Bạn có bị đổ mồ hôi cùng với ớn lạnh không?")
        rapid_breath = yes_no("Bạn có thở nhanh không?")
        cough = yes_no("Bạn có ho ngày càng nặng hơn có thể tạo ra đờm màu vàng/xanh hoặc có máu không?")
        diarrhea = yes_no("Bạn có bị tiêu chảy không?")
        for string in [short_breath, sweat, rapid_breath, cough, diarrhea]:
            if string == "có":
                count += 1

        if count >= 3:
            symptoms = ["Sốt", "Đau ngực", "Khó thở", "Buồn nôn", "Đổ mồ hôi kèm ớn lạnh", "Thở nhanh", "Ho có đờm",
                        "Tiêu chảy"]
            suggest_disease("Viêm Phổi", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(chills="có"), Fact(abdominal_pain="có"), Fact(nausea="có")))
    def askMalaria(self):
        count = 0
        headache = yes_no("Bạn có bị đau đầu không?")
        sweat = yes_no("Bạn có đổ mồ hôi thường xuyên không?")
        cough = yes_no("Bạn có ho thường xuyên không?")
        weakness = yes_no("Bạn có cảm thấy yếu ớt không?")
        muscle_pain = yes_no("Bạn có đau nhức cơ dữ dội không?")
        back_pain = yes_no("Bạn có đau lưng dưới không?")
        for string in [headache, sweat, weakness, cough, muscle_pain, back_pain]:
            if string == "có":
                count += 1

        if count >= 4:
            symptoms = ["Sốt", "Ớn lạnh", "Đau bụng", "Buồn nôn", "Đau đầu", "Đổ mồ hôi", "Ho", "Yếu ớt", "Đau nhức cơ",
                        "Đau lưng"]
            suggest_disease("Sốt Rét", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(rashes="có")))
    def askHIV(self):
        count = 0
        headache = yes_no("Bạn có bị đau đầu không?")
        muscle_ache = yes_no("Bạn có bị đau nhức cơ và đau khớp không?")
        sore_throat = yes_no("Bạn có bị đau họng và lở loét miệng đau không?")
        lymph = yes_no("Bạn có bị sưng hạch bạch huyết, đặc biệt là ở cổ không?")
        diarrhea = yes_no("Bạn có bị tiêu chảy không?")
        cough = yes_no("Bạn có ho thường xuyên không?")
        weigh_loss = yes_no("Bạn có bị sụt cân không chủ ý không?")
        night_sweats = yes_no("Bạn có bị đổ mồ hôi đêm không?")
        for string in [headache, muscle_ache, sore_throat, lymph, diarrhea, cough, weigh_loss, night_sweats]:
            if string == "có":
                count += 1

        if count >= 6:
            symptoms = ["Sốt", "Phát ban", "Đau đầu", "Đau nhức cơ", "Đau họng", "Sưng hạch bạch huyết", "Tiêu chảy",
                        "Ho", "Sụt cân", "Đổ mồ hôi đêm"]
            suggest_disease("AIDS", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(nausea="có")))
    def askPancreatitis(self):
        count = 0
        upper_abdominal_pain = yes_no("Bạn có bị đau bụng trên không?")
        abdominal_eat = yes_no("Cơn đau bụng có trở nên tồi tệ hơn sau khi ăn không?")
        hearbeat = yes_no("Nhịp tim của bạn có cao hơn bình thường không?")
        weigh_loss = yes_no("Bạn có bị sụt cân không chủ ý không?")
        oily_stool = yes_no("Bạn có phân nhờn và có mùi khó chịu không?")
        for string in [upper_abdominal_pain, abdominal_eat, hearbeat, weigh_loss, oily_stool]:
            if string == "có":
                count += 1

        if count >= 3:
            symptoms = ["Buồn nôn", "Sốt", "Đau bụng trên", "Nhịp tim cao", "Sụt cân", "Phân nhờn và có mùi"]
            suggest_disease("Viêm Tụy", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(fatigue="có"), Fact(short_breath="có"), Fact(nausea="có")))
    def askCorona(self):
        chills = yes_no("Bạn có bị ớn lạnh đôi khi kèm theo rùng mình không?")
        cough = yes_no("Bạn có ho thường xuyên không?")
        body_aches = yes_no("Bạn có bị đau nhức cơ thể không?")
        headache = yes_no("Bạn có bị đau đầu không?")
        sore_throat = yes_no("Bạn có bị đau họng và lở loét miệng đau không?")
        lose_smell = yes_no("Bạn có bị mất vị giác và khứu giác đáng kể không?")
        diarrhea = yes_no("Bạn có bị tiêu chảy không?")
        count = 0
        for string in [chills, body_aches, headache, sore_throat, lose_smell, diarrhea]:
            if string == "có":
                count += 1

        if count >= 4:
            symptoms = ["Sốt", "Mệt mỏi", "Khó thở", "Buồn nôn", "Ớn lạnh", "Ho", "Đau nhức cơ thể", "Đau đầu",
                        "Đau họng", "Tiêu chảy", "Mất vị giác/khứu giác"]
            suggest_disease("Vi-rút Corona", symptoms)