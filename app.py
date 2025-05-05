import streamlit as st
from expert import HeThongChuanDoanYTe, yes_no, multi_input, suggest_disease
import webbrowser

def main():
    st.set_page_config(page_title="Hệ Thống Chẩn Đoán Y Tế", page_icon="🏥")
    
    st.title("🏥 Hệ Thống Chẩn Đoán Y Tế")
    st.write("Chào mừng đến với Hệ thống Chuyên gia có thể giúp bạn chẩn đoán bệnh.")
    st.write("Vui lòng trả lời các câu hỏi sau để tìm ra bệnh và cách chữa trị")

    # Khởi tạo session state để lưu trữ thông tin
    if 'engine' not in st.session_state:
        st.session_state.engine = HeThongChuanDoanYTe()
        st.session_state.engine.reset()
        st.session_state.current_step = "start"
        st.session_state.answers = {}

    # Hàm xử lý câu hỏi có/không
    def handle_yes_no(question):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Có", key=f"yes_{question}"):
                st.session_state.answers[question] = "có"
                st.session_state.current_step = "next"
                st.rerun()
        with col2:
            if st.button("Không", key=f"no_{question}"):
                st.session_state.answers[question] = "không"
                st.session_state.current_step = "next"
                st.rerun()

    # Hàm xử lý câu hỏi nhiều lựa chọn
    def handle_multi_choice(question, options):
        st.write(question)
        selected = st.multiselect("Chọn các lựa chọn phù hợp:", options + ["không có"])
        if st.button("Tiếp tục", key=f"multi_{question}"):
            if "không có" in selected and len(selected) > 1:
                st.error("Không thể chọn 'không có' cùng với các giá trị khác")
            else:
                st.session_state.answers[question] = selected
                st.session_state.current_step = "next"
                st.rerun()

    # Xử lý các bước chẩn đoán
    if st.session_state.current_step == "start":
        st.write("### Thông tin cá nhân")
        name = st.text_input("Tên của bạn là gì?")
        gender = st.selectbox("Giới tính của bạn là gì?", ["nam", "nữ"])
        
        if st.button("Bắt đầu chẩn đoán"):
            st.session_state.answers["name"] = name
            st.session_state.answers["gender"] = gender
            st.session_state.current_step = "basic_questions"
            st.rerun()

    elif st.session_state.current_step == "basic_questions":
        st.write("### Câu hỏi cơ bản")
        handle_yes_no("Bạn có bị đỏ mắt không?")
        handle_yes_no("Bạn có cảm thấy mệt mỏi không?")
        handle_yes_no("Bạn có khó thở không?")
        handle_yes_no("Bạn có bị mất cảm giác thèm ăn không?")
        
        handle_multi_choice("Bạn có bị sốt không?", ["Sốt Thường", "Sốt Nhẹ", "Sốt Cao"])

    # Thêm các bước chẩn đoán khác tương tự...

    # Hiển thị kết quả chẩn đoán
    if st.session_state.current_step == "diagnosis":
        st.write("### Kết quả chẩn đoán")
        # Xử lý kết quả chẩn đoán từ engine
        pass

if __name__ == "__main__":
    main() 