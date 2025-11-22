import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# --- 1. CẤU HÌNH TRANG (Phải để đầu tiên) ---
st.set_page_config(page_title="B2 First Master", page_icon="🎓", layout="wide")

# --- 2. SIDEBAR: MENU & CẤU HÌNH AI ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/2560px-Google_Gemini_logo.svg.png", width=150)
    st.title("🚀 Lộ trình B2 (179+)")
    
    # --- QUAN TRỌNG: ĐỊNH NGHĨA MENU TRƯỚC KHI XỬ LÝ AI ---
    menu = st.radio("Chọn tính năng:", ["🏠 Dashboard", "✍️ Writing Coach", "🧠 Smart Vocab", "📝 Quick Quiz"])
    
    st.divider()
    
    # --- CẤU HÌNH AI (Đọc từ Secrets) ---
    model = None # Khởi tạo biến model mặc định là None
    try:
        if 'GEMINI_API_KEY' in st.secrets:
            genai.configure(api_key=st.secrets['GEMINI_API_KEY'])
            model = genai.GenerativeModel('gemini-pro')
            st.success("✅ AI đã kết nối")
        else:
            st.error("⚠️ Chưa có API Key trong Secrets")
            st.info("Vào Settings -> Secrets để thêm GEMINI_API_KEY")
    except Exception as e:
        st.error(f"❌ Lỗi kết nối: {e}")

    st.info("💡 Mục tiêu: 179 điểm (Grade A)")

# --- 3. HÀM GỌI GEMINI (Xử lý lỗi nếu chưa có model) ---
def ask_gemini(prompt):
    if model is None:
        return "⚠️ Lỗi: AI chưa được kết nối. Vui lòng kiểm tra lại API Key trong phần Settings -> Secrets."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Lỗi khi gọi AI: {e}"

# --- 4. NỘI DUNG CHÍNH (MAIN CONTENT) ---

# === TRANG 1: DASHBOARD ===
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

# === TRANG 2: WRITING COACH ===
elif menu == "✍️ Writing Coach":
    st.header("Sửa lỗi & Nâng cấp bài viết (Format Cambridge)")
    st.caption("Paste bài Essay hoặc Email của bạn vào đây, AI sẽ chấm điểm theo thang B2/C1.")
    
    input_text = st.text_area("Nội dung bài viết:", height=200)
    
    if st.button("Chấm bài ngay"):
        if not input_text:
            st.warning("Vui lòng nhập nội dung bài viết.")
        else:
            with st.spinner("Gemini đang chấm bài..."):
                prompt = f"""
                Bạn là giám khảo chấm thi Cambridge B2 First. Hãy chấm đoạn văn sau:
                "{input_text}"
                
                Yêu cầu output format Markdown:
                1. **Đánh giá chung:** (Ước lượng band điểm trên thang 190)
                2. **Sửa lỗi chi tiết:** (Kẻ bảng: Lỗi sai -> Sửa lại -> Giải thích)
                3. **Nâng cấp từ vựng (C1 Level):** Gợi ý các từ vựng/cấu trúc "đắt" hơn để thay thế từ đơn giản.
                4. **Bài viết mẫu (Rewrite):** Viết lại đoạn văn trên chuẩn văn phong native.
                """
                result = ask_gemini(prompt)
                st.markdown(result)

# === TRANG 3: SMART VOCAB ===
elif menu == "🧠 Smart Vocab":
    st.header("Học từ vựng sâu (Deep Learning)")
    st.caption("Nhập từ vựng để lấy Collocations và ngữ cảnh.")
    
    word = st.text_input("Nhập từ vựng (VD: Ambitious):")
    
    if st.button("Phân tích từ này"):
        if not word:
            st.warning("Vui lòng nhập từ vựng.")
        else:
            with st.spinner("Đang tra cứu Collocation và Context..."):
                prompt = f"""
                Tôi đang học từ: "{word}" để thi B2 First.
                Hãy giúp tôi:
                1. **Định nghĩa:** Ng
