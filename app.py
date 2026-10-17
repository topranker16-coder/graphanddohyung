import streamlit as st
import cv2
import numpy as np
import glob
import random

# 스마트폰 반응형 UI 설정
st.set_page_config(
    page_title="🔥 소방기호 원본 도식 스마트 암기장",
    page_icon="🎴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 모바일 커스텀 CSS 스타일링
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
    .card-badge {
        display: inline-block;
        background-color: #ef4444;
        color: white;
        font-size: 0.8rem;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    .card-badge-back {
        display: inline-block;
        background-color: #10b981;
        color: white;
        font-size: 0.8rem;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 12px;
        margin-bottom: 10px;
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

# 저장소 내 모든 이미지 파일(.png, .jpg, .jpeg)에서 소방기호 표 자동 추출
@st.cache_data
def load_cards_from_repo():
    all_files = glob.glob("*.[pP][nN][gG]") + glob.glob("*.[jJ][pP][gG]") + glob.glob("*.[jJ][pP][eE][gG]")
    img_paths = sorted(list(set(all_files)))
    cards = []
    
    for img_path in img_paths:
        img = cv2.imread(img_path)
        if img is None:
            continue
        h_img, w_img = img.shape[:2]
        if h_img < 200 or w_img < 200:
            continue
            
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

if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0
if "is_flipped" not in st.session_state:
    st.session_state.is_flipped = False
if "known_set" not in st.session_state:
    st.session_state.known_set = set()

st.title("🔥 소방기호 원본 도식 암기장")

if not cards:
    st.warning("⚠️ 저장소에서 소방기호 표 이미지(JPG, PNG)를 찾지 못했습니다. 원본 교재 이미지 파일을 깃허브 저장소에 올려주세요!")
else:
    st.caption(f"📱 교재 이미지에서 총 **{len(cards)}개**의 소방기호 카드를 불러왔습니다.")
    
    total_c = len(cards)
    curr_idx = st.session_state.card_idx % total_c
    curr_c = cards[curr_idx]

    # 암기 진도율
    known_cnt = len(st.session_state.known_set)
    prog_val = min(1.0, known_cnt / total_c)
    st.progress(prog_val)
    st.caption(f"📊 암기 진도율: {total_c}개 중 {known_cnt}개 암기 완료 ({int(prog_val*100)}%)")

    # 카드 표시 (Streamlit Native st.image 사용으로 에러 방지)
    with st.container():
        if not st.session_state.is_flipped:
            st.markdown(f'<div class="card-badge">앞면: 원본 기호 그림 ({curr_idx + 1} / {total_c})</div>', unsafe_allow_html=True)
            st.image(curr_c["symbol"], use_container_width=True)
            st.caption("👆 [🔄 카드 뒤집기]를 눌러 명칭을 확인하세요")
        else:
            st.markdown(f'<div class="card-badge-back">뒷면: 원본 정답 명칭 ({curr_idx + 1} / {total_c})</div>', unsafe_allow_html=True)
            st.image(curr_c["name"], use_container_width=True)

    st.write("")
    
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
