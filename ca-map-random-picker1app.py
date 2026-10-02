import streamlit as st
import random
import time

# Cấu hình trang web
st.set_page_config(
    page_title="Cá Mập Chọn Người",
    page_icon="🦈",
    layout="centered"
)

# Hiệu ứng CSS cho animation đớp
st.markdown("""
    <style>
    @keyframes chompAnimation {
        0% { transform: scale(1); }
        40% { transform: scale(1.15) translateY(-8px); }
        70% { transform: scale(0.95) translateY(8px); }
        100% { transform: scale(1) translateY(0); }
    }
    .chomp-box {
        animation: chompAnimation 0.5s ease-in-out;
        text-align: center;
    }
    .player-shuffle {
        font-size: 26px;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        padding: 10px;
        border: 2px dashed #FF4B4B;
        border-radius: 10px;
        background-color: #FFF0F0;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Link hình ảnh cá mập há miệng rộng và ngậm miệng đớp
SHARK_OPEN_URL = "https://images.unsplash.com/photo-1560275619-4662e36fa65c?w=800&auto=format&fit=crop"
SHARK_CLOSED_URL = "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&auto=format&fit=crop"

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

    # Vùng chứa hiệu ứng chuyển động
    anim_container = st.empty()

    # Nút bấm hành động
    if st.button("🦈 CÁ MẬP ĐỚP! 🦈", type="primary", use_container_width=True):
        if not st.session_state.players:
            st.error("Vui lòng thêm người chơi ở thanh bên trái!")
        else:
            # -------------------------------------------------------------
            # BƯỚC 1: HÁ MIỆNG RỘNG & XÁO TÊN LIÊN TỤC (TẠO CẢM GIÁC HỒI HỘP)
            # -------------------------------------------------------------
            for i in range(12):
                temp_chosen = random.choice(st.session_state.players)
                with anim_container.container():
                    st.image(SHARK_OPEN_URL, caption="😮 Cá mập đang HÁ MIỆNG RỘNG ngắm mồi...", use_container_width=True)
                    st.markdown(f'<div class="player-shuffle">🔍 Đang ngắm: {temp_chosen}</div>', unsafe_allow_html=True)
                time.sleep(0.12)

            # Chọn người chơi chính thức
            chosen = random.choice(st.session_state.players)
            st.session_state.last_chosen = chosen
            st.session_state.last_mode = mode

            if mode == "☠️ Cá mập 'xơi' dần (Loại trừ)":
                st.session_state.players.remove(chosen)
                st.session_state.history.append(chosen)

            # -------------------------------------------------------------
            # BƯỚC 2: CẮN SẬP HÀM (CHOMP!)
            # -------------------------------------------------------------
            with anim_container.container():
                st.image(SHARK_CLOSED_URL, caption="💥 CHOMP! Cá mập đã ĐÓNG HÀM CẮN TRÚNG!", use_container_width=True)
                st.markdown(f'<div class="chomp-box"><h2 style="color:#FF4B4B;">💥 CHOMP! ĐỚP TRÚNG: {chosen} 💥</h2></div>', unsafe_allow_html=True)
            
            time.sleep(1.2)
            anim_container.empty()

    # Hiển thị kết quả sau khi cắn xong
    if st.session_state.last_chosen:
        st.image(SHARK_CLOSED_URL, caption="🦈 Cá mập đã khép hàm sau khi đớp xong!", use_container_width=True)
        if st.session_state.last_mode == "☠️ Cá mập 'xơi' dần (Loại trừ)":
            st.error(f"😱 **{st.session_state.last_chosen}** đã bị cá mập cắn trúng!")
        else:
            st.balloons()
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
