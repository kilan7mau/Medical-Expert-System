import streamlit as st
import webbrowser
import sys
import os
from experta import *
import base64
from io import BytesIO

# Import các lớp và hàm từ expert.py
# Khi sử dụng các lớp và hàm từ expert.py, ta sẽ giữ nguyên logic chính, 
# chỉ thay đổi cách nhập liệu và hiển thị

class HeThongChuanDoanYTe(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        # Khởi tạo các biến trạng thái để lưu trữ phiên làm việc Streamlit
        self.state = {}
        self.step = 0
        self.input_cache = {}  # Cache để lưu các input đã nhập
        self.fact_history = []  # Danh sách các facts đã declare
        self.questions = []  # Danh sách các câu hỏi đã hỏi
        self.current_question = None  # Câu hỏi hiện tại đang hỏi

    def declare_fact(self, fact_name, fact_value):
        """Thêm fact vào hệ thống và lưu vào danh sách facts"""
        self.declare(Fact(**{fact_name: fact_value}))
        self.fact_history.append((fact_name, fact_value))
        return True

    def suggest_disease(self, disease, symptoms):
        """Hiển thị kết quả chẩn đoán bệnh"""
        st.success(f"Bạn có thể đang mắc bệnh **{disease}**")
        symptoms_text = '- ' + '\n- '.join(symptoms)
        st.write(f"Kết luận này dựa trên các triệu chứng của bạn trong số sau đây:\n{symptoms_text}")
        
        # Tạo key duy nhất cho các nút
        info_key = f"info_{hash(disease)}"
        restart_key = f"restart_{hash(disease)}"
        
        # Hiển thị nút để xem thêm thông tin về bệnh
        if st.button(f"Xem thêm thông tin về bệnh {disease}", key=info_key):
            webbrowser.open(f"Treatment/html/{disease}.html", new=2)
        
        # Hiển thị nút để bắt đầu lại
        if st.button("Bắt đầu lại", key=restart_key):
            st.session_state.clear()
            st.rerun()

    def ask_question(self, question_text, options=None, question_type="yes_no"):
        """Hiển thị câu hỏi trên giao diện Streamlit và nhận phản hồi"""
        if options is None:
            options = []
        
        # Tạo key duy nhất cho câu hỏi
        question_key = f"q_{hash(question_text)}"
        
        # Nếu câu hỏi đã được trả lời, trả về giá trị đã lưu
        if question_key in st.session_state:
            return st.session_state[question_key]
        
        # Nếu không, hiển thị câu hỏi và đợi phản hồi
        self.current_question = question_text
        
        if question_type == "yes_no":
            st.subheader(question_text)
            col1, col2 = st.columns(2)
            
            # Tạo key duy nhất cho các nút
            yes_key = f"yes_{question_key}"
            no_key = f"no_{question_key}"
            
            if col1.button("Có", key=yes_key):
                st.session_state[question_key] = "có"
                st.rerun()
            elif col2.button("Không", key=no_key):
                st.session_state[question_key] = "không"
                st.rerun()
            
            # Nếu chưa có câu trả lời, dừng thực thi
            if question_key not in st.session_state:
                st.stop()
            
            return st.session_state[question_key]
        
        elif question_type == "multi_select":
            st.subheader(question_text)
            
            # Tạo key duy nhất cho multiselect
            select_key = f"select_{question_key}"
            submit_key = f"submit_{question_key}"
            
            selected_options = st.multiselect(
                "Chọn tất cả các lựa chọn phù hợp:",
                options,
                key=select_key
            )
            
            if st.button("Xác nhận", key=submit_key):
                if not selected_options:
                    st.session_state[question_key] = ["không có"]
                else:
                    st.session_state[question_key] = selected_options
                st.rerun()
            
            # Nếu chưa có câu trả lời, dừng thực thi
            if question_key not in st.session_state:
                st.stop()
            
            return st.session_state[question_key]
        
        return None  # Không bao giờ nên đến đây

    def yes_no(self, input_str):
        """Wrapper cho phương thức ask_question với loại câu hỏi yes_no"""
        return self.ask_question(input_str, question_type="yes_no")

    def multi_input(self, input_str, options=[]):
        """Wrapper cho phương thức ask_question với loại câu hỏi multi_select"""
        options_with_none = options.copy()
        options_with_none.append("không có")
        return self.ask_question(input_str, options=options_with_none, question_type="multi_select")

    @DefFacts()
    def _initial_action_(self):
        """Initial fact để khởi động hệ thống"""
        yield Fact(action="engine_start")

    @Rule(Fact(action="engine_start"))
    def getUserInfo(self):
        st.header("Thông tin cá nhân")
        
        name = st.text_input("Tên của bạn là gì?", key="name")
        if not name:
            st.stop()
            
        gender = st.selectbox("Giới tính của bạn là gì?", ["Nam", "Nữ"], key="gender")
        if not gender:
            st.stop()
            
        st.success(f"Xin chào {name}!")
        st.write("Vui lòng trả lời các câu hỏi sau để được chẩn đoán.")
        
        self.declare_fact("name", name)
        self.declare_fact("gender", gender.lower())
        self.declare_fact("action", "questionnaire")

    @Rule(Fact(action="questionnaire"))
    def askBasicQuestions(self):
        st.header("Câu hỏi cơ bản")
        
        red_eyes = self.yes_no("Bạn có bị đỏ mắt không?")
        self.declare_fact("red_eyes", red_eyes)
        
        fatigue = self.yes_no("Bạn có cảm thấy mệt mỏi không?")
        self.declare_fact("fatigue", fatigue)
        
        short_breath = self.yes_no("Bạn có khó thở không?")
        self.declare_fact("short_breath", short_breath)
        
        appetite_loss = self.yes_no("Bạn có bị mất cảm giác thèm ăn không?")
        self.declare_fact("appetite_loss", appetite_loss)
        
        fever_options = ["Sốt Thường", "Sốt Nhẹ", "Sốt Cao"]
        fevers = self.multi_input("Bạn có bị sốt không?", fever_options)
        if fevers[0] != "không có":
            self.declare_fact("fever", "có")
            for f in fevers:
                f = f.replace(" ", "_")
                self.declare_fact(f, "có")
        else:
            self.declare_fact("fever", "không")

    @Rule(AND(Fact(appetite_loss="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(fatigue="không")))
    def askRelatedToAppetiteLoss(self):
        st.header("Câu hỏi liên quan đến mất cảm giác thèm ăn")
        
        joint_pain = self.yes_no("Bạn có đau khớp không?")
        self.declare_fact("joint_pain", joint_pain)
        
        vomits = self.multi_input("Bạn có bị nôn không?", ["Nôn Nhiều", "Nôn Thường"])
        if vomits[0] != "không có":
            self.declare_fact("vomit", "có")
            for v in vomits:
                v = v.replace(" ", "_")
                self.declare_fact(v, "có")
        else:
            self.declare_fact("vomit", "không")

    @Rule(AND(Fact(appetite_loss="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(fatigue="không"),
              Fact(joint_pain="có")))
    def askArthritis(self):
        st.header("Câu hỏi liên quan đến viêm khớp")
        
        stiff_joint = self.yes_no("Bạn có bị cứng khớp không?")
        swell_joint = self.yes_no("Bạn có bị sưng khớp không?")
        red_skin_around_joint = self.yes_no("Da quanh khớp có chuyển sang màu đỏ không?")
        decreased_range = self.yes_no("Phạm vi cử động ở các khớp có giảm không?")
        tired = self.yes_no("Bạn có cảm thấy mệt mỏi ngay cả khi đi bộ quãng đường ngắn không?")
        
        count = 0
        for string in [stiff_joint, swell_joint, red_skin_around_joint, decreased_range, tired]:
            if string == "có":
                count += 1

        if count >= 3:
            symptoms = ["Cứng khớp", "Sưng khớp", "Đau khớp", "Da đỏ quanh khớp", "Mệt mỏi",
                      "Giảm khả năng cử động ở khớp", "Mất cảm giác thèm ăn"]
            self.suggest_disease("Viêm Khớp", symptoms)

    @Rule(AND(Fact(appetite_loss="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(fatigue="không"),
              Fact("Nôn_Nhiều")))
    def askPepticUlcer(self):
        st.header("Câu hỏi liên quan đến loét dạ dày")
        
        burning_stomach = self.yes_no("Dạ dày của bạn có cảm giác nóng rát không?")
        bloating = self.yes_no("Bạn có cảm giác đầy hơi, chướng bụng hoặc ợ hơi không?")
        mild_nausea = self.yes_no("Bạn có buồn nôn nhẹ không?")
        weight_loss = self.yes_no("Bạn có bị sụt cân không?")
        abdominal_pain = self.yes_no("Bạn có đau bụng dữ dội và tập trung ở một vùng không?")
        
        count = 0
        for string in [burning_stomach, bloating, mild_nausea, weight_loss, abdominal_pain]:
            if string == "có":
                count += 1

        if count >= 3:
            symptoms = ["Mất cảm giác thèm ăn", "Nôn nhiều", "Cảm giác nóng rát ở dạ dày", "Đầy hơi dạ dày", "Buồn nôn",
                      "Sụt cân", "Đau bụng"]
            self.suggest_disease("Loét Dạ Dày", symptoms)

    @Rule(AND(Fact(appetite_loss="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(fatigue="không"),
              Fact("Nôn_Thường")))
    def askGastritis(self):
        st.header("Câu hỏi liên quan đến viêm dạ dày")
        
        nausea = self.yes_no("Bạn có cảm giác buồn nôn không?")
        fullness = self.yes_no("Bạn có cảm giác đầy ở vùng bụng trên không?")
        bloating = self.yes_no("Bạn có cảm thấy chướng bụng không?")
        abdominal_pain = self.yes_no("Bạn có đau gần vùng bụng không?")
        indigestion = self.yes_no("Bạn có gặp vấn đề về tiêu hóa không?")
        gnawing = self.yes_no(
            "Bạn có cảm giác đau âm ỉ hoặc nóng rát ở bụng trên mà có thể trở nên tốt hơn hoặc tồi tệ hơn khi ăn không?")
        
        count = 0
        for string in [nausea, fullness, bloating, abdominal_pain, indigestion, gnawing]:
            if string == "có":
                count += 1

        if count >= 4:
            symptoms = ["Mất cảm giác thèm ăn", "Nôn", "Buồn nôn", "Cảm giác đầy ở vùng bụng", "Chướng bụng",
                      "Đau bụng", "Khó tiêu", "Đau âm ỉ ở vùng bụng"]
            self.suggest_disease("Viêm Dạ Dày", symptoms)

    @Rule(AND(Fact(fatigue="có"), Fact(fever="không"), Fact(short_breath="không")))
    def askRelatedToFatigue(self):
        st.header("Câu hỏi liên quan đến mệt mỏi")
        
        extreme_thirst = self.yes_no("Bạn có cảm thấy khát nước nhiều hơn bình thường không?")
        self.declare_fact("extreme_thirst", extreme_thirst)
        
        extreme_hunger = self.yes_no("Bạn có cảm thấy đói nhiều hơn bình thường không?")
        self.declare_fact("extreme_hunger", extreme_hunger)
        
        dizziness = self.yes_no("Bạn có cảm thấy chóng mặt không?")
        self.declare_fact("dizziness", dizziness)
        
        muscle_weakness = self.yes_no("Cơ bắp của bạn có yếu hơn trước không?")
        self.declare_fact("muscle_weakness", muscle_weakness)

    @Rule(AND(Fact(fatigue="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(extreme_thirst="có"),
              Fact(extreme_hunger="có")))
    def askDiabetes(self):
        st.header("Câu hỏi liên quan đến tiểu đường")
        
        frequent_urination = self.yes_no("Bạn có đi tiểu thường xuyên hơn trước không?")
        weight_loss = self.yes_no("Bạn có bị sụt cân không chủ ý không?")
        irratabiliry = self.yes_no("Bạn có dễ cáu gắt hơn gần đây không?")
        blurred_vision = self.yes_no("Thị lực của bạn có bị mờ không?")
        frequent_infections = self.yes_no("Bạn có bị nhiễm trùng thường xuyên như nhiễm trùng nướu răng hoặc da không?")
        sores = self.yes_no("Các vết thương của bạn có lâu lành không?")
        
        count = 0
        for string in [frequent_urination, weight_loss, irratabiliry, blurred_vision, frequent_infections, sores]:
            if string == "có":
                count += 1

        if count >= 4:
            symptoms = ["Mệt mỏi", "Khát nước nhiều", "Đói nhiều", "Sụt cân", "Thị lực mờ", "Nhiễm trùng thường xuyên",
                      "Đi tiểu thường xuyên", "Dễ cáu gắt", "Vết thương lâu lành"]
            self.suggest_disease("Tiểu Đường", symptoms)

    @Rule(AND(Fact(fatigue="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(extreme_thirst="có"),
              Fact(dizziness="có")))
    def askDehydration(self):
        st.header("Câu hỏi liên quan đến mất nước")
        
        less_frequent_urination = self.yes_no("Bạn có đi tiểu ít hơn bình thường không?")
        dark_urine = self.yes_no("Nước tiểu của bạn có bị sẫm màu không?")
        lethargy = self.yes_no("Bạn có cảm thấy uể oải không?")
        dry_mouth = self.yes_no("Miệng của bạn có khô đáng kể không?")
        
        count = 0
        for string in [less_frequent_urination, dark_urine, lethargy, dry_mouth]:
            if string == "có":
                count += 1

        if count >= 2:
            symptoms = ["Mệt mỏi", "Khát nước nhiều", "Chóng mặt", "Nước tiểu sẫm màu", "Cảm giác uể oải", "Khô miệng",
                      "Đi tiểu ít hơn"]
            self.suggest_disease("Mất Nước", symptoms)

    @Rule(AND(Fact(fatigue="có"), Fact(fever="không"), Fact(short_breath="không"), Fact(muscle_weakness="có")))
    def askHypothoroidism(self):
        st.header("Câu hỏi liên quan đến suy giáp")
        
        depression = self.yes_no("Bạn có cảm thấy trầm cảm gần đây không?")
        constipation = self.yes_no("Bạn có bị táo bón không?")
        feeling_cold = self.yes_no("Bạn có cảm thấy lạnh không?")
        dry_skin = self.yes_no("Da của bạn có trở nên khô hơn không?")
        dry_hair = self.yes_no("Tóc của bạn có trở nên khô và mỏng hơn không?")
        weight_gain = self.yes_no("Bạn có tăng cân đáng kể không?")
        decreased_sweating = self.yes_no("Bạn có đổ mồ hôi ít hơn trước không?")
        slowed_heartrate = self.yes_no("Nhịp tim của bạn có chậm lại không?")
        pain_joints = self.yes_no("Bạn có cảm thấy đau và cứng ở các khớp không?")
        hoarseness = self.yes_no("Giọng của bạn có thay đổi bất thường không?")
        
        count = 0
        for string in [depression, constipation, feeling_cold, dry_skin, dry_hair, weight_gain, decreased_sweating,
                     slowed_heartrate, pain_joints, hoarseness]:
            if string == "có":
                count += 1

        if count >= 7:
            symptoms = ["Mệt mỏi", "Cơ bắp yếu", "Trầm cảm", "Táo bón", "Cảm giác lạnh", "Da khô", "Tóc khô",
                      "Tăng cân", "Đổ mồ hôi giảm", "Nhịp tim chậm", "Đau khớp", "Khàn giọng"]
            self.suggest_disease("Suy Giáp", symptoms)

    @Rule(AND(Fact(short_breath="có"), Fact(fever="không")))
    def askRelatedToShortBreath(self):
        st.header("Câu hỏi liên quan đến khó thở")
        
        back_joint_pian = self.yes_no("Bạn có đau lưng và đau khớp không?")
        self.declare_fact("back_joint_pian", back_joint_pian)
        
        chest_pain = self.yes_no("Bạn có đau ngực không?")
        self.declare_fact("chest_pain", chest_pain)
        
        cough = self.yes_no("Bạn có ho thường xuyên không?")
        self.declare_fact("cough", cough)
        
        fatigue = self.yes_no("Bạn có cảm thấy mệt mỏi không?")
        self.declare_fact("fatigue", fatigue)
        
        headache = self.yes_no("Bạn có bị đau đầu không?")
        self.declare_fact("headache", headache)
        
        pain_arms = self.yes_no("Bạn có đau ở cánh tay và vai không?")
        self.declare_fact("pain_arms", pain_arms)

    @Rule(AND(Fact(short_breath="có"), Fact(fever="không"), Fact(back_joint_pian="có")))
    def askObesity(self):
        st.header("Câu hỏi liên quan đến béo phì")
        
        sweating = self.yes_no("Bạn có đổ mồ hôi nhiều hơn bình thường không?")
        snoring = self.yes_no("Bạn có phát triển thói quen ngáy không?")
        sudden_physical = self.yes_no("Bạn có khó đối phó với hoạt động thể chất đột ngột không?")
        tired = self.yes_no("Bạn có cảm thấy mệt mỏi mỗi ngày mà không cần làm việc nhiều không?")
        isolatd = self.yes_no("Bạn có cảm thấy bị cô lập không?")
        confidence = self.yes_no("Bạn có cảm thấy thiếu tự tin và lòng tự trọng thấp trong các hoạt động hàng ngày không?")
        
        count = 0
        for string in [sweating, snoring, sudden_physical, tired, isolatd, confidence]:
            if string == "có":
                count += 1

        if count >= 4:
            symptoms = ["Khó thở", "Đau lưng và khớp", "Đổ mồ hôi nhiều", "Thói quen ngáy", "Mệt mỏi", "Thiếu tự tin"]
            self.suggest_disease("Béo Phì", symptoms)

    @Rule(AND(Fact(short_breath="có"), Fact(fever="không"), Fact(chest_pain="có"), Fact(fatigue="có"),
              Fact(headache="có")))
    def askAnemia(self):
        st.header("Câu hỏi liên quan đến thiếu máu")
        
        irregular_heartbeat = self.yes_no("Bạn có nhịp tim không đều không?")
        weakness = self.yes_no("Bạn có cảm thấy yếu không?")
        pale_skin = self.yes_no("Da của bạn có chuyển sang màu nhợt nhạt hoặc hơi vàng không?")
        lightheadedness = self.yes_no("Bạn có bị chóng mặt hoặc cảm giác choáng váng không?")
        cold_hands_feet = self.yes_no("Bạn có bị lạnh tay và chân không?")
        
        count = 0
        for string in [irregular_heartbeat, weakness, pale_skin, lightheadedness, cold_hands_feet]:
            if string == "có":
                count += 1

        if count >= 3:
            symptoms = ["Khó thở", "Đau ngực", "Mệt mỏi", "Đau đầu", "Nhịp tim không đều", "Yếu ớt", "Da nhợt nhạt",
                      "Chóng mặt", "Tay chân lạnh"]
            self.suggest_disease("Thiếu Máu", symptoms)

    @Rule(AND(Fact(short_breath="có"), Fact(fever="không"), Fact(chest_pain="có"), Fact(fatigue="có"),
              Fact(pain_arms="có")))
    def askCAD(self):
        st.header("Câu hỏi liên quan đến xơ vữa động mạch vành")
        
        heaviness = self.yes_no(
            "Bạn có cảm giác nặng nề hoặc thắt ngực, thường ở vùng trung tâm của ngực, có thể lan ra cánh tay, cổ, hàm, lưng hoặc dạ dày không?")
        sweating = self.yes_no("Bạn có đổ mồ hôi thường xuyên không?")
        dizziness = self.yes_no("Bạn có cảm thấy chóng mặt không?")
        burning = self.yes_no("Bạn có cảm giác nóng rát gần tim không?")
        
        count = 0
        for string in [heaviness, sweating, dizziness, burning]:
            if string == "có":
                count += 1

        if count >= 2:
            symptoms = ["Khó thở", "Đau ngực", "Mệt mỏi", "Đau cánh tay", "Cảm giác nặng nề", "Đổ mồ hôi", "Chóng mặt",
                      "Cảm giác nóng rát gần tim"]
            self.suggest_disease("Xơ Vữa Động Mạch Vành", symptoms)

    @Rule(AND(Fact(short_breath="có"), Fact(fever="không"), Fact(chest_pain="có"), Fact(cough="có")))
    def askAsthma(self):
        st.header("Câu hỏi liên quan đến hen suyễn")
        
        Wheezing = self.yes_no("Bạn có âm thanh thở khò khè khi thở ra không?")
        sleep_trouble = self.yes_no("Bạn có khó ngủ do khó thở, ho hoặc thở khò khè không?")
        
        count = 0
        for string in [Wheezing, sleep_trouble]:
            if string == "có":
                count += 1

        if count >= 1:
            symptoms = ["Khó thở", "Đau ngực", "Ho", "Thở khò khè khi thở ra", "Khó ngủ do ho hoặc thở khò khè"]
            self.suggest_disease("Hen Suyễn", symptoms)

    @Rule(Fact("Sốt_Cao"))
    def askDengue(self):
        st.header("Câu hỏi liên quan đến sốt xuất huyết")
        
        headache = self.yes_no("Bạn có đau đầu dữ dội không?")
        eyes_pain = self.yes_no("Bạn có đau sau mắt không?")
        muscle_pain = self.yes_no("Bạn có đau cơ dữ dội không?")
        joint_pian = self.yes_no("Bạn có đau khớp dữ dội không?")
        nausea = self.yes_no("Bạn có nôn hoặc cảm thấy buồn nôn không?")
        rashes = self.yes_no("Bạn có bị phát ban trên da xuất hiện từ hai đến năm ngày sau khi bắt đầu sốt không?")
        bleeding = self.yes_no("Bạn có bị chảy máu nhẹ như chảy máu mũi, chảy máu nướu răng, hoặc dễ bị bầm tím không?")
        
        count = 0
        for string in [headache, eyes_pain, muscle_pain, joint_pian, nausea, rashes, bleeding]:
            if string == "có":
                count += 1

        if count >= 5:
            symptoms = ["Sốt cao", "Đau đầu", "Đau mắt", "Đau cơ", "Đau khớp", "Buồn nôn", "Phát ban", "Chảy máu"]
            self.suggest_disease("Sốt Xuất Huyết", symptoms)

    @Rule(Fact("Sốt_Nhẹ"))
    def askBronchitis(self):
        st.header("Câu hỏi liên quan đến viêm phế quản")
        
        cough = self.yes_no("Bạn có ho dai dẳng, có thể tạo ra đờm màu vàng xám không?")
        wheezing = self.yes_no("Bạn có bị thở khò khè không?")
        chills = self.yes_no("Bạn có cảm thấy ớn lạnh không?")
        chest_tightness = self.yes_no("Bạn có cảm giác thắt ngực không?")
        sore_throat = self.yes_no("Bạn có đau họng không?")
        body_aches = self.yes_no("Bạn có đau nhức cơ thể không?")
        breathlessness = self.yes_no("Bạn có cảm thấy khó thở không?")
        headache = self.yes_no("Bạn có đau đầu không?")
        nose_blocked = self.yes_no("Bạn có bị nghẹt mũi hoặc xoang không?")
        
        count = 0
        for string in [headache, cough, wheezing, chills, chest_tightness, sore_throat, body_aches, breathlessness, nose_blocked]:
            if string == "có":
                count += 1

        if count >= 7:
            symptoms = ["Sốt nhẹ", "Ho", "Thở khò khè", "Ớn lạnh", "Thắt ngực", "Đau họng", "Đau nhức cơ thể", "Đau đầu", "Khó thở", "Nghẹt mũi"]
            self.suggest_disease("Viêm Phế Quản", symptoms)

    @Rule(Fact(red_eyes="có"))
    def askEyeStatus(self):
        st.header("Câu hỏi liên quan đến mắt")
        
        eye_burn = self.yes_no("Bạn có cảm giác nóng rát ở mắt không?")
        self.declare_fact("eye_burn", eye_burn)
        
        eye_crusting = self.yes_no("Bạn có bị chảy mủ hoặc đóng vảy ở mắt không?")
        self.declare_fact("eye_crusting", eye_crusting)
        
        eye_irritation = self.yes_no("Bạn có bị kích ứng mắt không?")
        self.declare_fact("eye_irritation", eye_irritation)

    @Rule(OR(Fact(eye_crusting="có"), Fact(eye_burn="có")), salience=1000)
    def disease_Conjunctivitis(self):
        symptoms = ["Cảm giác nóng rát ở mắt", "Đóng vảy ở mắt", "Đỏ mắt"]
        self.suggest_disease("Viêm Kết Mạc", symptoms)

    @Rule(Fact(eye_irritation="có"), salience=900)
    def disease_EyeAllergy(self):
        symptoms = ["Kích ứng mắt", "Đỏ mắt"]
        self.suggest_disease("Dị Ứng Mắt", symptoms)

    @Rule(Fact("Sốt_Thường"))
    def askRelatedToFever(self):
        st.header("Câu hỏi liên quan đến sốt thường")
        
        chest_pain = self.yes_no("Bạn có bị đau ngực không?")
        self.declare_fact("chest_pain", chest_pain)
        
        abdominal_pain = self.yes_no("Bạn có bị đau bụng không?")
        self.declare_fact("abdominal_pain", abdominal_pain)
        
        sore_throat = self.yes_no("Bạn có bị đau họng không?")
        self.declare_fact("sore_throat", sore_throat)
        
        chills = self.yes_no("Bạn có bị rùng mình ớn lạnh không?")
        self.declare_fact("chills", chills)
        
        rashes = self.yes_no("Bạn có bị phát ban trên da không?")
        self.declare_fact("rashes", rashes)
        
        nausea = self.yes_no("Bạn có nôn hoặc cảm thấy buồn nôn không?")
        self.declare_fact("nausea", nausea)

    @Rule(AND(Fact("Sốt_Thường"), Fact(chest_pain="có"), Fact(fatigue="có"), Fact(chills="có")))
    def askTB(self):
        st.header("Câu hỏi liên quan đến bệnh lao")
        
        persistent_cough = self.yes_no("Bạn có bị ho dai dẳng kéo dài hơn 2 đến 3 tuần không?")
        weigh_loss = self.yes_no("Bạn có bị sụt cân không chủ ý không?")
        night_sweats = self.yes_no("Bạn có bị đổ mồ hôi đêm không?")
        cough_blood = self.yes_no("Bạn có ho ra máu không?")
        
        count = 0
        for string in [persistent_cough, weigh_loss, night_sweats, cough_blood]:
            if string == "có":
                count += 1

        if count >= 2:
            symptoms = ["Sốt", "Đau ngực", "Mệt mỏi", "Mất cảm giác thèm ăn", "Ho dai dẳng"]
            self.suggest_disease("Bệnh Lao", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(fatigue="có"), Fact(sore_throat="có")))
    def askInfluenza(self):
        st.header("Câu hỏi liên quan đến cúm")
        
        weakness = self.yes_no("Bạn có cảm thấy yếu ớt không?")
        dry_cough = self.yes_no("Bạn có bị ho khan dai dẳng không?")
        muscle_ache = self.yes_no("Bạn có đau nhức cơ, đặc biệt là ở lưng, cánh tay và chân không?")
        chills = self.yes_no("Bạn có bị đổ mồ hôi cùng với ớn lạnh không?")
        nasal_congestion = self.yes_no("Bạn có bị nghẹt mũi không?")
        headache = self.yes_no("Bạn có bị đau đầu không?")
        
        count = 0
        for string in [weakness, dry_cough, muscle_ache, chills, nasal_congestion, headache]:
            if string == "có":
                count += 1

        if count >= 4:
            symptoms = ["Sốt", "Mệt mỏi", "Đau họng", "Yếu ớt", "Ho khan", "Đau nhức cơ", "Ớn lạnh", "Nghẹt mũi", "Đau đầu"]
            self.suggest_disease("Cúm", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(fatigue="có"), Fact(abdominal_pain="có")))
    def askHepatitis(self):
        st.header("Câu hỏi liên quan đến viêm gan")
        
        flu_like = self.yes_no("Bạn có triệu chứng giống như cúm không?")
        dark_urine = self.yes_no("Nước tiểu của bạn có sẫm màu không?")
        pale_stool = self.yes_no("Bạn có phân nhạt màu không?")
        weight_loss = self.yes_no("Bạn có bị sụt cân không chủ ý không?")
        jaundice = self.yes_no("Da và mắt của bạn có chuyển sang màu vàng không?")
        
        count = 0
        for string in [flu_like, dark_urine, pale_stool, weight_loss, jaundice]:
            if string == "có":
                count += 1

        if count >= 3:
            symptoms = ["Sốt", "Mệt mỏi", "Đau bụng", "Triệu chứng giống cúm", "Nước tiểu sẫm màu", "Phân nhạt màu", "Sụt cân", "Da và mắt vàng (Vàng da)"]
            self.suggest_disease("Viêm Gan", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(chest_pain="có"), Fact(short_breath="có"), Fact(nausea="có")))
    def askPneumonia(self):
        st.header("Câu hỏi liên quan đến viêm phổi")
        
        short_breath = self.yes_no("Bạn có cảm thấy khó thở khi làm các hoạt động bình thường hoặc thậm chí khi nghỉ ngơi không?")
        sweat = self.yes_no("Bạn có bị đổ mồ hôi cùng với ớn lạnh không?")
        rapid_breath = self.yes_no("Bạn có thở nhanh không?")
        cough = self.yes_no("Bạn có ho ngày càng nặng hơn có thể tạo ra đờm màu vàng/xanh hoặc có máu không?")
        diarrhea = self.yes_no("Bạn có bị tiêu chảy không?")
        
        count = 0
        for string in [short_breath, sweat, rapid_breath, cough, diarrhea]:
            if string == "có":
                count += 1

        if count >= 3:
            symptoms = ["Sốt", "Đau ngực", "Khó thở", "Buồn nôn", "Đổ mồ hôi kèm ớn lạnh", "Thở nhanh", "Ho có đờm", "Tiêu chảy"]
            self.suggest_disease("Viêm Phổi", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(chills="có"), Fact(abdominal_pain="có"), Fact(nausea="có")))
    def askMalaria(self):
        st.header("Câu hỏi liên quan đến sốt rét")
        
        headache = self.yes_no("Bạn có bị đau đầu không?")
        sweat = self.yes_no("Bạn có đổ mồ hôi thường xuyên không?")
        cough = self.yes_no("Bạn có ho thường xuyên không?")
        weakness = self.yes_no("Bạn có cảm thấy yếu ớt không?")
        muscle_pain = self.yes_no("Bạn có đau nhức cơ dữ dội không?")
        back_pain = self.yes_no("Bạn có đau lưng dưới không?")
        
        count = 0
        for string in [headache, sweat, weakness, cough, muscle_pain, back_pain]:
            if string == "có":
                count += 1

        if count >= 4:
            symptoms = ["Sốt", "Ớn lạnh", "Đau bụng", "Buồn nôn", "Đau đầu", "Đổ mồ hôi", "Ho", "Yếu ớt", "Đau nhức cơ", "Đau lưng"]
            self.suggest_disease("Sốt Rét", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(rashes="có")))
    def askHIV(self):
        st.header("Câu hỏi liên quan đến HIV")
        
        headache = self.yes_no("Bạn có bị đau đầu không?")
        muscle_ache = self.yes_no("Bạn có bị đau nhức cơ và đau khớp không?")
        sore_throat = self.yes_no("Bạn có bị đau họng và lở loét miệng đau không?")
        lymph = self.yes_no("Bạn có bị sưng hạch bạch huyết, đặc biệt là ở cổ không?")
        diarrhea = self.yes_no("Bạn có bị tiêu chảy không?")
        cough = self.yes_no("Bạn có ho thường xuyên không?")
        weigh_loss = self.yes_no("Bạn có bị sụt cân không chủ ý không?")
        night_sweats = self.yes_no("Bạn có bị đổ mồ hôi đêm không?")
        
        count = 0
        for string in [headache, muscle_ache, sore_throat, lymph, diarrhea, cough, weigh_loss, night_sweats]:
            if string == "có":
                count += 1

        if count >= 6:
            symptoms = ["Sốt", "Phát ban", "Đau đầu", "Đau nhức cơ", "Đau họng", "Sưng hạch bạch huyết", "Tiêu chảy", "Ho", "Sụt cân", "Đổ mồ hôi đêm"]
            self.suggest_disease("AIDS", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(nausea="có")))
    def askPancreatitis(self):
        st.header("Câu hỏi liên quan đến viêm tụy")
        
        upper_abdominal_pain = self.yes_no("Bạn có bị đau bụng trên không?")
        abdominal_eat = self.yes_no("Cơn đau bụng có trở nên tồi tệ hơn sau khi ăn không?")
        hearbeat = self.yes_no("Nhịp tim của bạn có cao hơn bình thường không?")
        weigh_loss = self.yes_no("Bạn có bị sụt cân không chủ ý không?")
        oily_stool = self.yes_no("Bạn có phân nhờn và có mùi khó chịu không?")
        
        count = 0
        for string in [upper_abdominal_pain, abdominal_eat, hearbeat, weigh_loss, oily_stool]:
            if string == "có":
                count += 1

        if count >= 3:
            symptoms = ["Buồn nôn", "Sốt", "Đau bụng trên", "Nhịp tim cao", "Sụt cân", "Phân nhờn và có mùi"]
            self.suggest_disease("Viêm Tụy", symptoms)

    @Rule(AND(Fact("Sốt_Thường"), Fact(fatigue="có"), Fact(short_breath="có"), Fact(nausea="có")))
    def askCorona(self):
        st.header("Câu hỏi liên quan đến COVID-19")
        
        chills = self.yes_no("Bạn có bị ớn lạnh đôi khi kèm theo rùng mình không?")
        cough = self.yes_no("Bạn có ho thường xuyên không?")
        body_aches = self.yes_no("Bạn có bị đau nhức cơ thể không?")
        headache = self.yes_no("Bạn có bị đau đầu không?")
        sore_throat = self.yes_no("Bạn có bị đau họng và lở loét miệng đau không?")
        lose_smell = self.yes_no("Bạn có bị mất vị giác và khứu giác đáng kể không?")
        diarrhea = self.yes_no("Bạn có bị tiêu chảy không?")
        
        count = 0
        for string in [chills, body_aches, headache, sore_throat, lose_smell, diarrhea]:
            if string == "có":
                count += 1

        if count >= 4:
            symptoms = ["Sốt", "Mệt mỏi", "Khó thở", "Buồn nôn", "Ớn lạnh", "Ho", "Đau nhức cơ thể", "Đau đầu", "Đau họng", "Tiêu chảy", "Mất vị giác/khứu giác"]
            self.suggest_disease("Vi-rút Corona", symptoms)


if __name__ == "__main__":
    st.set_page_config(page_title="Hệ Thống Chẩn Đoán Y Tế", page_icon="🏥")
    st.title("Hệ Thống Chẩn Đoán Y Tế")
    
    engine = HeThongChuanDoanYTe()
    engine.reset()
    engine.run()
    
    st.warning("Các triệu chứng không khớp với bất kỳ bệnh nào trong cơ sở dữ liệu của tôi.")