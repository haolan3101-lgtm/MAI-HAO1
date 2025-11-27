import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="AI Giáo trình MH", page_icon="⚓")
st.title("⚓ AI GIÁO TRÌNH MH")
st.markdown("**Bản quyền:** Trung tá QNCN Mai Xuân Hảo")
st.markdown("---")

# --- CẤU HÌNH API ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Chưa nhập API Key!")
    st.stop()

# --- CẤU HÌNH MODEL ---
noi_dung_huan_luyen = """
Bạn là AI Giáo trình MH, bản quyền của Trung tá QNCN Mai Xuân Hảo.
Nhiệm vụ: Trợ lý ảo chuyên biệt soạn thảo văn bản, giáo trình, đề tài lĩnh vực Quân sự, Hải quân.
Phong cách: Chính quy, nghiêm túc, dùng từ ngữ quân sự chính xác, đúng điều lệnh.
Luôn bắt đầu bằng câu chào: "Chào thủ trưởng/đồng chí, AI Giáo trình MH (Bản quyền của Trung tá QNCN Mai Xuân Hảo) sẵn sàng hỗ trợ."
"""

generation_config = {
  "temperature": 0.7,
  "max_output_tokens": 8192,
}

# Sử dụng model 1.5 flash (Bắt buộc để chạy được system instruction)
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction=noi_dung_huan_luyen
)

# --- GIAO DIỆN CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhập yêu cầu tại đây..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang soạn thảo..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"Lỗi: {e}")
