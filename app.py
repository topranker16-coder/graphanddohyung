import streamlit as st
import cv2
import numpy as np
import glob
import random

# 스마트폰 & PC 겸용 레이아웃 설정
st.set_page_config(
    page_title="🔥 전체 소방 도시기호 스마트 암기장",
    page_icon="🎴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 모바일 & PC 반응형 CSS
st.markdown('''
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    .main .block-container {
        max-width: 500px !important;
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    .flashcard-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #cbd5e1;
        border-radius: 20px;
        padding: 20px 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
        text-align: center;
        margin-bottom: 15px;
        position: relative;
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

# 초고화질 업스케일링 & 선명도 보정 함수 (캔버스 패딩)
def enhance_and_pad(crop_bgr, target_w=500, target_h=180):
    if crop_bgr is None or crop_bgr.size == 0:
        return np.ones((target_h, target_w, 3), dtype=np.uint8) * 255
        
    ch, cw = crop_bgr.shape[:2]
    if ch > 10 and cw > 10:
        crop_bgr = crop_bgr[2:ch-2, 2:cw-2]

    # 1. Lanczos4 3.2배 고화질 확대
    up = cv2.resize(crop_bgr, (0, 0), fx=3.2, fy=3.2, interpolation=cv2.INTER_LANCZOS4)
    
    # 2. 언샤프 마스크 선명도 보정
    kernel = np.array([[0, -0.25, 0], [-0.25, 2.0, -0.25], [0, -0.25, 0]])
    sharpened = cv2.filter2D(up, -1, kernel)
    
    # 3. 배경 노이즈 제거 (순백색 #FFFFFF 정화)
    gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)
    _, bg_mask = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY)
    sharpened[bg_mask == 255] = 255
    
    # 4. 캔버스 규격 맞춤 및 중앙 정렬
    sh, sw = sharpened.shape[:2]
    max_w = target_w - 30
    max_h = target_h - 20
    
    scale = min(max_w / sw, max_h / sh)
    nw, nh = max(1, int(sw * scale)), max(1, int(sh * scale))
    
    fit_img = cv2.resize(sharpened, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    
    canvas = np.ones((target_h, target_w, 3), dtype=np.uint8) * 255
    off_x = (target_w - nw) // 2
    off_y = (target_h - nh) // 2
    
    canvas[off_y:off_y+nh, off_x:off_x+nw] = fit_img
    return cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)

# 저장소 내 모든 이미지 파일(.jpg, .png, .jpeg)에서 소방기호 표 전체(100여 개+) 추출
@st.cache_data
def load_all_cards():
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
                        hd_sym = enhance_and_pad(sym_crop)
                        hd_name = enhance_and_pad(name_crop)
                        
                        cards.append({
                            "id": len(cards) + 1,
                            "symbol": hd_sym,  # 앞면: 선명한 기호 그림
                            "name": hd_name    # 뒷면: 선명한 정답 명칭
                        })
                    p += 2
                else:
                    p += 1
    return cards

cards = load_all_cards()

# 세션 상태 관리
if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0
if "is_flipped" not in st.session_state:
    st.session_state.is_flipped = False
if "known_set" not in st.session_state:
    st.session_state.known_set = set()

st.title("🔥 소방기호 원본 도식 암기장")

if not cards:
    st.warning("⚠️ 저장소에서 소방기호 표 이미지를 찾지 못했습니다. 원본 교재 이미지 파일(.jpg/.png)이 올라왔는지 확인해 주세요!")
else:
    total_c = len(cards)
    st.caption(f"📱 교재 원본 이미지에서 총 **{total_c}개**의 전체 소방 도시기호 카드가 빠짐없이 추출되었습니다!")

    tab1, tab2 = st.tabs(["🎴 플래시카드 학습", "📚 기호 전체보기"])

    with tab1:
        curr_idx = st.session_state.card_idx % total_c
        curr_c = cards[curr_idx]

        # 암기 진도율
        known_cnt = len(st.session_state.known_set)
        prog_val = min(1.0, known_cnt / total_c)
        st.progress(prog_val)
        st.caption(f"📊 암기 진도율: {total_c}개 중 {known_cnt}개 완료 ({int(prog_val*100)}%)")

        # 플래시카드 표시
        with st.container():
            if not st.session_state.is_flipped:
                st.markdown(f'<div class="flashcard-box"><div class="card-badge">앞면: 원본 기호 그림 ({curr_idx + 1} / {total_c})</div></div>', unsafe_allow_html=True)
                st.image(curr_c["symbol"], use_container_width=True)
                st.caption("👆 [🔄 카드 뒤집기]를 눌러 명칭을 확인하세요")
            else:
                st.markdown(f'<div class="flashcard-box"><div class="card-badge-back">뒷면: 원본 정답 명칭 ({curr_idx + 1} / {total_c})</div></div>', unsafe_allow_html=True)
                st.image(curr_c["name"], use_container_width=True)

        st.write("")
        
        # 컨트롤 버튼
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

    with tab2:
        st.subheader("📚 추출된 전체 소방기호 목록")
        for i, c in enumerate(cards):
            with st.expander(f"기호 #{i+1}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.caption("앞면 (기호)")
                    st.image(c["symbol"], use_container_width=True)
                with c2:
                    st.caption("뒷면 (명칭)")
                    st.image(c["name"], use_container_width=True)
