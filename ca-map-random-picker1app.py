import random
import time
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Cá Mập Giải Toán", page_icon="🦈", layout="centered"
)


# --- HÀM PHÁT ÂM THANH BẰNG HTML5 ---
def play_sound(sound_url):
    """Nhúng thẻ audio ẩn tự động phát âm thanh từ đường dẫn URL."""
    sound_html = f"""
        <iframe src="{sound_url}" allow="autoplay" style="display:none"></iframe>
        <audio autoplay style="display:none;">
            <source src="{sound_url}" type="audio/mpeg">
        </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)


# --- KHAI BÁO CÁC ĐƯỜNG DẪN ÂM THANH (SFX) ---
SOUND_CORRECT = (
    "https://assets.mixkit.co/active_storage/sfx/2870/2870.wav"
)
SOUND_GAMEOVER = (
    "https://assets.mixkit.co/active_storage/sfx/948/948.wav"
)
SOUND_VICTORY = (
    "https://assets.mixkit.co/active_storage/sfx/2012/2012.wav"
)


# CSS Tùy chỉnh Giao diện Mobile Runner
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #0a1118 0%, #0f2027 50%, #203a43 100%);
        color: #ffffff;
        font-family: 'Montserrat', sans-serif;
    }
    
    .title-container {
        position: relative;
        text-align: center;
        padding: 30px 10px;
        margin-bottom: 20px;
    }
    .main-title {
        font-size: 36px;
        font-weight: 900;
        color: #00E5FF;
        text-shadow: 0 0 15px rgba(0,229,255,0.8), 3px 3px 0px #000;
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
        z-index: 2;
    }
    .orbit-shark {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100%;
        height: 100%;
        margin-top: -45px;
        margin-left: -50%;
        pointer-events: none;
        animation: orbit 6s linear infinite;
        z-index: 3;
    }
    @keyframes orbit {
        0% { transform: rotate(0deg) translateX(130px) rotate(0deg); }
        100% { transform: rotate(360deg) translateX(130px) rotate(-360deg); }
    }
    
    .runner-track {
        position: relative;
        width: 100%;
        height: 520px;
        background: linear-gradient(180deg, #030a12 0%, #0a2533 50%, #0d3b52 100%);
        border: 4px solid #00E5FF;
        border-radius: 20px;
        overflow: hidden;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(0,229,255,0.3);
    }
    
    .lane-divider {
        position: absolute;
        top: 0;
        left: 50%;
        width: 4px;
        height: 100%;
        border-left: 3px dashed rgba(0, 229, 255, 0.3);
        transform: translateX(-50%);
    }
    
    .gate-container {
        position: absolute;
        width: 90%;
        left: 5%;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }
    
    .shark-runner {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        transition: bottom 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        animation: swimTail 0.5s infinite alternate ease-in-out;
        z-index: 10;
    }
    @keyframes swimTail {
        0% { transform: translateX(-50%) rotate(-4deg); }
        100% { transform: translateX(-50%) rotate(4deg); }
    }
    
    div.stButton > button {
        border-radius: 12px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        padding: 12px 10px !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.4) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- CÂU HỎI TOÁN HỌC ---
MATH_DATA = {
    6: [
        {
            "q": "Chặng 1: Tính giá trị: 15 + 25 : 5",
            "options": ["20", "8"],
            "ans": "20",
        },
        {"q": "Chặng 2: Tìm x biết x - 7 = 18", "options": ["25", "11"], "ans": "25"},
        {
            "q": "Chặng 3: Kết quả của phép tính 3³ là:",
            "options": ["27", "9"],
            "ans": "27",
        },
        {
            "q": r"Chặng 4: Phân số nào bằng phân số $\frac{2}{3}$?",
            "options": ["4/6", "5/6"],
            "ans": "4/6",
        },
    ],
    7: [
        {
            "q": "Chặng 1: Kết quả (-2,5) + 1,5 là:",
            "options": ["-1", "-4"],
            "ans": "-1",
        },
        {
            "q": r"Chặng 2: Tìm x biết $\frac{x}{4} = \frac{3}{2}$",
            "options": ["6", "12"],
            "ans": "6",
        },
        {
            "q": "Chặng 3: Tổng 3 góc trong tam giác bằng:",
            "options": ["180°", "360°"],
            "ans": "180°",
        },
        {
            "q": "Chặng 4: Cho y = 3x. Khi x = 4 thì y bằng:",
            "options": ["12", "7"],
            "ans": "12",
        },
    ],
    8: [
        {
            "q": "Chặng 1: Khai triển (x + 2)² - x² thu được:",
            "options": ["4x + 4", "2x + 4"],
            "ans": "4x + 4",
        },
        {
            "q": "Chặng 2: Nghiệm của 2x - 8 = 0 là:",
            "options": ["x = 4", "x = -4"],
            "ans": "x = 4",
        },
        {
            "q": "Chặng 3: Tam giác vuông có 2 cạnh góc vuông 3cm, 4cm. Cạnh huyền:",
            "options": ["5 cm", "7 cm"],
            "ans": "5 cm",
        },
        {
            "q": "Chặng 4: Phân tích x² - 9 thành nhân tử:",
            "options": ["(x-3)(x+3)", "(x-9)(x+1)"],
            "ans": "(x-3)(x+3)",
        },
    ],
    9: [
        {
            "q": "Chặng 1: Căn bậc hai số học của 81 là:",
            "options": ["9", "-9"],
            "ans": "9",
        },
        {
            "q": "Chặng 2: Nghiệm x² - 5x + 6 = 0 là:",
            "options": ["x=2; x=3", "x=-2; x=-3"],
            "ans": "x=2; x=3",
        },
        {
            "q": "Chặng 3: Tam giác vuông có cạnh đối 3, cạnh huyền 5. Sin góc:",
            "options": ["0,6", "0,8"],
            "ans": "0,6",
        },
        {
            "q": "Chặng 4: Đồ thị y = 2x + 1 đi qua điểm:",
            "options": ["(1, 3)", "(1, 2)"],
            "ans": "(1, 3)",
        },
    ],
}

if "state" not in st.session_state:
    st.session_state.state = "HOME"
if "grade" not in st.session_state:
    st.session_state.grade = 6
if "step" not in st.session_state:
    st.session_state.step = 0


# --- HÀM TẠO VẼ CÁ MẬP 2D ---
def draw_shark_rear():
    return '<svg width="65" height="75" viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg"><path d="M 20 70 Q 0 80 10 95 Q 35 85 30 70 Z" fill="#1e5799"/><path d="M 80 70 Q 100 80 90 95 Q 65 85 70 70 Z" fill="#1e5799"/><ellipse cx="50" cy="65" rx="28" ry="40" fill="#2980b9"/><ellipse cx="50" cy="65" rx="20" ry="32" fill="#00E5FF"/><path d="M 50 20 Q 42 45 50 65 Q 58 45 50 20 Z" fill="#1a5276"/><path d="M 50 100 L 25 120 L 50 110 L 75 120 Z" fill="#0088CC"/></svg>'


# --- HÀM TẠO CÁNH CỬA CỔNG VÒM 2D ---
def draw_runner_gate(val_text, status="active"):
    if status == "passed":
        border_col = "#00FF66"
        bg_grad = "linear-gradient(180deg, #052e16 0%, #15803d 100%)"
        glow = "0 0 15px #00FF66"
        icon = "✅"
    elif status == "active":
        border_col = "#FFD700"
        bg_grad = "linear-gradient(180deg, #1e1b4b 0%, #4338ca 100%)"
        glow = "0 0 20px #FFD700"
        icon = "🚪"
    else:
        border_col = "#475569"
        bg_grad = "linear-gradient(180deg, #0f172a 0%, #1e293b 100%)"
        glow = "none"
        icon = "🔒"

    return f'<div style="width: 135px; height: 75px; background: {bg_grad}; border: 3px solid {border_col}; border-bottom: none; border-radius: 35px 35px 0 0; box-shadow: {glow}; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;"><div style="font-size: 16px;">{icon}</div><div style="font-size: 16px; color: #FFFFFF; font-weight: 900; text-shadow: 2px 2px 4px #000;">{val_text}</div></div>'


def draw_shark_trophy():
    return '<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="100" r="90" fill="rgba(255, 215, 0, 0.2)" /><path d="M 40 100 Q 40 40 100 40 Q 160 40 160 100 Q 160 150 100 150 Z" fill="#3498db"/><ellipse cx="100" cy="110" rx="35" ry="30" fill="#ecf0f1"/><circle cx="75" cy="70" r="6" fill="#000"/><circle cx="125" cy="70" r="6" fill="#000"/><path d="M 85 95 Q 100 115 115 95" stroke="#000" stroke-width="4" fill="none"/><path d="M 85 110 L 115 110 L 110 135 L 90 135 Z" fill="#f1c40f" stroke="#d4ac0d" stroke-width="2"/><path d="M 80 90 L 120 90 L 115 112 L 85 112 Z" fill="#f39c12"/><polygon points="100,95 102,100 107,100 103,103 105,108 100,105 95,108 97,103 93,100 98,100" fill="#fff"/></svg>'


# ==========================================
# 1. TRANG CHỦ (HOME)
# ==========================================
if st.session_state.state == "HOME":
    st.markdown(
        '<div class="title-container"><div class="main-title">🦈 CÁ MẬP GIẢI TOÁN 🦈</div><div class="orbit-shark"><svg width="50" height="50" viewBox="0 0 100 100"><path d="M 20 50 Q 50 20 80 50 Q 50 80 20 50 Z" fill="#00E5FF"/><polygon points="80,50 65,40 65,60" fill="#00E5FF"/><circle cx="35" cy="45" r="4" fill="#000"/></svg></div></div>',
        unsafe_allow_html=True,
    )

    st.write("---")
    st.subheader("🎯 Chọn cấp độ lớp học để tham gia đường đua:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 TOÁN LỚP 6", use_container_width=True, type="primary"):
            st.session_state.grade = 6
            st.session_state.step = 0
            st.session_state.state = "PLAYING"
            st.rerun()

        if st.button("📚 TOÁN LỚP 8", use_container_width=True, type="primary"):
            st.session_state.grade = 8
            st.session_state.step = 0
            st.session_state.state = "PLAYING"
            st.rerun()

    with col2:
        if st.button("📚 TOÁN LỚP 7", use_container_width=True, type="primary"):
            st.session_state.grade = 7
            st.session_state.step = 0
            st.session_state.state = "PLAYING"
            st.rerun()

        if st.button("📚 TOÁN LỚP 9", use_container_width=True, type="primary"):
            st.session_state.grade = 9
            st.session_state.step = 0
            st.session_state.state = "PLAYING"
            st.rerun()

    st.info(
        "🎮 **Luật chơi:** Điều khiển cá mập bơi qua 4 cánh cửa vật cản. Chọn đúng cánh cửa có đáp án chuẩn để mở đường!"
    )

# ==========================================
# 2. MÀN HÌNH CHƠI GAME (RUNNER TRACK)
# ==========================================
elif st.session_state.state == "PLAYING":
    grade = st.session_state.grade
    step = st.session_state.step
    questions = MATH_DATA[grade]
    current_q = questions[step]

    # --- LOGIC XÁO TRỘN ĐÁP ÁN NGẪU NHIÊN CHO MỖI CHẶNG ---
    step_key = f"{grade}_{step}"
    if (
        "current_step_key" not in st.session_state
        or st.session_state.current_step_key != step_key
    ):
        opts = list(current_q["options"])
        random.shuffle(opts)
        st.session_state.shuffled_opts = opts
        st.session_state.current_step_key = step_key

    opts = st.session_state.shuffled_opts

    st.markdown(f"### 🦈 TOÁN LỚP {grade} — {current_q['q']}")

    shark_bottom_pos = 8 + (step * 20)

    # Dựng đường đua và vật cản ghép nối
    gates_html = ""
    for idx in range(4):
        top_pos = 70 - (idx * 20)

        if idx < step:
            st_type = "passed"
            opt_a = "ĐÃ QUA"
            opt_b = "ĐÃ QUA"
        elif idx == step:
            st_type = "active"
            opt_a = opts[0]
            opt_b = opts[1]
        else:
            st_type = "locked"
            opt_a = "🔒"
            opt_b = "🔒"

        gate_a = draw_runner_gate(opt_a, st_type)
        gate_b = draw_runner_gate(opt_b, st_type)

        gates_html += f'<div class="gate-container" style="top: {top_pos}%;">{gate_a}{gate_b}</div>'

    track_ui = f'<div class="runner-track"><div class="lane-divider"></div>{gates_html}<div class="shark-runner" style="bottom: {shark_bottom_pos}%;">{draw_shark_rear()}</div></div>'
    st.markdown(track_ui, unsafe_allow_html=True)

    # Nút bấm chọn cửa
    st.write("👉 **Chọn cánh cửa đúng để Cá Mập bơi qua:**")
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button(
            f"🚪 CỬA TRÁI: {opts[0]}", key="door_a", use_container_width=True
        ):
            if opts[0] == current_q["ans"]:
                play_sound(SOUND_CORRECT)  # 🔊Âm thanh trả lời đúng
                st.balloons()
                st.success("🎉 ĐÚNG RỒI! Cá mập đã húc vỡ cửa tiến lên!")
                time.sleep(0.8)
                if step + 1 >= 4:
                    st.session_state.state = "VICTORY"
                else:
                    st.session_state.step += 1
                st.rerun()
            else:
                st.session_state.state = "GAME_OVER"
                st.rerun()

    with col_btn2:
        if st.button(
            f"🚪 CỬA PHẢI: {opts[1]}", key="door_b", use_container_width=True
        ):
            if opts[1] == current_q["ans"]:
                play_sound(SOUND_CORRECT)  # 🔊Âm thanh trả lời đúng
                st.balloons()
                st.success("🎉 ĐÚNG RỒI! Cá mập đã húc vỡ cửa tiến lên!")
                time.sleep(0.8)
                if step + 1 >= 4:
                    st.session_state.state = "VICTORY"
                else:
                    st.session_state.step += 1
                st.rerun()
            else:
                st.session_state.state = "GAME_OVER"
                st.rerun()

# ==========================================
# 3. MÀN HÌNH GAME OVER
# ==========================================
elif st.session_state.state == "GAME_OVER":
    play_sound(SOUND_GAMEOVER)  # 🔊Âm thanh thua cuộc

    st.markdown(
        '<div style="text-align: center; padding: 30px;"><h1 style="color: #FF1744; font-size: 52px; text-shadow: 0 0 20px #FF1744;">☠️ GAME OVER ☠️</h1><h3 style="color: #FFF;">Cá mập đã chọn sai cửa và va phải vật cản!</h3></div>',
        unsafe_allow_html=True,
    )

    st.warning("⏳ Game đang tự động đưa bạn trở về Trang chủ...")

    time.sleep(2.5)
    st.session_state.state = "HOME"
    st.session_state.step = 0
    st.rerun()

# ==========================================
# 4. MÀN HÌNH CHIẾN THẮNG (VICTORY)
# ==========================================
elif st.session_state.state == "VICTORY":
    play_sound(SOUND_VICTORY)  # 🔊Âm thanh chiến thắng

    st.snow()
    st.markdown(
        '<div style="text-align: center; padding: 20px;"><h1 style="color: #FFD700; font-size: 40px; text-shadow: 0 0 20px #FFD700;">🏆 BẠN ĐÃ CHIẾN THẮNG! 🏆</h1><h3>Chúc mừng bạn đã giúp Cá Mập vượt qua cả 4 vật cản xuất sắc!</h3></div>',
        unsafe_allow_html=True,
    )

    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        st.markdown(
            f'<div style="text-align:center;">{draw_shark_trophy()}</div>',
            unsafe_allow_html=True,
        )

    st.write("---")
    if st.button(
        "🏠 QUAY VỀ TRANG CHỦ", type="primary", use_container_width=True
    ):
        st.session_state.state = "HOME"
        st.session_state.step = 0
        st.rerun()
