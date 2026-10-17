import streamlit as st
import cv2
import numpy as np
import glob
import random

# 스마트폰 반응형 UI 설정
st.set_page_config(
    page_title="🔥 소방기호 초고화질 스마트 암기장",
    page_icon="🎴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 모바일 커스텀 CSS 스타일링 (이미지 선명도 crisp-edges 주입)
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
    /* 디스플레이 렌더링 픽셀 선명도 극대화 */
    img {
        image-rendering: -webkit-optimize-contrast !important;
        image-rendering: crisp-edges !important;
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
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

# 4배 초고화질 선명도 강화 및 순백색 정화 알고리즘
def enhance_cell_hd(crop_bgr):
    if crop_bgr is None or crop_bgr.size == 0:
        return np.ones((200, 400, 3), dtype=np.uint8) * 255
        
    # 1. 자잘한 테두리 검은 격자선 잘라내기
    ch, cw = crop_bgr.shape[:2]
    if ch > 12 and cw > 12:
        crop_bgr = crop_bgr[3:ch-3, 3:cw-3]

    # 2. 4배 초고해상도 Lanczos4 업스케일링
    up = cv2.resize(crop_bgr, (0, 0), fx=4.0, fy=4.0, interpolation=cv2.INTER_LANCZOS4)
    
    # 3. 언샤프 마스크 (Unsharp Masking) - 선과 글자 테두리를 칼같이 벼려냄
    blur = cv2.GaussianBlur(up, (0, 0), 3.0)
    sharpened = cv2.addWeighted(up, 1.8, blur, -0.8, 0)
    
    # 4. 종이 지저분한 회색 노이즈 제거 (순백색 #FFFFFF 정화)
    gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)
    _, bg_mask = cv2.threshold(gray, 205, 255, cv2.THRESH_BINARY)
    sharpened[bg_mask == 255] = 255
    
    # 5. 텍스트 및 소방기호 선 딥블랙 진하기 보정
    dark_mask = gray < 160
    sharpened[dark_mask] = np.clip(sharpened[dark_mask].astype(np.int16) - 35, 0, 255).astype(np.uint8)
    
    return cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)

# 저장소 내 교재 이미지에서 표를 자동 추출하여 HD 카드로 변환
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
        if h_img < 300 or w_img < 300:
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
            
        for r_k in sorted(rows.keys()):
            if r_k < 60:
                continue
                
            r_boxes = sorted(rows[r_k], key=lambda b: b[0])
            p = 0
            while p < len(r_boxes) - 1:
                b1 = r_boxes[p]      # 왼쪽: 정답 명칭
                b2 = r_boxes[p+1]    # 오른쪽: 도시기호 그림
                
                x1, y1, w1, h1 = b1
                x2, y2, w2, h2 = b2
                
                if (x2 - (x1 + w1)) < 50:
                    name_crop = img[y1:y1+h1, x1:x1+w1]
                    sym_crop = img[y2:y2+h2, x2:x2+w2]
                    
                    cell_gray = cv2.cvtColor(sym_crop, cv2.COLOR_BGR2GRAY)
                    if np.sum(cell_gray < 220) > 30:
                        # 4배 HD 선명도 보정 적용
                        hd_sym = enhance_cell_hd(sym_crop)
                        hd_name = enhance_cell_hd(name_crop)
                        
                        cards.append({
                            "symbol": hd_sym,  # 앞면: 또렷한 기호 그림
                            "name": hd_name    # 뒷면: 또렷한 정답 명칭
                        })
                    p += 2
                else:
                    p += 1
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
    st.warning("⚠️ 저장소에서 소방기호 표 이미지를 찾지 못했습니다. 원본 교재 이미지 파일(.jpg/.png)을 올려주세요!")
else:
    st.caption(f"📱 교재 이미지에서 총 **{len(cards)}개**의 HD 선명 카드를 불러왔습니다.")
    
    total_c = len(cards)
    curr_idx = st.session_state.card_idx % total_c
    curr_c = cards[curr_idx]

    # 암기 진도율
    known_cnt = len(st.session_state.known_set)
    prog_val = min(1.0, known_cnt / total_c)
    st.progress(prog_val)
    st.caption(f"📊 암기 진도율: {total_c}개 중 {known_cnt}개 완료 ({int(prog_val*100)}%)")

    # 카드 표시
    with st.container():
        if not st.session_state.is_flipped:
            st.markdown(f'<div class="card-badge">앞면: 원본 기호 그림 ({curr_idx + 1} / {total_c})</div>', unsafe_allow_html=True)
            st.image(curr_c["symbol"], use_container_width=True)
            st.caption("👆 [🔄 카드 뒤집기]를 눌러 명칭을 확인하세요")
        else:
            st.markdown(f'<div class="card-badge-back">뒷면: 원본 정답 명칭 ({curr_idx + 1} / {total_c})</div>', unsafe_allow_html=True)
            st.image(curr_c["name"], use_container_width=True)

    st.write("")
    
    # 조작 버튼
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
