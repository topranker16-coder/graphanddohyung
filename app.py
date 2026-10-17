import streamlit as st
import cv2
import numpy as np
import glob
import random

st.set_page_config(
    page_title="🔥 소방기호 원본 도식 스마트 암기장",
    page_icon="🎴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 스마트폰 UI 커스텀 스타일링
st.markdown('''
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
        padding: 15px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        text-align: center;
        min-height: 280px;
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
        padding: 4px 12px;
        border-radius: 12px;
    }
    .card-num {
        position: absolute;
        top: 12px;
        right: 15px;
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .touch-hint {
        color: #94a3b8;
        font-size: 0.82rem;
        margin-top: 8px;
    }
    div.stButton > button {
        width: 100% !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 12px 0px !important;
        font-size: 0.95rem !important;
    }
</style>
''', unsafe_allow_html=True)

# 저장소의 이미지 파일들에서 108개 소방기호 카드를 자동 추출 (캐싱 처리)
@st.cache_data
def load_cards_from_repo():
    img_paths = sorted(glob.glob("*.jpg") + glob.glob("*.jpeg") + glob.glob("*.png"))
    cards = []
    
    for img_path in img_paths:
        img = cv2.imread(img_path)
        if img is None:
            continue
        h_img, w_img = img.shape[:2]
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        
        kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))
        kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
        
        horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_h)
        vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_v)
        
        table_grid = cv2.add(horizontal, vertical)
        contours, _ = cv2.findContours(table_grid, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        boxes = []
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
            
        for r_key in sorted(rows.keys()):
            r_boxes = sorted(rows[r_key], key=lambda b: b[0])
            if len(r_boxes) >= 2:
                sym_box = r_boxes[0]
                name_box = r_boxes[1]
                
                sx, sy, sw, sh = sym_box
                nx, ny, nw, nh = name_box
                
                sym_cell = cv2.cvtColor(img[sy:sy+sh, sx:sx+sw], cv2.COLOR_BGR2RGB)
                name_cell = cv2.cvtColor(img[ny:ny+nh, nx:nx+nw], cv2.COLOR_BGR2RGB)
                
                cell_gray = cv2.cvtColor(sym_cell, cv2.COLOR_RGB2GRAY)
                if np.sum(cell_gray < 220) > 30:
                    cards.append({
                        "symbol": sym_cell,
                        "name": name_cell
                    })
    return cards

cards = load_cards_from_repo()

# 세션 관리
if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0
if "is_flipped" not in st.session_state:
    st.session_state.is_flipped = False
if "known_set" not in st.session_state:
    st.session_state.known_set = set()

st.title("🔥 소방기호 원본 도식 암기장")

if not cards:
    st.warning("⚠️ 저장소에 교재 이미지 파일(.jpg)이 없습니다. 깃허브 저장소에 원본 이미지 파일들을 올려주세요!")
else:
    st.caption(f"📱 교재 이미지에서 총 **{len(cards)}개**의 원본 소방기호 카드가 준비되었습니다.")
    
    total_c = len(cards)
    curr_idx = st.session_state.card_idx % total_c
    curr_c = cards[curr_idx]

    # 암기 진도율
    known_cnt = len(st.session_state.known_set)
    prog_val = min(1.0, known_cnt / total_c)
    st.progress(prog_val)
    st.caption(f"📊 암기 진도율: {total_c}개 중 {known_cnt}개 암기 완료 ({int(prog_val*100)}%)")

    # 플래시카드 화면 (앞면: 실제 기호 / 뒷면: 실제 정답 명칭)
    if not st.session_state.is_flipped:
        st.markdown(f'''
        <div class="flashcard-box">
            <div class="card-badge">앞면: 원본 기호 그림</div>
            <div class="card-num">{curr_idx + 1} / {total_c}</div>
        </div>
        ''', unsafe_allow_html=True)
        st.image(curr_c["symbol"], use_container_width=True)
    else:
        st.markdown(f'''
        <div class="flashcard-box" style="border-color: #3b82f6; background: #ffffff;">
            <div class="card-badge" style="background-color: #10b981;">뒷면: 원본 정답 명칭</div>
            <div class="card-num">{curr_idx + 1} / {total_c}</div>
        </div>
        ''', unsafe_allow_html=True)
        st.image(curr_c["name"], use_container_width=True)

    # 버튼 영역
    col_flip, col_know = st.columns(2)
    with col_flip:
        if st.button("🔄 카드 뒤집기", type="primary"):
            st.session_state.is_flipped = not st.session_state.is_flipped
            st.rerun()
    with col_know:
        is_k = curr_idx in st.session_state.known_set
        if st.button("👍 암기완료!" if is_k else "👍 암기했어요"):
            if is_k:
                st.session_state.known_set.remove(curr_idx)
            else:
                st.session_state.known_set.add(curr_idx)
            st.rerun()

    st.write("")
    col_prev, col_rand, col_next = st.columns(3)
    with col_prev:
        if st.button("👈 이전"):
            st.session_state.card_idx = (st.session_state.card_idx - 1) % total_c
            st.session_state.is_flipped = False
            st.rerun()
    with col_rand:
        if st.button("🎲 섞기"):
            st.session_state.card_idx = random.randint(0, total_c - 1)
            st.session_state.is_flipped = False
            st.rerun()
    with col_next:
        if st.button("👉 다음"):
            st.session_state.card_idx = (st.session_state.card_idx + 1) % total_c
            st.session_state.is_flipped = False
            st.rerun()
