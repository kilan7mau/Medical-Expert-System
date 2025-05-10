import streamlit as st
import webbrowser
import sys
import os
from experta import *
import base64
from io import BytesIO
import pyswip
import unicodedata

# Khởi tạo Prolog engine
prolog = pyswip.Prolog()
prolog.consult("knowledge.pl")

# Dictionary chuyển đổi tên bệnh từ tiếng Anh sang tiếng Việt
DISEASE_NAMES = {
    "arthritis": "Viêm Khớp",
    "peptic_ulcer": "Loét Dạ Dày",
    "gastritis": "Viêm Dạ Dày",
    "diabetes": "Tiểu Đường",
    "dehydration": "Mất Nước",
    "hypothyroidism": "Suy Giáp",
    "obesity": "Béo Phì",
    "anemia": "Thiếu Máu",
    "cad": "Xơ Vữa Động Mạch Vành",
    "asthma": "Hen Suyễn",
    "dengue": "Sốt Xuất Huyết",
    "bronchitis": "Viêm Phế Quản",
    "conjunctivitis": "Viêm Kết Mạc",
    "eye_allergy": "Dị Ứng Mắt",
    "tb": "Bệnh Lao",
    "influenza": "Cúm",
    "hepatitis": "Viêm Gan",
    "pneumonia": "Viêm Phổi",
    "malaria": "Sốt Rét",
    "hiv": "AIDS",
    "pancreatitis": "Viêm Tụy",
    "corona": "Vi-rút Corona"
}

# Dictionary chuyển đổi triệu chứng từ tiếng Anh sang tiếng Việt
SYMPTOM_NAMES = {
    "appetite_loss": "Mất cảm giác thèm ăn",
    "fever": "Sốt",
    "short_breath": "Khó thở",
    "fatigue": "Mệt mỏi",
    "joint_pain": "Đau khớp",
    "stiff_joint": "Cứng khớp",
    "swell_joint": "Sưng khớp",
    "red_skin_around_joint": "Da đỏ quanh khớp",
    "decreased_range": "Giảm khả năng cử động ở khớp",
    "tired": "Mệt mỏi",
    "vomit_many": "Nôn nhiều",
    "vomit_normal": "Nôn thường",
    "burning_stomach": "Cảm giác nóng rát ở dạ dày",
    "bloating": "Đầy hơi dạ dày",
    "mild_nausea": "Buồn nôn nhẹ",
    "weight_loss": "Sụt cân",
    "abdominal_pain": "Đau bụng",
    "nausea": "Buồn nôn",
    "fullness": "Cảm giác đầy ở vùng bụng",
    "indigestion": "Khó tiêu",
    "gnawing": "Đau âm ỉ ở vùng bụng",
    "extreme_thirst": "Khát nước nhiều",
    "extreme_hunger": "Đói nhiều",
    "dizziness": "Chóng mặt",
    "muscle_weakness": "Cơ bắp yếu",
    "frequent_urination": "Đi tiểu thường xuyên",
    "irratabiliry": "Dễ cáu gắt",
    "blurred_vision": "Thị lực mờ",
    "frequent_infections": "Nhiễm trùng thường xuyên",
    "sores": "Vết thương lâu lành",
    "less_frequent_urination": "Đi tiểu ít hơn",
    "dark_urine": "Nước tiểu sẫm màu",
    "lethargy": "Cảm giác uể oải",
    "dry_mouth": "Khô miệng",
    "depression": "Trầm cảm",
    "constipation": "Táo bón",
    "feeling_cold": "Cảm giác lạnh",
    "dry_skin": "Da khô",
    "dry_hair": "Tóc khô",
    "weight_gain": "Tăng cân",
    "decreased_sweating": "Đổ mồ hôi giảm",
    "slowed_heartrate": "Nhịp tim chậm",
    "pain_joints": "Đau khớp",
    "hoarseness": "Khàn giọng",
    "back_joint_pain": "Đau lưng và khớp",
    "sweating": "Đổ mồ hôi nhiều",
    "snoring": "Thói quen ngáy",
    "sudden_physical": "Khó đối phó với hoạt động thể chất",
    "isolated": "Cảm giác bị cô lập",
    "confidence": "Thiếu tự tin",
    "chest_pain": "Đau ngực",
    "headache": "Đau đầu",
    "irregular_heartbeat": "Nhịp tim không đều",
    "weakness": "Yếu ớt",
    "pale_skin": "Da nhợt nhạt",
    "lightheadedness": "Chóng mặt",
    "cold_hands_feet": "Tay chân lạnh",
    "pain_arms": "Đau cánh tay",
    "heaviness": "Cảm giác nặng nề",
    "burning": "Cảm giác nóng rát gần tim",
    "cough": "Ho",
    "wheezing": "Thở khò khè",
    "sleep_trouble": "Khó ngủ do ho hoặc thở khò khè",
    "fever_high": "Sốt cao",
    "eyes_pain": "Đau mắt",
    "muscle_pain": "Đau cơ",
    "rashes": "Phát ban",
    "bleeding": "Chảy máu",
    "fever_mild": "Sốt nhẹ",
    "chills": "Ớn lạnh",
    "chest_tightness": "Thắt ngực",
    "sore_throat": "Đau họng",
    "body_aches": "Đau nhức cơ thể",
    "breathlessness": "Khó thở",
    "nose_blocked": "Nghẹt mũi",
    "eye_burn": "Cảm giác nóng rát ở mắt",
    "eye_crusting": "Đóng vảy ở mắt",
    "eye_irritation": "Kích ứng mắt",
    "fever_normal": "Sốt thường",
    "persistent_cough": "Ho dai dẳng",
    "night_sweats": "Đổ mồ hôi đêm",
    "cough_blood": "Ho ra máu",
    "dry_cough": "Ho khan",
    "muscle_ache": "Đau nhức cơ",
    "nasal_congestion": "Nghẹt mũi",
    "flu_like": "Triệu chứng giống cúm",
    "pale_stool": "Phân nhạt màu",
    "jaundice": "Da và mắt vàng",
    "short_breath_severe": "Khó thở nặng",
    "rapid_breath": "Thở nhanh",
    "diarrhea": "Tiêu chảy",
    "back_pain": "Đau lưng",
    "lymph": "Sưng hạch bạch huyết",
    "upper_abdominal_pain": "Đau bụng trên",
    "abdominal_eat": "Đau bụng sau khi ăn",
    "heartbeat": "Nhịp tim cao",
    "oily_stool": "Phân nhờn và có mùi",
    "lose_smell": "Mất vị giác/khứu giác"
}

def remove_accents(input_str):
    """Chuyển đổi chuỗi tiếng Việt thành không dấu"""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def convert_to_prolog_fact(fact_name):
    """Chuyển đổi tên fact thành định dạng phù hợp với Prolog"""
    # Loại bỏ dấu và chuyển thành chữ thường
    fact_name = remove_accents(fact_name).lower()
    # Thay thế khoảng trắng và ký tự đặc biệt bằng dấu gạch dưới
    fact_name = fact_name.replace(" ", "_")
    # Loại bỏ các ký tự không hợp lệ
    fact_name = ''.join(c for c in fact_name if c.isalnum() or c == '_')
    return fact_name

def convert_symptom_to_vietnamese(symptom):
    """Chuyển đổi triệu chứng từ tiếng Anh sang tiếng Việt"""
    # Loại bỏ dấu ngoặc và giá trị yes/no
    symptom = str(symptom).split('(')[0].strip()
    # Chuyển đổi sang tiếng Việt nếu có trong dictionary
    return SYMPTOM_NAMES.get(symptom, symptom)

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
        self.diagnosed_diseases = set()  # Tập hợp các bệnh đã được chẩn đoán

    def declare_fact(self, fact_name, fact_value):
        """Thêm fact vào hệ thống và lưu vào danh sách facts"""
        # Kiểm tra xem fact đã tồn tại chưa
        for fact in self.fact_history:
            if fact[0] == fact_name and fact[1] == fact_value:
                return True

        self.declare(Fact(**{fact_name: fact_value}))
        self.fact_history.append((fact_name, fact_value))
        return True

    def suggest_disease(self, disease, symptoms):
        """Hiển thị kết quả chẩn đoán bệnh"""
        # Kiểm tra xem bệnh đã được chẩn đoán chưa
        if disease in self.diagnosed_diseases:
            return

        self.diagnosed_diseases.add(disease)

        st.success(f"Bạn có thể đang mắc bệnh **{disease}**")
        symptoms_text = '- ' + '\n- '.join(symptoms)
        st.write(f"Kết luận này dựa trên các triệu chứng của bạn trong số sau đây:\n{symptoms_text}")

        # Tạo key duy nhất cho các nút
        info_key = f"info_{hash(disease)}_{hash(str(symptoms))}"
        restart_key = f"restart_{hash(disease)}_{hash(str(symptoms))}"

        col1, col2 = st.columns(2)

        # Hiển thị nút để xem thêm thông tin về bệnh
        if col1.button(f"Xem thêm thông tin về bệnh {disease}", key=info_key):
            webbrowser.open(f"Treatment/html/{disease}.html", new=2)

        # Hiển thị nút để bắt đầu lại
        if col2.button("Bắt đầu lại", key=restart_key):
            st.session_state.clear()
            self.diagnosed_diseases.clear()
            st.rerun()

        # Dừng chương trình sau khi chẩn đoán
        st.stop()

    def ask_question(self, question_text, options=None, question_type="yes_no", single_select=False):
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

            # Tạo key duy nhất cho selectbox/multiselect
            select_key = f"select_{question_key}"
            submit_key = f"submit_{question_key}"

            if single_select:
                # Sử dụng selectbox cho câu hỏi chỉ chọn một đáp án
                selected_option = st.selectbox(
                    "Chọn một lựa chọn phù hợp:",
                    options,
                    key=select_key
                )

                if st.button("Xác nhận", key=submit_key):
                    st.session_state[question_key] = [selected_option]
                    st.rerun()
            else:
                # Sử dụng multiselect cho câu hỏi chọn nhiều đáp án
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

    def multi_input(self, input_str, options=[], single_select=False):
        """Wrapper cho phương thức ask_question với loại câu hỏi multi_select"""
        options_with_none = options.copy()
        options_with_none.append("không có")
        return self.ask_question(input_str, options=options_with_none, question_type="multi_select",
                                 single_select=single_select)

    def check_disease_rules(self):
        """Kiểm tra các luật bệnh từ knowledge.pl"""
        for fact in self.fact_history:
            fact_name, fact_value = fact
            # Chuyển đổi tên fact thành định dạng phù hợp với Prolog
            prolog_fact_name = convert_to_prolog_fact(fact_name)
            # Chuyển đổi giá trị "có"/"không" thành "yes"/"no" cho Prolog
            prolog_value = "yes" if fact_value == "có" else "no"
            try:
                prolog.assertz(f"{prolog_fact_name}({prolog_value})")
            except Exception as e:
                st.error(f"Lỗi khi thêm fact {fact_name}: {str(e)}")

        # Kiểm tra từng luật bệnh
        for disease in ["arthritis", "peptic_ulcer", "gastritis", "diabetes", "dehydration", 
                       "hypothyroidism", "obesity", "anemia", "cad", "asthma", "dengue", 
                       "bronchitis", "conjunctivitis", "eye_allergy", "tb", "influenza", 
                       "hepatitis", "pneumonia", "malaria", "hiv", "pancreatitis", "corona"]:
            try:
                # Kiểm tra xem có luật nào khớp không
                if list(prolog.query(f"rule({disease}, _)")):
                    # Lấy danh sách triệu chứng từ luật
                    symptoms = list(prolog.query(f"rule({disease}, Symptoms)"))[0]["Symptoms"]
                    # Chuyển đổi tên bệnh sang tiếng Việt
                    disease_name = DISEASE_NAMES.get(disease, disease)
                    # Chuyển đổi triệu chứng sang tiếng Việt
                    symptoms_list = [convert_symptom_to_vietnamese(symptom) for symptom in symptoms]
                    self.suggest_disease(disease_name, symptoms_list)
            except Exception as e:
                st.error(f"Lỗi khi kiểm tra bệnh {disease}: {str(e)}")

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
        fevers = self.multi_input("Bạn có bị sốt không?", fever_options, single_select=True)
        if fevers[0] != "không có":
            self.declare_fact("fever", "có")
            for f in fevers:
                f = f.replace(" ", "_")
                self.declare_fact(f, "có")
                if f == "Sốt_Cao":
                    self.askDengue()
                elif f == "Sốt_Thường":
                    self.askRelatedToFever()
        else:
            self.declare_fact("fever", "không")

        # Chỉ kiểm tra các điều kiện khác nếu không có sốt cao
        if not any(f[0] == "Sốt_Cao" and f[1] == "có" for f in self.fact_history):
            if appetite_loss == "có" and fatigue == "không" and short_breath == "không":
                self.askRelatedToAppetiteLoss()
            elif fatigue == "có" and short_breath == "không":
                self.askRelatedToFatigue()

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

        # Kiểm tra điều kiện cho viêm phổi theo đúng logic trong expert.py
        if any(f[0] == "Sốt_Thường" and f[1] == "có" for f in self.fact_history) and \
           chest_pain == "có" and \
           any(f[0] == "short_breath" and f[1] == "có" for f in self.fact_history) and \
           nausea == "có":
            self.askPneumonia()
        # Kiểm tra điều kiện cho bệnh lao
        elif any(f[0] == "Sốt_Thường" and f[1] == "có" for f in self.fact_history) and \
             chest_pain == "có" and \
             any(f[0] == "fatigue" and f[1] == "có" for f in self.fact_history) and \
             chills == "có":
            self.askTB()
        # Kiểm tra điều kiện cho cúm
        elif any(f[0] == "Sốt_Thường" and f[1] == "có" for f in self.fact_history) and \
             any(f[0] == "fatigue" and f[1] == "có" for f in self.fact_history) and \
             sore_throat == "có":
            self.askInfluenza()
        # Kiểm tra điều kiện cho viêm gan
        elif any(f[0] == "Sốt_Thường" and f[1] == "có" for f in self.fact_history) and \
             any(f[0] == "fatigue" and f[1] == "có" for f in self.fact_history) and \
             abdominal_pain == "có":
            self.askHepatitis()
        # Kiểm tra điều kiện cho sốt rét
        elif any(f[0] == "Sốt_Thường" and f[1] == "có" for f in self.fact_history) and \
             chills == "có" and \
             abdominal_pain == "có" and \
             nausea == "có":
            self.askMalaria()
        # Kiểm tra điều kiện cho AIDS
        elif any(f[0] == "Sốt_Thường" and f[1] == "có" for f in self.fact_history) and \
             rashes == "có":
            self.askHIV()
        # Kiểm tra điều kiện cho viêm tụy
        elif any(f[0] == "Sốt_Thường" and f[1] == "có" for f in self.fact_history) and \
             nausea == "có":
            self.askPancreatitis()
        # Kiểm tra điều kiện cho COVID-19
        elif any(f[0] == "Sốt_Thường" and f[1] == "có" for f in self.fact_history) and \
             any(f[0] == "fatigue" and f[1] == "có" for f in self.fact_history) and \
             any(f[0] == "short_breath" and f[1] == "có" for f in self.fact_history) and \
             nausea == "có":
            self.askCorona()

    def askRelatedToAppetiteLoss(self):
        st.header("Câu hỏi liên quan đến mất cảm giác thèm ăn")

        joint_pain = self.yes_no("Bạn có đau khớp không?")
        self.declare_fact("joint_pain", joint_pain)

        vomit_options = ["Nôn Nhiều", "Nôn Thường"]
        vomits = self.multi_input("Bạn có bị nôn không?", vomit_options, single_select=True)
        if vomits[0] != "không có":
            self.declare_fact("vomit", "có")
            for v in vomits:
                v = v.replace(" ", "_")
                self.declare_fact(v, "có")
        else:
            self.declare_fact("vomit", "không")

        # Kiểm tra điều kiện để hỏi về viêm khớp
        if joint_pain == "có":
            self.askArthritis()

    def askArthritis(self):
        st.header("Câu hỏi về viêm khớp")

        stiff_joint = self.yes_no("Bạn có bị cứng khớp không?")
        self.declare_fact("stiff_joint", stiff_joint)

        swell_joint = self.yes_no("Bạn có bị sưng khớp không?")
        self.declare_fact("swell_joint", swell_joint)

        red_skin_around_joint = self.yes_no("Da quanh khớp có chuyển sang màu đỏ không?")
        self.declare_fact("red_skin_around_joint", red_skin_around_joint)

        decreased_range = self.yes_no("Phạm vi cử động ở các khớp có giảm không?")
        self.declare_fact("decreased_range", decreased_range)

        tired = self.yes_no("Bạn có cảm thấy mệt mỏi ngay cả khi đi bộ quãng đường ngắn không?")
        self.declare_fact("tired", tired)

        # Kiểm tra các luật bệnh sau khi thu thập đủ thông tin
        self.check_disease_rules()

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

        # Kiểm tra điều kiện để hỏi về tiểu đường
        if extreme_thirst == "có" and extreme_hunger == "có":
            self.askDiabetes()

    def askDiabetes(self):
        st.header("Câu hỏi về tiểu đường")

        frequent_urination = self.yes_no("Bạn có đi tiểu thường xuyên hơn trước không?")
        self.declare_fact("frequent_urination", frequent_urination)

        weight_loss = self.yes_no("Bạn có bị sụt cân không chủ ý không?")
        self.declare_fact("weight_loss", weight_loss)

        irratabiliry = self.yes_no("Bạn có dễ cáu gắt hơn gần đây không?")
        self.declare_fact("irratabiliry", irratabiliry)

        blurred_vision = self.yes_no("Thị lực của bạn có bị mờ không?")
        self.declare_fact("blurred_vision", blurred_vision)

        frequent_infections = self.yes_no("Bạn có bị nhiễm trùng thường xuyên như nhiễm trùng nướu răng hoặc da không?")
        self.declare_fact("frequent_infections", frequent_infections)

        sores = self.yes_no("Các vết thương của bạn có lâu lành không?")
        self.declare_fact("sores", sores)

        # Kiểm tra điều kiện để chẩn đoán tiểu đường
        count = 0
        for fact in self.fact_history:
            if fact[0] in ["frequent_urination", "weight_loss", "irratabiliry", "blurred_vision", "frequent_infections", "sores"] and fact[1] == "có":
                count += 1

        if count >= 4:
            symptoms = ["Mệt mỏi", "Khát nước nhiều", "Đói nhiều", "Sụt cân", "Thị lực mờ", 
                       "Nhiễm trùng thường xuyên", "Đi tiểu thường xuyên", "Dễ cáu gắt", "Vết thương lâu lành"]
            self.suggest_disease("Tiểu Đường", symptoms)
        else:
            self.check_disease_rules()

    def askDehydration(self):
        st.header("Câu hỏi về mất nước")

        less_frequent_urination = self.yes_no("Bạn có đi tiểu ít hơn bình thường không?")
        self.declare_fact("less_frequent_urination", less_frequent_urination)

        dark_urine = self.yes_no("Nước tiểu của bạn có bị sẫm màu không?")
        self.declare_fact("dark_urine", dark_urine)

        lethargy = self.yes_no("Bạn có cảm thấy uể oải không?")
        self.declare_fact("lethargy", lethargy)

        dry_mouth = self.yes_no("Miệng của bạn có khô đáng kể không?")
        self.declare_fact("dry_mouth", dry_mouth)

        self.check_disease_rules()

    def askHypothyroidism(self):
        st.header("Câu hỏi về suy giáp")

        depression = self.yes_no("Bạn có cảm thấy trầm cảm gần đây không?")
        self.declare_fact("depression", depression)

        constipation = self.yes_no("Bạn có bị táo bón không?")
        self.declare_fact("constipation", constipation)

        feeling_cold = self.yes_no("Bạn có cảm thấy lạnh không?")
        self.declare_fact("feeling_cold", feeling_cold)

        dry_skin = self.yes_no("Da của bạn có trở nên khô hơn không?")
        self.declare_fact("dry_skin", dry_skin)

        dry_hair = self.yes_no("Tóc của bạn có trở nên khô và mỏng hơn không?")
        self.declare_fact("dry_hair", dry_hair)

        weight_gain = self.yes_no("Bạn có tăng cân đáng kể không?")
        self.declare_fact("weight_gain", weight_gain)

        decreased_sweating = self.yes_no("Bạn có đổ mồ hôi ít hơn trước không?")
        self.declare_fact("decreased_sweating", decreased_sweating)

        slowed_heartrate = self.yes_no("Nhịp tim của bạn có chậm lại không?")
        self.declare_fact("slowed_heartrate", slowed_heartrate)

        pain_joints = self.yes_no("Bạn có cảm thấy đau và cứng ở các khớp không?")
        self.declare_fact("pain_joints", pain_joints)

        hoarseness = self.yes_no("Giọng của bạn có thay đổi bất thường không?")
        self.declare_fact("hoarseness", hoarseness)

        self.check_disease_rules()

    def askObesity(self):
        st.header("Câu hỏi về béo phì")

        sweating = self.yes_no("Bạn có đổ mồ hôi nhiều hơn bình thường không?")
        self.declare_fact("sweating", sweating)

        snoring = self.yes_no("Bạn có phát triển thói quen ngáy không?")
        self.declare_fact("snoring", snoring)

        sudden_physical = self.yes_no("Bạn có khó đối phó với hoạt động thể chất đột ngột không?")
        self.declare_fact("sudden_physical", sudden_physical)

        tired = self.yes_no("Bạn có cảm thấy mệt mỏi mỗi ngày mà không cần làm việc nhiều không?")
        self.declare_fact("tired", tired)

        isolated = self.yes_no("Bạn có cảm thấy bị cô lập không?")
        self.declare_fact("isolated", isolated)

        confidence = self.yes_no("Bạn có cảm thấy thiếu tự tin và lòng tự trọng thấp trong các hoạt động hàng ngày không?")
        self.declare_fact("confidence", confidence)

        self.check_disease_rules()

    def askAnemia(self):
        st.header("Câu hỏi về thiếu máu")

        irregular_heartbeat = self.yes_no("Bạn có nhịp tim không đều không?")
        self.declare_fact("irregular_heartbeat", irregular_heartbeat)

        weakness = self.yes_no("Bạn có cảm thấy yếu không?")
        self.declare_fact("weakness", weakness)

        pale_skin = self.yes_no("Da của bạn có chuyển sang màu nhợt nhạt hoặc hơi vàng không?")
        self.declare_fact("pale_skin", pale_skin)

        lightheadedness = self.yes_no("Bạn có bị chóng mặt hoặc cảm giác choáng váng không?")
        self.declare_fact("lightheadedness", lightheadedness)

        cold_hands_feet = self.yes_no("Bạn có bị lạnh tay và chân không?")
        self.declare_fact("cold_hands_feet", cold_hands_feet)

        self.check_disease_rules()

    def askCAD(self):
        st.header("Câu hỏi về xơ vữa động mạch vành")

        heaviness = self.yes_no("Bạn có cảm giác nặng nề hoặc thắt ngực, thường ở vùng trung tâm của ngực, có thể lan ra cánh tay, cổ, hàm, lưng hoặc dạ dày không?")
        self.declare_fact("heaviness", heaviness)

        sweating = self.yes_no("Bạn có đổ mồ hôi thường xuyên không?")
        self.declare_fact("sweating", sweating)

        dizziness = self.yes_no("Bạn có cảm thấy chóng mặt không?")
        self.declare_fact("dizziness", dizziness)

        burning = self.yes_no("Bạn có cảm giác nóng rát gần tim không?")
        self.declare_fact("burning", burning)

        self.check_disease_rules()

    def askAsthma(self):
        st.header("Câu hỏi về hen suyễn")

        wheezing = self.yes_no("Bạn có âm thanh thở khò khè khi thở ra không?")
        self.declare_fact("wheezing", wheezing)

        sleep_trouble = self.yes_no("Bạn có khó ngủ do khó thở, ho hoặc thở khò khè không?")
        self.declare_fact("sleep_trouble", sleep_trouble)

        self.check_disease_rules()

    def askDengue(self):
        st.header("Câu hỏi về sốt xuất huyết")

        headache = self.yes_no("Bạn có đau đầu dữ dội không?")
        self.declare_fact("headache", headache)

        eyes_pain = self.yes_no("Bạn có đau sau mắt không?")
        self.declare_fact("eyes_pain", eyes_pain)

        muscle_pain = self.yes_no("Bạn có đau cơ dữ dội không?")
        self.declare_fact("muscle_pain", muscle_pain)

        joint_pain = self.yes_no("Bạn có đau khớp dữ dội không?")
        self.declare_fact("joint_pain", joint_pain)

        nausea = self.yes_no("Bạn có nôn hoặc cảm thấy buồn nôn không?")
        self.declare_fact("nausea", nausea)

        rashes = self.yes_no("Bạn có bị phát ban trên da xuất hiện từ hai đến năm ngày sau khi bắt đầu sốt không?")
        self.declare_fact("rashes", rashes)

        bleeding = self.yes_no("Bạn có bị chảy máu nhẹ như chảy máu mũi, chảy máu nướu răng, hoặc dễ bị bầm tím không?")
        self.declare_fact("bleeding", bleeding)

        self.check_disease_rules()

    def askBronchitis(self):
        st.header("Câu hỏi về viêm phế quản")

        cough = self.yes_no("Bạn có ho dai dẳng, có thể tạo ra đờm màu vàng xám không?")
        self.declare_fact("cough", cough)

        wheezing = self.yes_no("Bạn có bị thở khò khè không?")
        self.declare_fact("wheezing", wheezing)

        chills = self.yes_no("Bạn có cảm thấy ớn lạnh không?")
        self.declare_fact("chills", chills)

        chest_tightness = self.yes_no("Bạn có cảm giác thắt ngực không?")
        self.declare_fact("chest_tightness", chest_tightness)

        sore_throat = self.yes_no("Bạn có đau họng không?")
        self.declare_fact("sore_throat", sore_throat)

        body_aches = self.yes_no("Bạn có đau nhức cơ thể không?")
        self.declare_fact("body_aches", body_aches)

        breathlessness = self.yes_no("Bạn có cảm thấy khó thở không?")
        self.declare_fact("breathlessness", breathlessness)

        headache = self.yes_no("Bạn có đau đầu không?")
        self.declare_fact("headache", headache)

        nose_blocked = self.yes_no("Bạn có bị nghẹt mũi hoặc xoang không?")
        self.declare_fact("nose_blocked", nose_blocked)

        self.check_disease_rules()

    def askEyeStatus(self):
        st.header("Câu hỏi về tình trạng mắt")

        eye_burn = self.yes_no("Bạn có cảm giác nóng rát ở mắt không?")
        self.declare_fact("eye_burn", eye_burn)

        eye_crusting = self.yes_no("Bạn có bị chảy mủ hoặc đóng vảy ở mắt không?")
        self.declare_fact("eye_crusting", eye_crusting)

        eye_irritation = self.yes_no("Bạn có bị kích ứng mắt không?")
        self.declare_fact("eye_irritation", eye_irritation)

        self.check_disease_rules()

    def askTB(self):
        st.header("Câu hỏi về bệnh lao")

        fever_normal = self.yes_no("Bạn có bị sốt thường không?")
        self.declare_fact("fever_normal", fever_normal)

        chest_pain = self.yes_no("Bạn có đau ngực không?")
        self.declare_fact("chest_pain", chest_pain)

        fatigue = self.yes_no("Bạn có cảm thấy mệt mỏi không?")
        self.declare_fact("fatigue", fatigue)

        chills = self.yes_no("Bạn có cảm thấy ớn lạnh không?")
        self.declare_fact("chills", chills)

        self.check_disease_rules()

    def askInfluenza(self):
        st.header("Câu hỏi về cúm")

        fever_normal = self.yes_no("Bạn có bị sốt thường không?")
        self.declare_fact("fever_normal", fever_normal)

        fatigue = self.yes_no("Bạn có cảm thấy mệt mỏi không?")
        self.declare_fact("fatigue", fatigue)

        sore_throat = self.yes_no("Bạn có đau họng không?")
        self.declare_fact("sore_throat", sore_throat)

        self.check_disease_rules()

    def askHepatitis(self):
        st.header("Câu hỏi về viêm gan")

        fever_normal = self.yes_no("Bạn có bị sốt thường không?")
        self.declare_fact("fever_normal", fever_normal)

        fatigue = self.yes_no("Bạn có cảm thấy mệt mỏi không?")
        self.declare_fact("fatigue", fatigue)

        abdominal_pain = self.yes_no("Bạn có đau bụng không?")
        self.declare_fact("abdominal_pain", abdominal_pain)

        self.check_disease_rules()

    def askPneumonia(self):
        st.header("Câu hỏi về viêm phổi")

        short_breath_severe = self.yes_no("Bạn có cảm thấy khó thở khi làm các hoạt động bình thường hoặc thậm chí khi nghỉ ngơi không?")
        self.declare_fact("short_breath_severe", short_breath_severe)

        sweat = self.yes_no("Bạn có bị đổ mồ hôi cùng với ớn lạnh không?")
        self.declare_fact("sweat", sweat)

        rapid_breath = self.yes_no("Bạn có thở nhanh không?")
        self.declare_fact("rapid_breath", rapid_breath)

        cough = self.yes_no("Bạn có ho ngày càng nặng hơn có thể tạo ra đờm màu vàng/xanh hoặc có máu không?")
        self.declare_fact("cough", cough)

        diarrhea = self.yes_no("Bạn có bị tiêu chảy không?")
        self.declare_fact("diarrhea", diarrhea)

        # Kiểm tra điều kiện để chẩn đoán viêm phổi
        count = 0
        for fact in self.fact_history:
            if fact[0] in ["short_breath_severe", "sweat", "rapid_breath", "cough", "diarrhea"] and fact[1] == "có":
                count += 1

        if count >= 3:
            symptoms = ["Sốt", "Đau ngực", "Khó thở", "Buồn nôn", "Đổ mồ hôi kèm ớn lạnh", 
                       "Thở nhanh", "Ho có đờm", "Tiêu chảy"]
            self.suggest_disease("Viêm Phổi", symptoms)
        else:
            self.check_disease_rules()

    def askMalaria(self):
        st.header("Câu hỏi về sốt rét")

        fever_normal = self.yes_no("Bạn có bị sốt thường không?")
        self.declare_fact("fever_normal", fever_normal)

        chills = self.yes_no("Bạn có cảm thấy ớn lạnh không?")
        self.declare_fact("chills", chills)

        abdominal_pain = self.yes_no("Bạn có đau bụng không?")
        self.declare_fact("abdominal_pain", abdominal_pain)

        nausea = self.yes_no("Bạn có cảm thấy buồn nôn không?")
        self.declare_fact("nausea", nausea)

        self.check_disease_rules()

    def askHIV(self):
        st.header("Câu hỏi về AIDS")

        fever_normal = self.yes_no("Bạn có bị sốt thường không?")
        self.declare_fact("fever_normal", fever_normal)

        rashes = self.yes_no("Bạn có bị phát ban trên da không?")
        self.declare_fact("rashes", rashes)

        self.check_disease_rules()

    def askPancreatitis(self):
        st.header("Câu hỏi về viêm tụy")

        fever_normal = self.yes_no("Bạn có bị sốt thường không?")
        self.declare_fact("fever_normal", fever_normal)

        nausea = self.yes_no("Bạn có cảm thấy buồn nôn không?")
        self.declare_fact("nausea", nausea)

        self.check_disease_rules()

    def askCorona(self):
        st.header("Câu hỏi về COVID-19")

        fever_normal = self.yes_no("Bạn có bị sốt thường không?")
        self.declare_fact("fever_normal", fever_normal)

        fatigue = self.yes_no("Bạn có cảm thấy mệt mỏi không?")
        self.declare_fact("fatigue", fatigue)

        short_breath = self.yes_no("Bạn có khó thở không?")
        self.declare_fact("short_breath", short_breath)

        nausea = self.yes_no("Bạn có cảm thấy buồn nôn không?")
        self.declare_fact("nausea", nausea)

        self.check_disease_rules()


if __name__ == "__main__":
    st.set_page_config(page_title="Hệ Thống Chẩn Đoán Y Tế", page_icon="🏥")
    st.title("Hệ Thống Chẩn Đoán Y Tế")

    engine = HeThongChuanDoanYTe()
    engine.reset()
    engine.run()

    # Chỉ hiển thị thông báo này nếu không có bệnh nào được chẩn đoán
    if not engine.diagnosed_diseases:
        st.warning("Các triệu chứng không khớp với bất kỳ bệnh nào trong cơ sở dữ liệu của tôi.")