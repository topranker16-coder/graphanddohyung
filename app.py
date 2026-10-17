import io
import cv2
import numpy as np
import base64
import random
from PIL import Image
import streamlit as st

# 스마트폰 화면 최적화 설정
st.set_page_config(
    page_title="🔥 실제 원본 도식 100% 매칭 소방기호 암기장",
    page_icon="🎴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 모바일 전용 CSS 스타일링
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    .main .block-container {
        max-width: 480px !important;
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    .flashcard-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #cbd5e1;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        text-align: center;
        min-height: 330px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 15px;
        position: relative;
    }
    .card-badge {
        position: absolute;
        top: 12px;
        left: 15px;
        background-color: #ef4444;
        color: white;
        font-size: 0.75rem;
        font-weight: bold;
        padding: 3px 10px;
        border-radius: 12px;
    }
    .card-num {
        position: absolute;
        top: 12px;
        right: 15px;
        color: #64748b;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .symbol-img-box {
        background: #ffffff;
        border: 1px solid #94a3b8;
        border-radius: 12px;
        padding: 12px;
        margin: 15px 0;
        display: inline-block;
        max-width: 100%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .touch-hint {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 10px;
    }
    div.stButton > button {
        width: 100% !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 12px 0px !important;
    }
</style>
""", unsafe_allow_html=True)

# OpenCV 표 조각 자르기 함수
def extract_symbols_from_image(img_bgr):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))
    kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
    
    horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_h)
    vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_v)
    
    table_grid = cv2.add(horizontal, vertical)
    contours, _ = cv2.findContours(table_grid, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    boxes = []
    h_img, w_img = img_bgr.shape[:2]
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if 35 < w < w_img * 0.45 and 20 < h < h_img * 0.15:
            boxes.append((x, y, w, h))
            
    boxes = sorted(boxes, key=lambda b: (b[1], b[0]))
    filtered = []
    for b in boxes:
        x, y, w, h = b
        if not any(abs(x-fx)<10 and abs(y-fy)<10 for fx,fy,fw,fh in filtered):
            filtered.append(b)
            
    rows = {}
    for b in filtered:
        r_key = round(b[1] / 15) * 15
        if r_key not in rows:
            rows[r_key] = []
        rows[r_key].append(b)
        
    extracted_cards = []
    for r_key in sorted(rows.keys()):
        r_boxes = sorted(rows[r_key], key=lambda b: b[0])
        if len(r_boxes) >= 2:
            sym_box = r_boxes[0]
            name_box = r_boxes[1]
            
            sx, sy, sw, sh = sym_box
            nx, ny, nw, nh = name_box
            
            sym_cell = img_bgr[sy:sy+sh, sx:sx+sw]
            name_cell = img_bgr[ny:ny+nh, nx:nx+nw]
            
            cell_gray = cv2.cvtColor(sym_cell, cv2.COLOR_BGR2GRAY)
            if np.sum(cell_gray < 220) > 30:
                _, buf_s = cv2.imencode('.png', sym_cell)
                _, buf_n = cv2.imencode('.png', name_cell)
                
                b64_s = base64.b64encode(buf_s).decode('utf-8')
                b64_n = base64.b64encode(buf_n).decode('utf-8')
                
                extracted_cards.append({
                    "symbol_b64": f"data:image/png;base64,{b64_s}",
                    "name_b64": f"data:image/png;base64,{b64_n}"
                })
    return extracted_cards

st.title("🔥 실제 원본 도식 소방기호 암기장")
st.write("소방기호 표 사진을 올려주시면 **교재/도판 속 실제 기호 그림**을 그대로 잘라내어 100% 정밀 매칭 플래시카드를 만들어 드립니다!")

# 이미지 업로더
uploaded_files = st.file_uploader(
    "📸 소방기호 표/도판 사진들을 업로드하세요 (JPG, PNG)",
    type=['jpg', 'jpeg', 'png'],
    accept_multiple_files=True
)

if uploaded_files:
    all_cards = []
    for u_file in uploaded_files:
        file_bytes = np.asarray(bytearray(u_file.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img_bgr is not None:
            cards = extract_symbols_from_image(img_bgr)
            all_cards.extend(cards)
            
    if all_cards:
        st.success(f"✨ 업로드한 사진에서 총 **{len(all_cards)}개**의 실제 도식 기호를 성공적으로 잘라내었습니다!")
        st.session_state["extracted_cards"] = all_cards
    else:
        st.warning("⚠️ 이미지에서 표 구역을 찾지 못했습니다. 표 테두리가 또렷한 도판 사진을 올려주세요.")

# 세션 관리 및 플래시카드 렌더링
if "extracted_cards" in st.session_state and st.session_state["extracted_cards"]:
    cards_list = st.session_state["extracted_cards"]
    
    if "card_idx" not in st.session_state:
        st.session_state.card_idx = 0
    if "is_flipped" not in st.session_state:
        st.session_state.is_flipped = False
        
    curr_idx = st.session_state.card_idx % len(cards_list)
    curr_card = cards_list[curr_idx]
    
    st.divider()
    
    # 카드 앞/뒷면 표시
    if not st.session_state.is_flipped:
        card_html = f"""
        <div class="flashcard-box">
            <div class="card-badge">앞면: 원본 교재 기호</div>
            <div class="card-num">{curr_idx + 1} / {len(cards_list)}</div>
            <div class="symbol-img-box">
                <img src="{curr_card['symbol_b64']}" style="max-height: 160px; max-width: 100%; object-fit: contain;">
            </div>
            <div class="touch-hint">👆 아래 [🔄 카드 뒤집기]를 눌러 정답을 확인하세요</div>
        </div>
        """
    else:
        card_html = f"""
        <div class="flashcard-box" style="border-color: #3b82f6;">
            <div class="card-badge" style="background-color: #10b981;">뒷면: 원본 정답 명칭</div>
            <div class="card-num">{curr_idx + 1} / {len(cards_list)}</div>
            <div class="symbol-img-box">
                <img src="{curr_card['name_b64']}" style="max-height: 160px; max-width: 100%; object-fit: contain;">
            </div>
        </div>
        """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # 조작 버튼
    col_flip, col_next = st.columns(2)
    with col_flip:
        if st.button("🔄 카드 뒤집기", type="primary"):
            st.session_state.is_flipped = not st.session_state.is_flipped
            st.rerun()
    with col_next:
        if st.button("👉 다음 카드"):
            st.session_state.card_idx = (st.session_state.card_idx + 1) % len(cards_list)
            st.session_state.is_flipped = False
            st.rerun()
            
    col_prev, col_rand = st.columns(2)
    with col_prev:
        if st.button("👈 이전 카드"):
            st.session_state.card_idx = (st.session_state.card_idx - 1) % len(cards_list)
            st.session_state.is_flipped = False
            st.rerun()
    with col_rand:
        if st.button("🎲 무작위 섞기"):
            st.session_state.card_idx = random.randint(0, len(cards_list) - 1)
            st.session_state.is_flipped = False
            st.rerun()
else:
    st.info("💡 가지고 계신 **소방기호 표 이미지 파일(`1000011668.jpg` 등)**을 위에 선택해 보세요! 교재 속 진짜 기호 그림이 카드에 그대로 나타납니다.")
