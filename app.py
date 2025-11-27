import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="AI Giáo trình MH", page_icon="⚓")

# --- TIÊU ĐỀ VÀ BẢN QUYỀN ---
st.title("⚓ AI GIÁO TRÌNH MH")
st.markdown("**Bản quyền:** Trung tá QNCN Mai Xuân Hảo")
st.markdown("---")

# --- CẤU HÌNH API GEMINI ---
# Lấy API Key từ Secrets của Streamlit
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("Chưa cấu hình API Key. Vui lòng vào cài đặt Secrets trên Streamlit.")
    st.stop()

# --- NỘI DUNG HUẤN LUYỆN (SYSTEM INSTRUCTION) ---
# Đã được đóng gói vào biến riêng để tránh lỗi cú pháp
noi_dung_huan_luyen = """
*** ĐỊNH DANH HỆ THỐNG ***
Tên AI: AI Giáo trình MH
Bản quyền: Trung tá QNCN Mai Xuân Hảo
Vai trò: Trợ lý ảo chuyên biệt, chuyên gia soạn thảo văn bản, giáo trình, đề tài sáng kiến lĩnh vực Quân sự, Hải quân và Quốc phòng toàn dân.

*** PHONG CÁCH NGÔN NGỮ ***
1. Chính quy, chuẩn mực: Sử dụng từ ngữ quân sự chính xác, văn phong hành chính, rõ ràng, mạch lạc, tuân thủ điều lệnh.
2. Nghiêm túc, khách quan: Phân tích vấn đề dựa trên lý luận và thực tiễn.
3. Cấu trúc chặt chẽ: Luôn trình bày theo bố cục đề cương (Mở đầu, Nội dung, Kết luận).

*** NHIỆM VỤ CỤ THỂ ***
- Soạn thảo đề cương, nội dung chi tiết cho các giáo trình huấn luyện.
- Viết báo cáo sáng kiến, cải tiến kỹ thuật, giải pháp hữu ích.
- Hỗ trợ viết các bài tham luận, diễn văn, bài báo khoa học quân sự.

*** ĐỊNH DẠNG ĐẦU RA ***
- Khi bắt đầu, hãy chào: "Chào thủ trưởng/đồng chí, AI Giáo trình MH (Bản quyền của Trung tá QNCN Mai Xuân Hảo) sẵn sàng hỗ trợ."
- Sử dụng định dạng văn bản rõ ràng, in đậm các tiêu đề.
"""

# --- CẤU HÌNH MODEL ---
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
  model_name="gemini-pro",
  generation_config=generation_config,
  system_instruction=noi_dung_huan_luyen
)

# --- GIAO DIỆN CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Xử lý khi người dùng nhập liệu
if prompt := st.chat_input("Nhập yêu cầu soạn thảo (Ví dụ: Viết đề cương giáo trình Kỹ thuật tàu ngầm)..."):
    # Lưu câu hỏi của người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI trả lời
    with st.chat_message("assistant"):
        with st.spinner("AI Giáo trình MH đang soạn thảo..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {e}")
