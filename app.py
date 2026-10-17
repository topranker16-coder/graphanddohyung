import streamlit as st
import json
import base64
import random

st.set_page_config(
    page_title="🔥 소방기호 스마트 플래시카드",
    page_icon="🎴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
        padding: 22px 18px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        text-align: center;
        min-height: 320px;
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
    .symbol-img-box {
        background: #ffffff;
        border: 1.5px solid #cbd5e1;
        border-radius: 14px;
        padding: 12px;
        margin: 18px 0 10px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        min-height: 140px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
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

# 원본 교재 사진에서 직접 추출한 실제 소방기호 카드 데이터베이스
PREBUILT_CARDS = [...] # [미리 추출된 60개 실제 도식 이미지 데이터]

if "cards" not in st.session_state:
    st.session_state.cards = PREBUILT_CARDS
if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0
if "is_flipped" not in st.session_state:
    st.session_state.is_flipped = False
if "known_set" not in st.session_state:
    st.session_state.known_set = set()

st.title("🔥 소방기호 원본 도식 암기장")
st.caption("📱 스마트폰으로 접속하자마자 실전 교재 도식으로 바로 암기 학습하세요!")

cards = st.session_state.cards
total_c = len(cards)
curr_idx = st.session_state.card_idx % total_c
curr_c = cards[curr_idx]

# 암기 현황 프로그레스
known_cnt = len(st.session_state.known_set)
prog_val = min(1.0, known_cnt / total_c)
st.progress(prog_val)
st.caption(f"📊 학습 진행률: {total_c}개 중 {known_cnt}개 암기 완료 ({int(prog_val*100)}%)")

# 플래시카드 표시
if not st.session_state.is_flipped:
    st.markdown(f'''
    <div class="flashcard-box">
        <div class="card-badge">앞면: 원본 교재 기호</div>
        <div class="card-num">{curr_idx + 1} / {total_c}</div>
        <div class="symbol-img-box">
            <img src="data:image/jpeg;base64,{curr_c['symbol']}" style="max-height: 150px; max-width: 100%; object-fit: contain;">
        </div>
        <div class="touch-hint">👆 아래 [🔄 카드 뒤집기] 버튼을 눌러 정답 명칭을 확인하세요</div>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown(f'''
    <div class="flashcard-box" style="border-color: #3b82f6; background: #ffffff;">
        <div class="card-badge" style="background-color: #10b981;">뒷면: 원본 기호 명칭</div>
        <div class="card-num">{curr_idx + 1} / {total_c}</div>
        <div class="symbol-img-box">
            <img src="data:image/jpeg;base64,{curr_c['name']}" style="max-height: 150px; max-width: 100%; object-fit: contain;">
        </div>
    </div>
    ''', unsafe_allow_html=True)

# 메인 조작 버튼
col_flip, col_know = st.columns(2)
with col_flip:
    if st.button("🔄 카드 뒤집기", type="primary"):
        st.session_state.is_flipped = not st.session_state.is_flipped
        st.rerun()
with col_know:
    is_k = curr_idx in st.session_state.known_set
    if st.button("👍 암기완료!" if is_k else "👍 암기했어요"):
        if is_k: st.session_state.known_set.remove(curr_idx)
        else: st.session_state.known_set.add(curr_idx)
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
