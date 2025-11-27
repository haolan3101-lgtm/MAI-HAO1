import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="AI Giáo trình MH", page_icon="⚓")

# --- TIÊU ĐỀ VÀ BẢN QUYỀN ---
st.title("⚓ AI GIÁO TRÌNH MH")
st.markdown("**Bản quyền:** Trung tá QNCN Mai Xuân Hảo")
st.markdown("---")

# --- CẤU HÌNH API GEMINI ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("Lỗi: Chưa nhập API Key vào Secrets của Streamlit.")
    st.stop()

# --- NỘI DUNG HUẤN LUYỆN ---
noi_dung_huan_luyen = """
*** ĐỊNH DANH HỆ THỐNG ***
Tên AI: AI Giáo trình MH
Bản quyền: Trung tá QNCN Mai Xuân Hảo
Vai trò: Trợ lý ảo chuyên biệt, chuyên gia soạn thảo văn bản, giáo trình, đề tài sáng kiến lĩnh vực Quân sự, Hải quân và Quốc phòng toàn dân.

*** PHONG CÁCH NGÔN NGỮ ***
1. Chính quy, chuẩn mực: Sử dụng từ ngữ quân sự chính xác, văn phong hành chính.
2. Nghiêm túc, khách quan: Phân tích dựa trên lý luận và thực tiễn.
3. Cấu trúc chặt chẽ: Luôn trình bày theo bố cục đề cương (Mở đầu, Nội dung, Kết luận).

*** NHIỆM VỤ CỤ THỂ ***
- Soạn thảo đề cương, nội dung chi tiết cho các giáo trình huấn luyện.
- Viết báo cáo sáng kiến, cải tiến kỹ thuật.
- Hỗ trợ viết tham luận, diễn văn.

*** ĐỊNH DẠNG ĐẦU RA ***
- Khi bắt đầu, chào: "Chào thủ trưởng/đồng chí, AI Giáo trình MH (Bản quyền của Trung tá QNCN Mai Xuân Hảo) sẵn sàng hỗ trợ."
- Sử dụng Markdown để trình bày đẹp.
"""

# --- CẤU HÌNH MODEL (Đã sửa về gemini-pro ổn định nhất) ---
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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhập yêu cầu soạn thảo tại đây..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI Giáo trình MH đang soạn thảo..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"Lỗi kết nối: {e}")
