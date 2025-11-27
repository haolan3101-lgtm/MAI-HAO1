import streamlit as st
import google.generativeai as genai

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="AI Giáo trình MH", page_icon="⚓")
st.title("⚓ AI GIÁO TRÌNH MH")
st.markdown("**Bản quyền:** Trung tá QNCN Mai Xuân Hảo")
st.markdown("---")

# --- 2. KẾT NỐI API (Xử lý lỗi thông minh) ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Chưa nhập API Key. Hãy vào Settings -> Secrets để nhập.")
    st.stop()

# --- 3. CẤU HÌNH AI (Dùng bản gemini-pro ổn định nhất) ---
# Tắt bộ lọc an toàn để tránh bị chặn khi viết nội dung quân sự chuyên sâu
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    safety_settings=safety_settings
)

# --- 4. KỸ THUẬT "TIÊM NHẮC NHỞ" (SYSTEM PROMPT INJECTION) ---
# Đây là bí quyết: Nhét vai trò vào lịch sử chat ngay từ đầu
noi_dung_huan_luyen = """
Bạn là AI Giáo trình MH, Bản quyền của Trung tá QNCN Mai Xuân Hảo.
Vai trò: Trợ lý ảo chuyên biệt, chuyên gia soạn thảo văn bản, giáo trình, đề tài sáng kiến lĩnh vực Quân sự, Hải quân và Quốc phòng toàn dân.
Phong cách: Chính quy, chuẩn mực, sử dụng từ ngữ quân sự chính xác, văn phong hành chính.
Luôn bắt đầu câu trả lời bằng: "Chào thủ trưởng/đồng chí, AI Giáo trình MH (Bản quyền của Trung tá QNCN Mai Xuân Hảo) sẵn sàng hỗ trợ."
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        # Giả vờ như người dùng đã ra lệnh cài đặt cấu hình ngay từ đầu
        {"role": "user", "content": noi_dung_huan_luyen},
        # Giả vờ AI đã nhận lệnh
        {"role": "model", "content": "Rõ! Tôi đã nhận nhiệm vụ. Tôi là AI Giáo trình MH của Trung tá QNCN Mai Xuân Hảo. Xin chờ lệnh."}
    ]

# --- 5. HIỂN THỊ GIAO DIỆN CHAT ---
# Chỉ hiển thị tin nhắn từ cái thứ 2 trở đi (Giấu phần cài đặt đi cho đẹp)
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. XỬ LÝ KHI NGƯỜI DÙNG NHẬP LIỆU ---
if prompt := st.chat_input("Nhập yêu cầu soạn thảo tại đây..."):
    # Hiển thị câu hỏi
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI trả lời
    with st.chat_message("assistant"):
        with st.spinner("AI đang soạn thảo văn bản..."):
            try:
                # Gửi toàn bộ lịch sử chat (bao gồm cả phần huấn luyện ẩn)
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": [m["content"]]} 
                    for m in st.session_state.messages
                ])
                # Lấy phản hồi (không gửi lại prompt vì đã nằm trong history rồi)
                response = chat.send_message(prompt) 
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"Đã xảy ra lỗi kết nối: {e}")
