import random
import time
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Cá Mập Giải Toán",
    page_icon="🦈",
    layout="centered"
)

# CSS tùy chỉnh giao diện Đại dương & Animation
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: #ffffff;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Trang chủ: Cá mập bơi quanh tiêu đề */
    .title-container {
        position: relative;
        text-align: center;
        padding: 40px 10px;
        margin-bottom: 20px;
    }
    .main-title {
        font-size: 38px;
        font-weight: 900;
        color: #00E5FF;
        text-shadow: 0 0 15px rgba(0,229,255,0.6), 3px 3px 0px #000;
        text-transform: uppercase;
        letter-spacing: 2px;
        display: inline-block;
        position: relative;
        z-index: 2;
    }
    .orbit-shark {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100%;
        height: 100%;
        margin-top: -50px;
        margin-left: -50%;
        pointer-events: none;
        animation: orbit 6s linear infinite;
        z-index: 3;
    }
    @keyframes orbit {
        0% { transform: rotate(0deg) translateX(140px) rotate(0deg); }
        100% { transform: rotate(360deg) translateX(140px) rotate(-360deg); }
    }
    
    /* Đường đua và Cá mập nhìn từ sau lưng */
    .track-container {
        position: relative;
        width: 100%;
        height: 280px;
        background: rgba(0, 30, 60, 0.7);
        border: 3px solid #00E5FF;
        border-radius: 15px;
        overflow: hidden;
        margin: 20px 0;
        box-shadow: inset 0 0 20px rgba(0,229,255,0.3);
    }
    .track-line {
        position: absolute;
        top: 0;
        left: 50%;
        width: 4px;
        height: 100%;
        background: dashed #00E5FF;
        transform: translateX(-50%);
    }
    
    /* Cá mập 2D bơi nhìn từ sau lưng */
    .shark-rear {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        transition: bottom 0.8s ease-in-out;
        animation: swimTail 0.6s infinite alternate ease-in-out;
    }
    @keyframes swimTail {
        0% { transform: translateX(-50%) rotate(-3deg); }
        100% { transform: translateX(-50%) rotate(3deg); }
    }
    
    /* Nút chọn lớp học */
    .grade-btn {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        border: none;
        color: white;
        padding: 15px 25px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(56,239,125,0.4);
        cursor: pointer;
        width: 100%;
        margin-bottom: 10px;
    }
    
    /* Cánh cửa vật cản */
    .door-box {
        background: linear-gradient(145deg, #1e3c72, #2a5298);
        border: 3px solid #FFD700;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: #fff;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- NGÂN HÀNG CÂU HỎI TOÁN HỌC VIỆT NAM (LỚP 6 - LỚP 9) ---
MATH_DATA = {
    6: [
        {"q": "Chặng 1: Tính giá trị của biểu thức: 15 + 25 : 5", "options": ["20", "8"], "ans": "20", "exp": "Thực hiện phép chia trước: 25 : 5 = 5, sau đó 15 + 5 = 20."},
        {"q": "Chặng 2: Tìm x biết x - 7 = 18", "options": ["x = 25", "x = 11"], "ans": "x = 25", "exp": "x = 18 + 7 = 25."},
        {"q": "Chặng 3: Kết quả của phép tính 3³ là bao nhiêu?", "options": ["27", "9"], "ans": "27", "exp": "3³ = 3 × 3 × 3 = 27."},
        {"q": "Chặng 4: Phân số nào dưới đây bằng phân số 2/3?", "options": ["4/6", "5/6"], "ans": "4/6", "exp": "Rút gọn 4/6 cho 2 ta được 2/3."}
    ],
    7: [
        {"q": "Chặng 1: Kết quả của phép tính (-2,5) + 1,5 là:", "options": ["-1", "-4"], "ans": "-1", "exp": "(-2,5) + 1,5 = -(2,5 - 1,5) = -1."},
        {"q": "Chặng 2: Tìm x biết x / 4 = 3 / 2", "options": ["x = 6", "x = 12"], "ans": "x = 6", "exp": "x = (4 × 3) / 2 = 6."},
        {"q": "Chặng 3: Tổng số đo ba góc trong một tam giác bằng:", "options": ["180°", "360°"], "ans": "180°", "exp": "Theo định lý tổng ba góc trong một tam giác."},
        {"q": "Chặng 4: Cho y tỉ lệ thuận với x theo hệ số k = 3. Khi x = 4 thì y bằng:", "options": ["12", "7"], "ans": "12", "exp": "y = k × x = 3 × 4 = 12."}
    ],
    8: [
        {"q": "Chặng 1: Khai triển hằng đẳng thức (x + 2)² - x² thu được:", "options": ["4x + 4", "2x + 4"], "ans": "4x + 4", "exp": "(x² + 4x + 4) - x² = 4x + 4."},
        {"q": "Chặng 2: Nghiệm của phương trình 2x - 8 = 0 là:", "options": ["x = 4", "x = -4"], "ans": "x = 4", "exp": "2x = 8 => x = 4."},
        {"q": "Chặng 3: Tam giác vuông có 2 cạnh góc vuông là 3cm và 4cm. Cạnh huyền bằng:", "options": ["5 cm", "7 cm"], "ans": "5 cm", "exp": "Theo định lý Pitago: √(3² + 4²) = √25 = 5 cm."},
        {"q": "Chặng 4: Phân tích đa thức x² - 9 thành nhân tử:", "options": ["(x - 3)(x + 3)", "(x - 9)(x + 1)"], "ans": "(x - 3)(x + 3)", "exp": "Áp dụng hằng đẳng thức a² - b² = (a - b)(a + b)."}
    ],
    9: [
        {"q": "Chặng 1: Căn bậc hai số học của 81 là:", "options": ["9", "-9"], "ans": "9", "exp": "Căn bậc hai số học luôn mang giá trị không âm: √81 = 9."},
        {"q": "Chặng 2: Nghiệm của phương trình x² - 5x + 6 = 0 là:", "options": ["x = 2 và x = 3", "x = -2 và x = -3"], "ans": "x = 2 và x = 3", "exp": "(x - 2)(x - 3) = 0 => x = 2 hoặc x = 3."},
        {"q": "Chặng 3: Tam giác vuông có cạnh đối bằng 3, cạnh huyền bằng 5. Sin của góc là:", "options": ["0,6", "0,8"], "ans": "0,6", "exp": "sin = Đổi / Huyền = 3 / 5 = 0,6."},
        {"q": "Chặng 4: Đồ thị hàm số y = 2x + 1 đi qua điểm nào?", "options": ["(1, 3)", "(1, 2)"], "ans": "(1, 3)", "exp": "Thay x = 1 vào y = 2(1) + 1 = 3."}
    ]
}

# --- KHỞI TẠO STATE ---
if "state" not in st.session_state:
    st.session_state.state = "HOME" # HOME, PLAYING, GAME_OVER, VICTORY
if "grade" not in st.session_state:
    st.session_state.grade = 6
if "step" not in st.session_state:
    st.session_state.step = 0 # 0, 1, 2, 3 (4 vật cản)

# --- VẼ CÁ MẬP 2D NHÌN TỪ SAU LƯNG (SVG) ---
def draw_shark_rear():
    return """
    <svg width="70" height="80" viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg">
        <!-- Vây ngực trái & phải -->
        <path d="M 20 70 Q 0 80 10 95 Q 35 85 30 70 Z" fill="#1e5799"/>
        <path d="M 80 70 Q 100 80 90 95 Q 65 85 70 70 Z" fill="#1e5799"/>
        <!-- Thân cá mập hình thoi/oval nhìn từ sau -->
        <ellipse cx="50" cy="65" rx="28" ry="40" fill="#2980b9"/>
        <ellipse cx="50" cy="65" rx="20" ry="32" fill="#3498db"/>
        <!-- Vây lưng nhọn hướng lên trên -->
        <path d="M 50 25 Q 43 45 50 65 Q 57 45 50 25 Z" fill="#1a5276"/>
        <!-- Vây đuôi vẫy phía sau -->
        <path d="M 50 100 L 30 120 L 50 110 L 70 120 Z" fill="#1b4f72"/>
    </svg>
    """

# --- VẼ CÁ MẬP CẦM CÚP VÀNG (SVG VICTORY) ---
def draw_shark_trophy():
    return """
    <svg width="220" height="220" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <!-- Hào quang -->
        <circle cx="100" cy="100" r="90" fill="rgba(255, 215, 0, 0.2)" />
        <!-- Cá mập -->
        <path d="M 40 100 Q 40 40 100 40 Q 160 40 160 100 Q 160 150 100 150 Z" fill="#3498db"/>
        <!-- Bụng trắng -->
        <ellipse cx="100" cy="110" rx="35" ry="30" fill="#ecf0f1"/>
        <!-- Mắt vui vẻ -->
        <circle cx="75" cy="70" r="6" fill="#000"/>
        <circle cx="125" cy="70" r="6" fill="#000"/>
        <!-- Mắt cười -->
        <path d="M 85 95 Q 100 115 115 95" stroke="#000" stroke-width="4" fill="none"/>
        <!-- Cúp vàng -->
        <path d="M 85 110 L 115 110 L 110 135 L 90 135 Z" fill="#f1c40f" stroke="#d4ac0d" stroke-width="2"/>
        <path d="M 80 90 L 120 90 L 115 112 L 85 112 Z" fill="#f39c12"/>
        <!-- Quai cúp -->
        <path d="M 80 95 Q 70 100 85 110" stroke="#f39c12" stroke-width="3" fill="none"/>
        <path d="M 120 95 Q 130 100 115 110" stroke="#f39c12" stroke-width="3" fill="none"/>
        <!-- Ngôi sao trên cúp -->
        <polygon points="100,95 102,100 107,100 103,103 105,108 100,105 95,108 97,103 93,100 98,100" fill="#fff"/>
    </svg>
    """

# ==========================================
# MÀN HÌNH 1: TRANG CHỦ (HOME)
# ==========================================
if st.session_state.state == "HOME":
    st.markdown("""
    <div class="title-container">
        <div class="main-title">🦈 CÁ MẬP GIẢI TOÁN 🦈</div>
        <div class="orbit-shark">
            <svg width="50" height="50" viewBox="0 0 100 100">
                <path d="M 20 50 Q 50 20 80 50 Q 50 80 20 50 Z" fill="#00E5FF"/>
                <polygon points="80,50 65,40 65,60" fill="#00E5FF"/>
                <circle cx="35" cy="45" r="4" fill="#000"/>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("🎯 Chọn cấp độ lớp học để bắt đầu thử thách:")
    
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

    st.info("💡 **Hướng dẫn:** Vượt qua 4 vật cản (cánh cửa đáp án) bằng cách chọn đáp án đúng để giúp Cá Mập giành Cúp Vàng!")

# ==========================================
# MÀN HÌNH 2: ĐANG CHƠI (PLAYING)
# ==========================================
elif st.session_state.state == "PLAYING":
    grade = st.session_state.grade
    step = st.session_state.step
    current_q = MATH_DATA[grade][step]
    
    st.title(f"🦈 Thử Thách Toán Lớp {grade}")
    
    # --- ĐƯỜNG ĐUA VÀ CÁ MẬP BƠI TỪ SAU LƯNG ---
    bottom_pos = 15 + (step * 20) # Cá mập tiến dần lên theo chặng
    
    track_html = f"""
    <div class="track-container">
        <div class="track-line"></div>
        
        <!-- 4 Vật cản (Cánh cửa) trên đường thẳng -->
        <div style="position: absolute; top: 15%; width: 100%; text-align: center; color: #FFD700; font-weight: bold;">🚪 CỬA 4</div>
        <div style="position: absolute; top: 35%; width: 100%; text-align: center; color: #FFD700; font-weight: bold;">🚪 CỬA 3</div>
        <div style="position: absolute; top: 55%; width: 100%; text-align: center; color: #FFD700; font-weight: bold;">🚪 CỬA 2</div>
        <div style="position: absolute; top: 75%; width: 100%; text-align: center; color: #FFD700; font-weight: bold;">🚪 CỬA 1</div>
        
        <!-- Cá mập nhìn từ sau lưng đang bơi tiến lên -->
        <div class="shark-rear" style="bottom: {bottom_pos}%;">
            {draw_shark_rear()}
        </div>
    </div>
    """
    st.markdown(track_html, unsafe_allow_html=True)
    
    # Hiển thị câu hỏi
    st.markdown(f"### ❓ {current_q['q']}")
    
    # Hiển thị 2 cánh cửa đáp án
    col_a, col_b = st.columns(2)
    
    opts = current_q["options"]
    
    with col_a:
        st.markdown(f'<div class="door-box">🚪 CÁNH CỬA A</div>', unsafe_allow_html=True)
        if st.button(f"🅰️ {opts[0]}", key="btn_a", use_container_width=True):
            if opts[0] == current_q["ans"]:
                st.balloons()
                st.success("🎉 ĐÚNG RỒI! Cá mập đã bơi qua cửa thành công!")
                time.sleep(1)
                if step + 1 >= 4:
                    st.session_state.state = "VICTORY"
                else:
                    st.session_state.step += 1
                st.rerun()
            else:
                st.session_state.state = "GAME_OVER"
                st.rerun()

    with col_b:
        st.markdown(f'<div class="door-box">🚪 CÁNH CỬA B</div>', unsafe_allow_html=True)
        if st.button(f"🅱️ {opts[1]}", key="btn_b", use_container_width=True):
            if opts[1] == current_q["ans"]:
                st.balloons()
                st.success("🎉 ĐÚNG RỒI! Cá mập đã bơi qua cửa thành công!")
                time.sleep(1)
                if step + 1 >= 4:
                    st.session_state.state = "VICTORY"
                else:
                    st.session_state.step += 1
                st.rerun()
            else:
                st.session_state.state = "GAME_OVER"
                st.rerun()

# ==========================================
# MÀN HÌNH 3: GAME OVER
# ==========================================
elif st.session_state.state == "GAME_OVER":
    st.markdown("""
    <div style="text-align: center; padding: 30px;">
        <h1 style="color: #FF1744; font-size: 50px; text-shadow: 0 0 20px #FF1744;">☠️ GAME OVER ☠️</h1>
        <h3>Rất tiếc! Bạn đã chọn sai cánh cửa vật cản.</h3>
        <p>Cá mập đã va phải chướng ngại vật!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.warning("⏳ Game sẽ tự động đưa bạn trở về Trang chủ trong giây lát...")
    
    time.sleep(3)
    st.session_state.state = "HOME"
    st.session_state.step = 0
    st.rerun()

# ==========================================
# MÀN HÌNH 4: CHIẾN THẮNG (VICTORY)
# ==========================================
elif st.session_state.state == "VICTORY":
    st.snow()
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #FFD700; font-size: 42px; text-shadow: 0 0 20px #FFD700;">🏆 XUẤT SẮC! CHIẾN THẮNG! 🏆</h1>
        <h3>Bạn đã giải đúng 4 bài toán và giúp Cá Mập chinh phục các cánh cửa!</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Hiển thị Cá mập cầm cúp
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        st.markdown(f'<div style="text-align:center;">{draw_shark_trophy()}</div>', unsafe_allow_html=True)
        
    st.write("---")
    if st.button("🏠 QUAY VỀ TRANG CHỦ", type="primary", use_container_width=True):
        st.session_state.state = "HOME"
        st.session_state.step = 0
        st.rerun()
