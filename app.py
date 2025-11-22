import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# --- CẤU HÌNH APP ---
st.set_page_config(page_title="B2 First Master", page_icon="🎓", layout="wide")

# --- SIDEBAR: CÀI ĐẶT & MENU ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/2560px-Google_Gemini_logo.svg.png", width=150)
    st.title("🚀 Lộ trình B2 (179+)")
    
    # Nhập API Key
    api_key = st.text_input("Nhập Gemini API Key của bạn:", type="password")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
    
    menu = st.radio("Chọn tính năng:", ["🏠 Dashboard", "✍️ Writing Coach", "🧠 Smart Vocab", "📝 Quick Quiz"])
    
    st.info("💡 Mục tiêu: 179 điểm (Grade A)")

# --- HÀM HỖ TRỢ GỌI GEMINI ---
def ask_gemini(prompt):
    if not api_key:
        return "⚠️ Vui lòng nhập API Key ở thanh bên trái."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi: {e}"

# --- TRANG 1: DASHBOARD (THEO DÕI TIẾN ĐỘ) ---
if menu == "🏠 Dashboard":
    st.header("📅 Quản lý học tập hàng ngày")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Duolingo Streak", value="35 Day", delta="Keep going!")
    with col2:
        st.metric(label="Elsa Score", value="6.0", delta="+0.5 Goal")
    with col3:
        st.metric(label="Target Date", value="12/2025")

    st.subheader("✅ Check-list hôm nay")
    c1 = st.checkbox("Duolingo / Elsa (15p)")
    c2 = st.checkbox("Destination Unit (30p)")
    c3 = st.checkbox("Review Vocab (Anki)")
    
    if c1 and c2 and c3:
        st.balloons()
        st.success("Tuyệt vời! Bạn đã hoàn thành Deep Work hôm nay.")

# --- TRANG 2: WRITING COACH (CHẤM BÀI) ---
elif menu == "✍️ Writing Coach":
    st.header("Sửa lỗi & Nâng cấp bài viết (Format Cambridge)")
    
    input_text = st.text_area("Dán bài viết (Email/Essay/Report) của bạn vào đây:", height=200)
    
    if st.button("Chấm bài ngay"):
        with st.spinner("Gemini đang chấm bài..."):
            prompt = f"""
            Bạn là giám khảo chấm thi Cambridge B2 First. Hãy chấm đoạn văn sau:
            "{input_text}"
            
            Yêu cầu output format Markdown:
            1. **Đánh giá chung:** (Ước lượng band điểm)
            2. **Sửa lỗi chi tiết:** (Kẻ bảng: Lỗi sai -> Sửa lại -> Giải thích)
            3. **Nâng cấp từ vựng (C1 Level):** Gợi ý các từ vựng/cấu trúc "đắt" hơn để thay thế từ đơn giản trong bài.
            4. **Bài viết mẫu (Rewrite):** Viết lại đoạn văn trên chuẩn văn phong native.
            """
            result = ask_gemini(prompt)
            st.markdown(result)

# --- TRANG 3: SMART VOCAB (TỪ VỰNG SÂU) ---
elif menu == "🧠 Smart Vocab":
    st.header("Học từ vựng sâu (Deep Learning)")
    
    word = st.text_input("Nhập từ vựng bạn vừa gặp (VD: Ambitious):")
    
    if st.button("Phân tích từ này"):
        with st.spinner("Đang tra cứu Collocation và Context..."):
            prompt = f"""
            Tôi đang học từ: "{word}" để thi B2 First.
            Hãy giúp tôi:
            1. **Định nghĩa:** Ngắn gọn tiếng Anh & Việt.
            2. **Collocations (Quan trọng):** 5 cụm từ hay đi với từ này (Adjective + Noun, Verb + Noun...).
            3. **Word Formation:** Các dạng từ khác của nó (Noun, Adj, Adv).
            4. **Story:** Viết một câu chuyện cực ngắn (3 câu) chứa từ này để tôi dễ nhớ.
            """
            result = ask_gemini(prompt)
            st.markdown(result)

# --- TRANG 4: QUICK QUIZ (KIỂM TRA BÀI CŨ) ---
elif menu == "📝 Quick Quiz":
    st.header("Tạo đề thi từ nội dung sách Destination")
    
    topic = st.text_input("Nhập chủ đề ngữ pháp hoặc Unit bạn vừa học (VD: Present Perfect, Phrasal Verbs with 'Get'):")
    
    if st.button("Tạo Quiz"):
        with st.spinner("Đang soạn đề thi..."):
            prompt = f"""
            Tạo cho tôi 5 câu hỏi trắc nghiệm (Multiple Choice) về chủ đề: "{topic}".
            Độ khó: Cambridge B2 First.
            Cuối cùng mới hiện đáp án và giải thích chi tiết.
            """
            result = ask_gemini(prompt)
            st.markdown(result)
