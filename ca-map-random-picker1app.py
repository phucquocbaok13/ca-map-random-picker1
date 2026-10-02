import base64
import os
import random
import time
import streamlit as st

# Cấu hình trang web
st.set_page_config(
    page_title="Cá Mập Chọn Người", page_icon="🦈", layout="centered"
)


# Hàm chuyển đổi ảnh cục bộ sang Base64 để hiển thị HTML/CSS
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None


# Hàm hiển thị hình ảnh cá mập có tên người chơi nằm trong vòm miệng
def display_shark_with_player(name, image_path="shark.png"):
    img_b64 = get_image_base64(image_path)
    if img_b64:
        html_code = f"""
        <div style="position: relative; width: 100%; max-width: 480px; margin: 15px auto; text-align: center;">
            <img src="data:image/png;base64,{img_b64}" style="width: 100%; height: auto; display: block; border-radius: 12px;">
            <div style="
                position: absolute;
                top: 55%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 42%;
                color: #FFEA00;
                font-size: 26px;
                font-weight: 900;
                font-family: 'Arial', sans-serif;
                text-align: center;
                word-wrap: break-word;
                line-height: 1.2;
                text-shadow: 2px 2px 5px #000000, -2px -2px 5px #000000, 2px -2px 5px #000000, -2px 2px 5px #000000;
            ">
                {name}
            </div>
        </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Chưa tìm thấy file 'shark.png' trong thư mục GitHub!")


# Giao diện tiêu đề
st.title("🦈 CÁ MẬP CHỌN NGƯỜI NGẪU NHIÊN")
st.caption("Mini-game giải trí chọn người may mắn hoặc nhận thử thách / chịu phạt!")

# Sidebar - Quản lý danh sách người chơi
st.sidebar.header("⚙️ Danh sách tham gia")
default_players = "Nguyễn Văn A\nTrần Thị B\nLê Văn C\nPhạm Thị D\nHoàng Văn E"

input_text = st.sidebar.text_area(
    "Nhập danh sách tên (mỗi dòng 1 tên):", value=default_players, height=200
)

# Khởi tạo trạng thái Session State
if "players" not in st.session_state:
    st.session_state.players = [
        name.strip() for name in input_text.split("\n") if name.strip()
    ]
if "history" not in st.session_state:
    st.session_state.history = []
if "last_chosen" not in st.session_state:
    st.session_state.last_chosen = None
if "last_mode" not in st.session_state:
    st.session_state.last_mode = None

# Nút cập nhật lại danh sách từ Sidebar
if st.sidebar.button("🔄 Cập nhật danh sách", use_container_width=True):
    st.session_state.players = [
        name.strip() for name in input_text.split("\n") if name.strip()
    ]
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
        ["🎯 Chọn 1 người may mắn", "☠️ Cá mập 'xơi' dần (Loại trừ)"],
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

    # Hiển thị kết quả & hình ảnh cá mập ngậm tên người chơi
    if st.session_state.last_chosen:
        display_shark_with_player(st.session_state.last_chosen)

        if st.session_state.last_mode == "☠️ Cá mập 'xơi' dần (Loại trừ)":
            st.error(f"😱 **{st.session_state.last_chosen}** đã nằm trong bụng cá mập!")
        else:
            st.success(
                f"🎉 Chúc mừng **{st.session_state.last_chosen}** đã được cá mập chọn!"
            )

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
    st.session_state.players = [
        name.strip() for name in input_text.split("\n") if name.strip()
    ]
    st.session_state.history = []
    st.session_state.last_chosen = None
    st.rerun()
