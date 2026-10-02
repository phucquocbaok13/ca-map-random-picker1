import streamlit as st
import random
import time

# Cấu hình trang web
st.set_page_config(
    page_title="Cá Mập Chọn Người",
    page_icon="🦈",
    layout="centered"
)

# Giao diện tiêu đề
st.title("🦈 CÁ MẬP CHỌN NGƯỜI NGẪU NHIÊN")
st.caption("Mini-game giải trí chọn người may mắn hoặc nhận thử thách / chịu phạt!")

# Sidebar - Quản lý danh sách người chơi
st.sidebar.header("⚙️ Danh sách tham gia")
default_players = "Nguyễn Văn A\nTrần Thị B\nLê Văn C\nPhạm Thị D\nHoàng Văn E"

input_text = st.sidebar.text_area(
    "Nhập danh sách tên (mỗi dòng 1 tên):",
    value=default_players,
    height=200
)

# Khởi tạo trạng thái Session State
if "players" not in st.session_state:
    st.session_state.players = [name.strip() for name in input_text.split("\n") if name.strip()]
if "history" not in st.session_state:
    st.session_state.history = []
if "last_chosen" not in st.session_state:
    st.session_state.last_chosen = None
if "last_mode" not in st.session_state:
    st.session_state.last_mode = None

# Nút cập nhật lại danh sách từ Sidebar
if st.sidebar.button("🔄 Cập nhật danh sách", use_container_width=True):
    st.session_state.players = [name.strip() for name in input_text.split("\n") if name.strip()]
    st.session_state.history = []
    st.session_state.last_chosen = None
    st.sidebar.success("Đã làm mới danh sách!")

# Giao diện chính
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("👥 Người chơi còn lại")
    if st.session_state.players:
        st.info(" | ".join(st.session_state.players))
    else:
        st.warning("⚠️️ Không còn ai trong danh sách!")

    # Lựa chọn chế độ
    mode = st.radio(
        "Chế độ chọn:",
        ["🎯 Chọn 1 người may mắn", "☠️ Cá mập 'xơi' dần (Loại trừ)"]
    )

    st.write("---")

    # Nút bấm hành động
    if st.button("🦈 CÁ MẬP ĐỚP! 🦈", type="primary", use_container_width=True):
        if not st.session_state.players:
            st.error("Vui lòng thêm người chơi ở thanh bên trái!")
        else:
            # Hiệu ứng chờ đợi
            with st.spinner("🦈 Cá mập đang lượn vòng quanh chọn mồi..."):
                time.sleep(1.2)

            chosen = random.choice(st.session_state.players)
            st.session_state.last_chosen = chosen
            st.session_state.last_mode = mode

            if mode == "☠️ Cá mập 'xơi' dần (Loại trừ)":
                st.session_state.players.remove(chosen)
                st.session_state.history.append(chosen)

    # Hiển thị hình ảnh cá mập há miệng và kết quả
    if st.session_state.last_chosen:
        try:
            st.image("shark.png", caption="🦈 CHOMP! Cá mập đã đớp trúng!", use_container_width=True)
        except Exception:
            st.warning("⚠️ Chưa tìm thấy file 'shark.png' trong thư mục GitHub!")

        if st.session_state.last_mode == "☠️ Cá mập 'xơi' dần (Loại trừ)":
            st.error(f"😱 **{st.session_state.last_chosen}** đã bị cá mập cắn trúng!")
        else:
            st.success(f"🎉 Chúc mừng **{st.session_state.last_chosen}** đã được cá mập lựa chọn!")

with col2:
    st.subheader("📜 Đã bị chọn")
    if st.session_state.history:
        for idx, item in enumerate(st.session_state.history, 1):
            st.write(f"**{idx}.** ☠️ {item}")
    else:
        st.caption("Chưa có lượt chọn nào.")

# Reset game
st.write("---")
if st.button("🔄 Đặt lại trò chơi ban đầu"):
    st.session_state.players = [name.strip() for name in input_text.split("\n") if name.strip()]
    st.session_state.history = []
    st.session_state.last_chosen = None
    st.rerun()
