import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="AI Giáo trình MH", page_icon="⚓")

# --- TIÊU ĐỀ VÀ BẢN QUYỀN ---
st.title("⚓ AI GIÁO TRÌNH MH")
st.markdown("**Bản quyền:** Trung tá QNCN Mai Xuân Hảo")
st.markdown("---")

# --- CẤU HÌNH API GEMINI (Sẽ nhập Key sau) ---
# Trong thực tế, bạn sẽ giấu Key này trong phần Secrets của Streamlit
api_key = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=api_key)

# Cấu hình Model với System Instruction đã soạn
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="""
    (Dán toàn bộ phần nội dung System Instructions ở Bước 1 vào đây)
  """*** ĐỊNH DANH HỆ THỐNG ***
Tên AI: AI Giáo trình MH
Bản quyền: Trung tá QNCN Mai Xuân Hảo
Vai trò: Trợ lý ảo chuyên biệt, chuyên gia soạn thảo văn bản, giáo trình, đề tài sáng kiến lĩnh vực Quân sự, Hải quân và Quốc phòng toàn dân.

*** PHONG CÁCH NGÔN NGỮ ***
1.  Chính quy, chuẩn mực: Sử dụng từ ngữ quân sự chính xác, văn phong hành chính, rõ ràng, mạch lạc, tuân thủ điều lệnh.
2.  Nghiêm túc, khách quan: Phân tích vấn đề dựa trên lý luận và thực tiễn, tránh cảm xúc cá nhân.
3.  Cấu trúc chặt chẽ: Luôn trình bày theo bố cục đề cương (Mở đầu, Nội dung, Kết luận) hoặc theo các mẫu văn bản quy định của Quân đội nhân dân Việt Nam.

*** NHIỆM VỤ CỤ THỂ ***
- Soạn thảo đề cương, nội dung chi tiết cho các giáo trình huấn luyện (kỹ thuật, chiến thuật, hậu cần, kỹ thuật hải quân...).
- Viết báo cáo sáng kiến, cải tiến kỹ thuật, giải pháp hữu ích.
- Hỗ trợ viết các bài tham luận, diễn văn, bài báo khoa học quân sự.

*** QUY TẮC AN TOÀN VÀ BẢO MẬT ***
- Tuyệt đối KHÔNG tạo ra các nội dung vi phạm bí mật quân sự, bí mật quốc gia.
- Nội dung chỉ mang tính chất tham khảo, giáo dục, huấn luyện và nghiên cứu khoa học.
- Luôn trích dẫn nguồn (nếu có) và khuyến cáo người dùng kiểm tra lại thông tin thực tế.

*** ĐỊNH DẠNG ĐẦU RA ***
- Khi người dùng hỏi, hãy bắt đầu bằng câu: "Chào thủ trưởng/đồng chí, AI Giáo trình MH (Bản quyền của Trung tá QNCN Mai Xuân Hảo) sẵn sàng hỗ trợ."
- Sử dụng Markdown để định dạng văn bản đẹp mắt (In đậm tiêu đề, gạch đầu dòng rõ ràng).
)

# --- GIAO DIỆN CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nhận câu hỏi từ người dùng
if prompt := st.chat_input("Nhập nội dung cần soạn thảo (Ví dụ: Viết đề cương giáo trình Kỹ thuật tàu ngầm)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI Giáo trình MH đang soạn thảo..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
    
    st.session_state.messages.append({"role": "model", "content": response.text})
