import streamlit as st
import os
from experta import *
import pyswip
import unicodedata
import streamlit.components.v1 as components
import functools
import time
import logging

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("medical_expert_system.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="Hệ Thống Chẩn Đoán Y Tế", 
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    "red_eyes": "Mắt đỏ",
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

# Cache cho các kết quả của hàm lặp lại nhiều lần
@functools.lru_cache(maxsize=64)
def remove_accents(input_str):
    """Chuyển đổi chuỗi tiếng Việt thành không dấu"""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

@functools.lru_cache(maxsize=128)
def convert_to_prolog_fact(fact_name):
    """Chuyển đổi tên fact thành định dạng phù hợp với Prolog"""
    # Loại bỏ dấu và chuyển thành chữ thường
    fact_name = remove_accents(fact_name).lower()
    # Thay thế khoảng trắng và ký tự đặc biệt bằng dấu gạch dưới
    fact_name = fact_name.replace(" ", "_")
    # Loại bỏ các ký tự không hợp lệ
    return ''.join(c for c in fact_name if c.isalnum() or c == '_')

@functools.lru_cache(maxsize=128)
def convert_symptom_to_vietnamese(symptom):
    """Chuyển đổi triệu chứng từ tiếng Anh sang tiếng Việt"""
    # Loại bỏ dấu ngoặc và giá trị yes/no
    symptom = str(symptom).split('(')[0].strip()
    # Chuyển đổi sang tiếng Việt nếu có trong dictionary
    return SYMPTOM_NAMES.get(symptom, symptom)

# Decorator để đo thời gian thực thi của hàm
def measure_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            logger.debug(f"Calling function {func.__name__} with args: {args}, kwargs: {kwargs}")
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            if execution_time > 0.5:  # Chỉ ghi nhận các hàm tốn thời gian > 0.5s
                logger.info(f"Function {func.__name__} took {execution_time:.2f} seconds to execute")
            return result
        except Exception as e:
            logger.error(f"Error in function {func.__name__}: {str(e)}")
            raise
    return wrapper

# Import các lớp và hàm từ expert.py
# Khi sử dụng các lớp và hàm từ expert.py, ta sẽ giữ nguyên logic chính, 
# chỉ thay đổi cách nhập liệu và hiển thị

class HeThongChuanDoanYTe(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        # Khởi tạo các biến trạng thái để lưu trữ phiên làm việc Streamlit
        self.step = 0
        self.fact_history = []  # Danh sách các facts đã declare
        self.current_question = None  # Câu hỏi hiện tại đang hỏi
        self.diagnosed_diseases = set()  # Tập hợp các bệnh đã được chẩn đoán
        self.question_cache = {}  # Cache để lưu các câu hỏi đã hỏi
        
        # Khởi tạo session_state cho Streamlit nếu chưa tồn tại
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.step = 0
            # Tạo một set trống để lưu trữ các câu hỏi đã hỏi
            st.session_state.questions_asked = set()

    def translate_word(self, word, dictionary):
        """Dịch từ từ dictionary với xử lý capitalize"""
        word_title = word.title()
        return dictionary.get(word_title, dictionary.get(word, "Không rõ"))

    def declare_fact(self, fact_name, fact_value):
        """Thêm fact vào hệ thống và lưu vào danh sách facts"""
        # Kiểm tra xem fact đã tồn tại chưa để tránh trùng lặp
        for existing_fact in self.fact_history:
            if existing_fact[0] == fact_name and existing_fact[1] == fact_value:
                return True

        # Thêm fact mới
        self.declare(Fact(**{fact_name: fact_value}))
        self.fact_history.append((fact_name, fact_value))
        
        # Ghi log cho debugging
        # print(f"Added fact: {fact_name}({fact_value})")
        return True

    @measure_time
    def suggest_disease(self, disease, symptoms):
        """Hiển thị kết quả chẩn đoán bệnh với giao diện được cải thiện cho dark theme"""
        # Kiểm tra xem bệnh đã được chẩn đoán chưa
        if disease in self.diagnosed_diseases:
            return

        self.diagnosed_diseases.add(disease)
        
        # Tạo container với hiệu ứng thông báo thành công cho dark theme
        result_container = st.container()
        with result_container:
            st.markdown(f"""
            <div style="background-color:#103131; padding:15px; border-radius:8px; margin-bottom:20px; border:2px solid #0E8388;">
                <h2 style="color:#CBE4DE; text-align:center">Bạn có thể đang mắc bệnh: {disease}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Hiển thị triệu chứng trong một expander để tiết kiệm không gian
            with st.expander("Xem các triệu chứng đã nhận diện"):
                for symptom in symptoms:
                    st.markdown(f"<p style='color:#A5C9CA; margin:5px;'>• {symptom}</p>", unsafe_allow_html=True)

            # Tạo key duy nhất cho các nút
            info_key = f"info_{hash(disease)}_{hash(str(symptoms))}"
            restart_key = f"restart_{hash(disease)}_{hash(str(symptoms))}"

            col1, col2 = st.columns(2)

            # Hiển thị nút để xem thêm thông tin về bệnh
            if col1.button(f"Xem thêm thông tin về bệnh {disease}", key=info_key):
                # Dictionary chuyển đổi tên bệnh tiếng Việt sang tên file HTML tiếng Anh
                disease_dict = {
                    "Hội Chứng Suy Giảm Miễn Dịch Mắc Phải": "AIDS",
                    "Thiếu Máu": "Anemia",
                    "Viêm Khớp": "Arthritis",
                    "Hen Suyễn": "Asthma",
                    "Viêm Phế Quản": "Bronchitis",
                    "Viêm Kết Mạc": "Conjunctivitis",
                    "Vi-rút Corona": "Corona Virus",
                    "Xơ Vữa Động Mạch Vành": "Coronary Atherosclerosis",
                    "Mất Nước": "Dehydration",
                    "Sốt Xuất Huyết": "Dengue",
                    "Tiểu Đường": "Diabetes",
                    "Dị Ứng Mắt": "Eye Allergy",
                    "Viêm Dạ Dày": "Gastritis",
                    "Viêm Gan": "Hepatitis",
                    "Suy Giáp": "Hypothyroidism",
                    "Cúm": "Influenza",
                    "Sốt Rét": "Malaria",
                    "Béo Phì": "Obesity",
                    "Viêm Tụy": "Pancreatitis",
                    "Loét Dạ Dày": "Peptic Ulcer",
                    "Viêm Phổi": "Pneumonia",
                    "Bệnh Lao": "Tuberculosis",
                }
                
                # Lấy tên file tiếng Anh và hiển thị nội dung HTML
                disease_en = self.translate_word(disease, disease_dict)
                try:
                    with open(f"Treatment/html/{disease_en}.html", "r", encoding="utf-8") as f:
                        html_content = f.read()
                        
                    # Thêm CSS để định dạng nội dung HTML phù hợp với dark theme
                    html_content = f"""
                    <style>
                    body, html {{
                        background-color: transparent;
                        color: #E7F6F2;
                    }}
                    h1, h2, h3, h4, h5, h6 {{
                        color: #A5C9CA;
                    }}
                    p, li, ul, ol {{
                        color: #E7F6F2;
                    }}
                    a {{
                        color: #0E8388;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                    }}
                    th, td {{
                        border: 1px solid #395B64;
                        padding: 8px;
                        text-align: left;
                    }}
                    th {{
                        background-color: transparent;
                        color: #E7F6F2;
                    }}
                    tr:nth-child(even) {{
                        background-color: transparent;
                    }}
                    </style>
                    {html_content}
                    """
                    
                    with st.expander(f"📖 Thông tin chi tiết về {disease}", expanded=True):
                        components.html(html_content, height=600, scrolling=True)
                except FileNotFoundError:
                    st.error(f"Không tìm thấy tài liệu về bệnh {disease}. Vui lòng tham khảo ý kiến bác sĩ.")

            # Hiển thị nút để bắt đầu lại với hiệu ứng cảnh báo
            if col2.button("Bắt đầu lại", key=restart_key):
                # Reset toàn bộ trạng thái ứng dụng
                st.session_state.clear()
                self.diagnosed_diseases.clear()
                self.fact_history.clear()
                st.rerun()

        # Dừng chương trình sau khi chẩn đoán và hiển thị lời khuyên
        st.markdown("""
        <div style="padding:10px; margin-top:20px;">
            <p style="color:#A5C9CA;">⚠️ <b>Lưu ý:</b> Đây chỉ là kết quả chẩn đoán sơ bộ. Vui lòng tham khảo ý kiến bác sĩ để được tư vấn chi tiết.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    @measure_time
    def ask_question(self, question_text, options=None, question_type="yes_no", single_select=False):
        """Hiển thị câu hỏi trên giao diện Streamlit và nhận phản hồi với UI được cải thiện"""
        if options is None:
            options = []

        # Tạo key duy nhất cho câu hỏi
        question_key = f"q_{hash(question_text)}"
        logger.info(f"Processing question: {question_text} with key: {question_key}")
        
        # Đảm bảo rằng session_state.questions_asked đã được khởi tạo
        if 'questions_asked' not in st.session_state:
            logger.debug("Initializing questions_asked in session_state")
            st.session_state.questions_asked = set()
        
        # Theo dõi các câu hỏi đã hỏi để tránh hỏi lại
        if question_key in st.session_state and question_key in st.session_state.questions_asked:
            logger.debug(f"Question {question_key} already answered, returning cached value")
            return st.session_state[question_key]
            
        # Thêm câu hỏi vào danh sách các câu hỏi đã hỏi
        logger.debug(f"Adding question {question_key} to questions_asked")
        st.session_state.questions_asked.add(question_key)

        # Nếu câu hỏi đã được trả lời, trả về giá trị đã lưu
        if question_key in st.session_state:
            return st.session_state[question_key]

        # Nếu không, hiển thị câu hỏi và đợi phản hồi
        self.current_question = question_text
        
        # Tạo container để nhóm câu hỏi với giao diện đẹp hơn
        question_container = st.container()
        with question_container:
            if question_type == "yes_no":
                # Hiển thị câu hỏi với màu sắc phù hợp dark theme, nhưng không có background
                st.markdown(f"""
                <h3 style="color:#A5C9CA; margin-bottom:15px; padding-top:10px;">{question_text}</h3>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)

                # Tạo key duy nhất cho các nút
                yes_key = f"yes_{question_key}"
                no_key = f"no_{question_key}"

                if col1.button("✓ Có", key=yes_key):
                    st.session_state[question_key] = "có"
                    st.rerun()
                elif col2.button("✗ Không", key=no_key):
                    st.session_state[question_key] = "không"
                    st.rerun()

                # Nếu chưa có câu trả lời, dừng thực thi
                if question_key not in st.session_state:
                    st.stop()

                return st.session_state[question_key]

            elif question_type == "multi_select":
                # Hiển thị câu hỏi với màu sắc phù hợp dark theme, nhưng không có background
                st.markdown(f"""
                <h3 style="color:#A5C9CA; margin-bottom:15px; padding-top:10px;">{question_text}</h3>
                """, unsafe_allow_html=True)

                # Tạo key duy nhất cho selectbox/multiselect
                select_key = f"select_{question_key}"
                submit_key = f"submit_{question_key}"

                if single_select:
                    # Sử dụng radio cho câu hỏi chỉ chọn một đáp án (trực quan hơn selectbox)
                    selected_option = st.radio(
                        "Chọn một lựa chọn phù hợp:",
                        options,
                        key=select_key,
                        format_func=lambda x: f"📍 {x}" if x != "không có" else "❌ Không có triệu chứng"
                    )

                    if st.button("✓ Xác nhận", key=submit_key, type="primary"):
                        st.session_state[question_key] = [selected_option]
                        st.rerun()
                else:
                    # Sử dụng multiselect có định dạng cho câu hỏi chọn nhiều đáp án
                    selected_options = st.multiselect(
                        "Chọn tất cả các lựa chọn phù hợp:",
                        options,
                        key=select_key,
                        format_func=lambda x: f"📍 {x}" if x != "không có" else "❌ Không có triệu chứng"
                    )

                    if st.button("✓ Xác nhận", key=submit_key, type="primary"):
                        if not selected_options:
                            st.session_state[question_key] = ["không có"]
                        else:
                            st.session_state[question_key] = selected_options
                        st.rerun()

                # Nếu chưa có câu trả lời, dừng thực thi
                if question_key not in st.session_state:
                    st.stop()

                return st.session_state[question_key]

        # Không nên đến được đây
        return None

    def yes_no(self, input_str):
        """Wrapper cho phương thức ask_question với loại câu hỏi yes_no"""
        return self.ask_question(input_str, question_type="yes_no")

    def multi_input(self, input_str, options=[], single_select=False):
        """Wrapper cho phương thức ask_question với loại câu hỏi multi_select"""
        # Tạo bản sao các options để tránh thay đổi mảng gốc
        options_with_none = options.copy()
        
        # Thêm tùy chọn "không có" nếu chưa có
        if "không có" not in options_with_none:
            options_with_none.append("không có")
            
        return self.ask_question(
            input_str, 
            options=options_with_none,
            question_type="multi_select",
            single_select=single_select
        )

    @measure_time
    def check_disease_rules(self):
        """Kiểm tra các luật bệnh từ knowledge.pl dựa vào triệu chứng của người dùng"""
        if not self.fact_history:
            logger.warning("No facts in history, skipping disease check")
            return
            
        # Hiển thị thông báo đang xử lý
        with st.spinner("Đang phân tích triệu chứng..."):
            try:
                # Đặt lại Prolog engine trước khi thêm facts mới
                logger.debug("Retracting all existing facts from Prolog engine")
                prolog.retractall("symptom(_,_)")
                
                # Theo dõi số fact được thêm thành công
                facts_added = 0
                
                # Đưa các facts (symptom(có/không)) vào hệ Prolog
                logger.info(f"Adding {len(self.fact_history)} facts to Prolog engine")
                for fact_name, fact_value in self.fact_history:
                    prolog_fact_name = convert_to_prolog_fact(fact_name)
                    prolog_value = "yes" if fact_value == "có" else "no"
                    try:
                        prolog.assertz(f"{prolog_fact_name}({prolog_value})")
                        facts_added += 1
                        logger.debug(f"Added fact: {prolog_fact_name}({prolog_value})")
                    except Exception as e:
                        logger.error(f"Error adding fact {fact_name}: {str(e)}")
                        st.error(f"Lỗi khi thêm fact {fact_name}: {str(e)}")
                        
                if facts_added == 0:
                    logger.warning("No facts could be added to the knowledge base")
                    st.warning("Không thể thêm triệu chứng vào cơ sở tri thức. Vui lòng thử lại.")
                    return

                # Tạo tập hợp các triệu chứng người dùng xác nhận
                user_symptoms = set([
                    f"{convert_to_prolog_fact(name)}({'yes' if value == 'có' else 'no'})"
                    for name, value in self.fact_history
                ])
                logger.info(f"User has {len(user_symptoms)} symptoms")
                
                # Tạo danh sách các bệnh có thể chẩn đoán
                potential_diseases = []
                
                # Tìm các bệnh phù hợp với triệu chứng
                logger.info("Checking disease rules against user symptoms")
                for disease in DISEASE_NAMES:
                    try:
                        # Truy vấn danh sách triệu chứng cần thiết cho bệnh
                        result = list(prolog.query(f"rule({disease}, Symptoms)"))
                        if not result:
                            logger.debug(f"No rule found for disease: {disease}")
                            continue

                        disease_symptoms = set(result[0]["Symptoms"])
                        logger.debug(f"Disease {disease} requires {len(disease_symptoms)} symptoms")
                        
                        # Tính tỷ lệ phù hợp giữa triệu chứng người dùng và triệu chứng của bệnh
                        matching_symptoms = disease_symptoms.intersection(user_symptoms)
                        if not matching_symptoms:
                            logger.debug(f"No matching symptoms for disease: {disease}")
                            continue
                            
                        match_ratio = len(matching_symptoms) / len(disease_symptoms)
                        logger.info(f"Disease {disease} has match ratio: {match_ratio:.2f} ({len(matching_symptoms)}/{len(disease_symptoms)})")
                        
                        # Nếu tất cả triệu chứng phù hợp hoặc >= 85% triệu chứng phù hợp
                        if disease_symptoms.issubset(user_symptoms) or match_ratio >= 0.85:
                            symptoms_list = [
                                convert_symptom_to_vietnamese(symptom)
                                for symptom in matching_symptoms
                            ]
                            disease_name = DISEASE_NAMES.get(disease, disease)
                            logger.info(f"Found potential disease: {disease_name} with match ratio: {match_ratio:.2f}")
                            potential_diseases.append((disease_name, symptoms_list, match_ratio))

                    except Exception as e:
                        logger.error(f"Error checking disease {disease}: {str(e)}", exc_info=True)
                        st.error(f"Lỗi khi kiểm tra bệnh {disease}: {str(e)}")
                
                # Sắp xếp các bệnh tiềm năng theo tỷ lệ phù hợp
                potential_diseases.sort(key=lambda x: x[2], reverse=True)
                logger.info(f"Found {len(potential_diseases)} potential diseases")
                
                # Hiển thị kết quả chẩn đoán cho bệnh có tỷ lệ phù hợp cao nhất
                if potential_diseases:
                    disease_name, symptoms_list, match_ratio = potential_diseases[0]
                    logger.info(f"Suggesting disease: {disease_name} with confidence: {match_ratio:.2f}")
                    self.suggest_disease(disease_name, symptoms_list)
                else:
                    # Kiểm tra xem có đủ triệu chứng để chẩn đoán không
                    if len(self.fact_history) < 5:
                        logger.info("Not enough symptoms to diagnose (less than 5)")
                        st.info("Cần thêm thông tin để chẩn đoán chính xác. Vui lòng trả lời thêm các câu hỏi.")
                    else:
                        logger.warning("No matching diseases found despite having enough symptoms")
                        st.warning("Các triệu chứng không khớp với bất kỳ bệnh nào trong cơ sở dữ liệu. Vui lòng tham khảo ý kiến bác sĩ.")
            except Exception as e:
                logger.error(f"Error in check_disease_rules: {str(e)}", exc_info=True)
                st.error(f"Đã xảy ra lỗi khi phân tích triệu chứng: {str(e)}")
                st.error("Vui lòng thử lại hoặc liên hệ với quản trị viên hệ thống.")

    @DefFacts()
    def _initial_action_(self):
        """Initial fact để khởi động hệ thống"""
        yield Fact(action="engine_start")

    @Rule(Fact(action="engine_start"))
    def getUserInfo(self):
        st.markdown("""
        <h2 style="color:#A5C9CA; text-align:center; margin:20px 0;">Thông tin cá nhân</h2>
        <hr style="border-color:#395B64; margin-bottom:20px;">
        """, unsafe_allow_html=True)

        # Tạo một form với thiết kế dark theme
        with st.container():
            st.markdown("""
            <p style="color:#D8D9DA; margin-bottom:15px;">Vui lòng cung cấp thông tin cá nhân của bạn để bắt đầu chẩn đoán.</p>
            """, unsafe_allow_html=True)
            
            name = st.text_input("Tên của bạn là gì?", key="name")
            if not name:
                st.stop()

            gender = st.selectbox("Giới tính của bạn là gì?", ["Nam", "Nữ"], key="gender")
            if not gender:
                st.stop()

            st.markdown(f"""
            <p style="color:#CBE4DE; margin-top:15px;"><b>Xin chào {name}!</b></p>
            <p style="color:#CBE4DE;">Vui lòng trả lời các câu hỏi sau để được chẩn đoán.</p>
            """, unsafe_allow_html=True)

        self.declare_fact("name", name)
        self.declare_fact("gender", gender.lower())
        self.declare_fact("action", "questionnaire")

    # Thêm một phương thức helper để tạo header
    def create_dark_header(self, text):
        """Tạo header phù hợp với dark theme không có background"""
        return st.markdown(f"""
        <h2 style="color:#A5C9CA; text-align:center; margin:20px 0; padding-top:10px;">{text}</h2>
        <hr style="border-color:#395B64; margin-bottom:20px;">
        """, unsafe_allow_html=True)
        
    @Rule(Fact(action="questionnaire"))
    def askBasicQuestions(self):
        self.create_dark_header("Câu hỏi cơ bản")

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
        if red_eyes == "có":
            self.askEyeStatus()

    def askRelatedToFever(self):
        self.create_dark_header("Câu hỏi liên quan đến sốt thường")

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
        self.create_dark_header("Câu hỏi liên quan đến mất cảm giác thèm ăn")

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
        self.create_dark_header("Câu hỏi về viêm khớp")

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
        self.create_dark_header("Câu hỏi liên quan đến mệt mỏi")

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
            if fact[0] in ["frequent_urination", "weight_loss", "irratabiliry", "blurred_vision", "frequent_infections",
                           "sores"] and fact[1] == "có":
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

        confidence = self.yes_no(
            "Bạn có cảm thấy thiếu tự tin và lòng tự trọng thấp trong các hoạt động hàng ngày không?")
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

        heaviness = self.yes_no(
            "Bạn có cảm giác nặng nề hoặc thắt ngực, thường ở vùng trung tâm của ngực, có thể lan ra cánh tay, cổ, hàm, lưng hoặc dạ dày không?")
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

        short_breath_severe = self.yes_no(
            "Bạn có cảm thấy khó thở khi làm các hoạt động bình thường hoặc thậm chí khi nghỉ ngơi không?")
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
    try:
        logger.info("Starting Medical Expert System application")
        
        # Hiển thị header với thiết kế phù hợp với dark theme
        st.markdown("""
        <div style="padding:10px; border-radius:10px; margin-bottom:20px;">
            <h1 style="color:#D8D9DA; text-align:center">Hệ Thống Chẩn Đoán Y Tế</h1>
            <p style="color:#D8D9DA; text-align:center">Chẩn đoán sơ bộ dựa trên triệu chứng</p>
        </div>
        """, unsafe_allow_html=True)
        
        # CSS cho dark theme
        st.markdown("""
        <style>
        .stAlert {
            background-color: transparent !important;
            color: #E7F6F2 !important;
            border: 1px solid #395B64 !important;
        }
        .stAlert p {
            color: #E7F6F2 !important;
        }
        .stSpinner {
            filter: invert(0.8) !important;
        }
        div.stButton > button {
            background-color: #0E8388;
            color: white;
        }
        div.stButton > button:hover {
            background-color: #2E4F4F;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Tạo sidebar với thông tin ứng dụng
        with st.sidebar:
            st.image("https://img.icons8.com/color/96/000000/medical-doctor.png", width=100)
            st.markdown("""
            <div style="background-color:#213555; padding:10px; border-radius:5px; margin-bottom:10px;">
                <h2 style="color:#D8D9DA; text-align:center">Thông tin</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color:#2C3333; padding:10px; border-radius:5px; border:1px solid #395B64; margin-bottom:10px;">
                <p style="color:#A5C9CA;">Đây là hệ thống chẩn đoán y tế sử dụng hệ thống chuyên gia và lập luận dựa trên luật.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color:#772222; padding:10px; border-radius:5px; border:1px solid #913838; margin-bottom:20px;">
                <p style="color:#E7F6F2;">⚠️ <b>Lưu ý:</b> Kết quả chẩn đoán chỉ mang tính tham khảo. Vui lòng tham khảo ý kiến bác sĩ để có chẩn đoán chính xác.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Các tab thông tin trong sidebar
            tab1, tab2 = st.tabs(["Về ứng dụng", "Hướng dẫn"])
            
            with tab1:
                st.markdown("""
                <div style="background-color:#2C3333; padding:10px; border-radius:5px; margin-bottom:10px;">
                    <p style="color:#A5C9CA;"><b>Hệ thống chẩn đoán y tế</b> này sử dụng:</p>
                    <ul style="color:#A5C9CA;">
                        <li>Hệ thống chuyên gia Experta</li>
                        <li>Lập luận Prolog</li>
                        <li>Giao diện Streamlit</li>
                    </ul>
                    <p style="color:#A5C9CA;">Hệ thống có thể chẩn đoán 22 loại bệnh khác nhau dựa trên các triệu chứng mà bạn cung cấp.</p>
                </div>
                """, unsafe_allow_html=True)
                
            with tab2:
                st.markdown("""
                <div style="background-color:#2C3333; padding:10px; border-radius:5px;">
                    <p style="color:#A5C9CA;"><b>Hướng dẫn sử dụng:</b></p>
                    <ol style="color:#A5C9CA;">
                        <li>Nhập thông tin cá nhân</li>
                        <li>Trả lời các câu hỏi về triệu chứng</li>
                        <li>Nhận kết quả chẩn đoán sơ bộ</li>
                        <li>Xem thêm thông tin về bệnh nếu cần</li>
                    </ol>
                    <p style="color:#A5C9CA;">Bạn có thể bắt đầu lại quá trình bất kỳ lúc nào bằng cách nhấn nút "Bắt đầu lại".</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Nút bắt đầu lại trong thanh sidebar
            if st.sidebar.button("🔄 Bắt đầu lại", type="primary"):
                logger.info("User requested restart")
                st.session_state.clear()
                st.rerun()

        # Tạo container chính cho ứng dụng
        main_container = st.container()
        with main_container:
            # Khởi tạo và chạy hệ thống chuyên gia
            try:
                logger.info("Initializing expert system engine")
                engine = HeThongChuanDoanYTe()
                with st.spinner("Đang khởi tạo hệ thống..."):
                    engine.reset()
                    logger.info("Engine reset successful, starting execution")
                    engine.run()
                    logger.info("Engine execution completed")
                
                # Nếu không có bệnh nào được chẩn đoán sau khi chạy, hiển thị thông báo
                if not engine.diagnosed_diseases and 'name' in st.session_state:
                    logger.warning("No diseases diagnosed after completing the questionnaire")
                    st.warning("Các triệu chứng không khớp với bất kỳ bệnh nào trong cơ sở dữ liệu của chúng tôi. Vui lòng tham khảo ý kiến bác sĩ hoặc thử lại với các triệu chứng khác.")
                    
                    # Nút bắt đầu lại
                    if st.button("Bắt đầu lại", type="primary"):
                        logger.info("User requested restart after no diagnosis")
                        st.session_state.clear()
                        st.rerun()
            except Exception as e:
                logger.error(f"Error during engine execution: {str(e)}", exc_info=True)
                st.error(f"Đã xảy ra lỗi khi chạy hệ thống: {str(e)}")
                st.error("Vui lòng làm mới trang và thử lại.")
                # Hiển thị nút làm mới trang
                if st.button("Làm mới trang", type="primary"):
                    st.rerun()
    
    except Exception as e:
        logger.error(f"Unexpected error in main application: {str(e)}", exc_info=True)
        st.error("Đã xảy ra lỗi không mong muốn trong ứng dụng.")
        st.error("Vui lòng làm mới trang và thử lại.")