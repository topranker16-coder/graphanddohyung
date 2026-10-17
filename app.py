import streamlit as st
import random

# 스마트폰 & PC 겸용 반응형 레이아웃 설정
st.set_page_config(
    page_title="🔥 소방 도시기호 고화질 벡터 암기장",
    page_icon="🎴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 모바일 & PC 반응형 초고화질 CSS 주입
st.markdown("""
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
        padding: 24px 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
        text-align: center;
        min-height: 340px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 15px;
        position: relative;
    }
    
    .card-badge {
        position: absolute;
        top: 14px;
        left: 16px;
        background-color: #ef4444;
        color: white;
        font-size: 0.78rem;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 12px;
    }

    .card-num {
        position: absolute;
        top: 14px;
        right: 16px;
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .svg-container {
        margin: 20px 0 10px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }

    .svg-container svg {
        width: 160px;
        height: 160px;
        filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.08));
    }

    .card-title {
        color: #0f172a;
        font-size: 1.55rem;
        font-weight: 800;
        margin-top: 12px;
        margin-bottom: 8px;
    }

    .card-desc {
        color: #334155;
        font-size: 0.95rem;
        line-height: 1.55;
        margin-top: 10px;
        text-align: left;
        background-color: #f1f5f9;
        padding: 12px 15px;
        border-radius: 12px;
        width: 100%;
        box-sizing: border-box;
    }

    .exam-tip {
        color: #b91c1c;
        font-size: 0.88rem;
        font-weight: 600;
        margin-top: 8px;
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 8px 12px;
        border-radius: 4px;
        text-align: left;
        width: 100%;
        box-sizing: border-box;
    }

    .touch-hint {
        color: #94a3b8;
        font-size: 0.82rem;
        margin-top: 10px;
    }

    div.stButton > button {
        width: 100% !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 12px 0px !important;
        font-size: 0.95rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 한국 소방 화재안전기준(NFSC) 정식 도시기호 백터(SVG) DB
VECTOR_SYMBOLS_DB = [
    # 소화기류
    {
        "id": 1,
        "name": "ABC 분말 소화기",
        "category": "소화기류",
        "svg": """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="38" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><text x="50" y="61" font-size="34" font-weight="900" text-anchor="middle" fill="#0f172a" font-family="sans-serif">소</text></svg>""",
        "desc": "A급(일반), B급(유류), C급(전기) 화재에 범용으로 사용되는 대표적인 수동식 분말소화기 기호입니다.",
        "exam_tip": "📌 원 안에 한글 '소'자가 표기된 표준 기호입니다."
    },
    {
        "id": 2,
        "name": "자동확산 소화기",
        "category": "소화기류",
        "svg": """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="38" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><text x="50" y="61" font-size="34" font-weight="900" text-anchor="middle" fill="#0f172a" font-family="sans-serif">자</text></svg>""",
        "desc": "보일러실, 주방 등 화재 위험이 높은 천장에 설치되어 열 감지 시 자동으로 약제를 분사하는 소화기입니다.",
        "exam_tip": "📌 원 안에 한글 '자'자가 적혀 있습니다."
    },
    {
        "id": 3,
        "name": "주방자동소화장치 (자동식소화기)",
        "category": "소화기류",
        "svg": """<svg viewBox="0 0 100 100"><polygon points="50,10 90,50 50,90 10,50" fill="#0f172a"/><text x="50" y="60" font-size="28" font-weight="900" text-anchor="middle" fill="#ffffff" font-family="sans-serif">소</text></svg>""",
        "desc": "아파트 및 다세대주택 주방 가스/인덕션 상부에 의무 설치되는 자동소화장치 관련 기호입니다.",
        "exam_tip": "📌 검은색 마름모(다이아몬드) 바탕에 흰색 '소' 글자가 기재됩니다."
    },
    {
        "id": 4,
        "name": "이산화탄소 소화기 (CO2)",
        "category": "소화기류",
        "svg": """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="38" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><text x="50" y="62" font-size="36" font-weight="900" text-anchor="middle" fill="#0f172a" font-family="sans-serif">C</text></svg>""",
        "desc": "전기실, 변전실 등 잔여 약제 오염이 없어야 하는 장소에 설치되는 가스계 소화기입니다.",
        "exam_tip": "📌 원 안에 영문 알파벳 'C'가 표기됩니다."
    },
    {
        "id": 5,
        "name": "할로겐화합물 소화기",
        "category": "소화기류",
        "svg": """<svg viewBox="0 0 100 100"><polygon points="50,10 90,82 10,82" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><text x="50" y="68" font-size="30" font-weight="900" text-anchor="middle" fill="#0f172a" font-family="sans-serif">소</text></svg>""",
        "desc": "할론 또는 할로겐화합물 청정소화약제를 사용하는 소화기 기호입니다.",
        "exam_tip": "📌 정삼각형 테두리 안에 '소'자가 들어갑니다."
    },

    # 소화전 & 배관 설비
    {
        "id": 6,
        "name": "옥내소화전함",
        "category": "소화전/배관",
        "svg": """<svg viewBox="0 0 100 100"><rect x="15" y="15" width="70" height="70" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><polygon points="15,15 85,15 15,85" fill="#0f172a"/></svg>""",
        "desc": "건물 복도 등에 설치되어 초기 화재 시 관계자나 거주자가 직접 호스를 내어 진화하는 소화전입니다.",
        "exam_tip": "📌 사각형 대각선 기준 대각선 좌상단 절반이 검은색으로 칠해집니다."
    },
    {
        "id": 7,
        "name": "옥외소화전",
        "category": "소화전/배관",
        "svg": """<svg viewBox="0 0 100 100"><line x1="8" y1="50" x2="92" y2="50" stroke="#0f172a" stroke-width="5"/><path d="M 36 50 A 14 28 0 0 1 64 50" fill="none" stroke="#0f172a" stroke-width="5"/><text x="50" y="40" font-size="24" font-weight="900" text-anchor="middle" fill="#0f172a" font-family="sans-serif">H</text></svg>""",
        "desc": "건물 외부에 설치되어 소방대원이 외부에서 진화 작용을 하거나 용수를 공급받는 소화전입니다.",
        "exam_tip": "📌 배관 라인 위에 아치형 모양과 'H' 문자가 표시됩니다."
    },
    {
        "id": 8,
        "name": "쌍구형 송수구 (소방차 연결)",
        "category": "소화전/배관",
        "svg": """<svg viewBox="0 0 100 100"><line x1="50" y1="90" x2="50" y2="45" stroke="#0f172a" stroke-width="6"/><line x1="20" y1="45" x2="80" y2="45" stroke="#0f172a" stroke-width="6"/><circle cx="20" cy="28" r="14" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><circle cx="80" cy="28" r="14" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><line x1="20" y1="42" x2="20" y2="45" stroke="#0f172a" stroke-width="5"/><line x1="80" y1="42" x2="80" y2="45" stroke="#0f172a" stroke-width="5"/></svg>""",
        "desc": "화재 시 소방차가 건물의 스프링클러나 연결송수관 설비 배관으로 물을 펌핑해 넣는 외벽 연결구입니다.",
        "exam_tip": "📌 Y자형 배관 끝에 2개의 원형 입구가 그려집니다."
    },

    # 스프링클러 헤드류
    {
        "id": 9,
        "name": "스프링클러헤드 (폐쇄형 상향식)",
        "category": "헤드류",
        "svg": """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="34" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><circle cx="50" cy="50" r="12" fill="#0f172a"/><line x1="50" y1="5" x2="50" y2="16" stroke="#0f172a" stroke-width="5"/></svg>""",
        "desc": "헤드가 위쪽을 향하도록 설치되어 배관 상부에 위치하며 동파 방지나 들보 피하기용으로 사용됩니다.",
        "exam_tip": "📌 큰 원 중앙에 검은 색 작은 원이 채워진 형태입니다."
    },
    {
        "id": 10,
        "name": "스프링클러헤드 (폐쇄형 하향식)",
        "category": "헤드류",
        "svg": """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="34" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><line x1="50" y1="16" x2="50" y2="84" stroke="#0f172a" stroke-width="4"/><line x1="16" y1="50" x2="84" y2="50" stroke="#0f172a" stroke-width="4"/><path d="M 32 66 A 18 18 0 0 0 68 66 Z" fill="#0f172a"/></svg>""",
        "desc": "천장 아래로 살수하도록 설치되는 가장 일반적인 반자 천장용 스프링클러 헤드입니다.",
        "exam_tip": "📌 십자선 내부의 아래쪽 반원이 검은색으로 칠해져 있습니다."
    },
    {
        "id": 11,
        "name": "개방형 스프링클러헤드",
        "category": "헤드류",
        "svg": """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="34" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><line x1="50" y1="16" x2="50" y2="84" stroke="#0f172a" stroke-width="4"/><line x1="16" y1="50" x2="84" y2="50" stroke="#0f172a" stroke-width="4"/></svg>""",
        "desc": "감열부가 없어 밸브가 열리면 구역 내 모든 헤드에서 동시에 방수되는 헤드입니다 (드렌처/일제살수식).",
        "exam_tip": "📌 원 안에 십자선만 깔끔하게 그어져 있습니다."
    },

    # 밸브류
    {
        "id": 12,
        "name": "체크밸브 (역류방지)",
        "category": "밸브류",
        "svg": """<svg viewBox="0 0 100 100"><line x1="8" y1="50" x2="92" y2="50" stroke="#0f172a" stroke-width="5"/><polygon points="30,26 30,74 70,50" fill="#ffffff" stroke="#0f172a" stroke-width="5"/><line x1="70" y1="26" x2="70" y2="74" stroke="#0f172a" stroke-width="5"/></svg>""",
        "desc": "소방용수가 한쪽 방향으로만 흘러가고 반대쪽으로 역류하지 못하게 차단하는 밸브 기호입니다.",
        "exam_tip": "📌 화살표 삼각 기호 오른쪽 끝에 수직 막대가 접해 있습니다."
    },
    {
        "id": 13,
        "name": "준비작동식 밸브 (프리액션밸브)",
        "category": "밸브류",
        "svg": """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="36" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><text x="50" y="62" font-size="36" font-weight="900" text-anchor="middle" fill="#0f172a" font-family="sans-serif">P</text></svg>""",
        "desc": "동파 방지를 위해 평상시 2차측 배관이 비어있고 감지기 연동 시 물이 차오르는 준비작동식 밸브입니다.",
        "exam_tip": "📌 원 안에 Pre-action의 영문 알파벳 'P'가 들어갑니다."
    },
    {
        "id": 14,
        "name": "습식 유수검지장치 (알람밸브)",
        "category": "밸브류",
        "svg": """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="36" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><text x="50" y="62" font-size="36" font-weight="900" text-anchor="middle" fill="#0f172a" font-family="sans-serif">A</text></svg>""",
        "desc": "1, 2차측에 항시 가압수가 채워져 있어 헤드 개방 즉시 살수 및 경보를 발하는 밸브입니다.",
        "exam_tip": "📌 원 안에 Alarm의 영문 알파벳 'A'가 들어갑니다."
    },

    # 경보 & 감지기 설비
    {
        "id": 15,
        "name": "연기감지기 (광전식/이온화식)",
        "category": "경보/감지기",
        "svg": """<svg viewBox="0 0 100 100"><rect x="18" y="18" width="64" height="64" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><text x="50" y="62" font-size="38" font-weight="900" text-anchor="middle" fill="#0f172a" font-family="sans-serif">S</text></svg>""",
        "desc": "화재 초기 단계에서 발생하 연기 입자를 감지하여 수신기로 신호를 보내는 감지기입니다.",
        "exam_tip": "📌 사각형 안에 Smoke를 뜻하는 영문 'S'가 표기됩니다."
    },
    {
        "id": 16,
        "name": "열감지기 (차동식/정온식)",
        "category": "경보/감지기",
        "svg": """<svg viewBox="0 0 100 100"><rect x="18" y="18" width="64" height="64" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><text x="50" y="62" font-size="38" font-weight="900" text-anchor="middle" fill="#0f172a" font-family="sans-serif">H</text></svg>""",
        "desc": "화재 열로 인한 온도의 급격한 상승 또는 일정 온도 도달을 감지하는 감지기 기호입니다.",
        "exam_tip": "📌 사각형 안에 Heat를 뜻하는 영문 'H'가 표기됩니다."
    },
    {
        "id": 17,
        "name": "비상경보벨 (경종)",
        "category": "경보/감지기",
        "svg": """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="36" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><text x="50" y="62" font-size="36" font-weight="900" text-anchor="middle" fill="#0f172a" font-family="sans-serif">B</text></svg>""",
        "desc": "화재 신호를 수신기로부터 받아 건물 내부 음향으로 화재를 경보하는 모터 경종 기호입니다.",
        "exam_tip": "📌 원 안에 Bell의 영문 'B'가 기재됩니다."
    },
    {
        "id": 18,
        "name": "피난구유도등",
        "category": "경보/감지기",
        "svg": """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="36" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><path d="M 50 14 A 36 36 0 0 1 86 50 L 50 50 Z" fill="#0f172a"/><path d="M 14 50 A 36 36 0 0 1 50 86 L 50 50 Z" fill="#0f172a"/></svg>""",
        "desc": "비상 탈출구 상단에 설치되어 어두운 화재 현장에서 비상구 위치를 알려주는 유도등 기호입니다.",
        "exam_tip": "📌 원이 4분할되어 대각선 2분할 사분면이 검은색으로 반전됩니다."
    },

    # 기타 & 제연 설비
    {
        "id": 19,
        "name": "비상콘센트",
        "category": "제연/기타",
        "svg": """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="36" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><circle cx="36" cy="50" r="6" fill="#0f172a"/><circle cx="64" cy="50" r="6" fill="#0f172a"/><line x1="14" y1="50" x2="86" y2="50" stroke="#0f172a" stroke-width="4"/></svg>""",
        "desc": "소방대원이 화재 진압 활동 시 조명기구나 파괴용 전동공구 전원을 연결하는 소화활동용 콘센트입니다.",
        "exam_tip": "📌 원 안에 플러그 2구 구멍과 가로 직선 라인이 표현됩니다."
    },
    {
        "id": 20,
        "name": "연기댐퍼 (Smoke Damper)",
        "category": "제연/기타",
        "svg": """<svg viewBox="0 0 100 100"><rect x="15" y="25" width="70" height="50" stroke="#0f172a" stroke-width="5" fill="#ffffff"/><line x1="15" y1="75" x2="85" y2="25" stroke="#0f172a" stroke-width="5"/><text x="50" y="58" font-size="22" font-weight="900" text-anchor="middle" fill="#0f172a" font-family="sans-serif">SD</text></svg>""",
        "desc": "제연 덕트 배관에 설치되어 화재 감지 시 유독 가스와 연기의 확산을 차단하는 제연 댐퍼입니다.",
        "exam_tip": "📌 직사각형 대각선과 함께 영문 'SD'가 표기됩니다."
    }
]

# 세션 상태 초기화
if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0
if "is_flipped" not in st.session_state:
    st.session_state.is_flipped = False
if "known_set" not in st.session_state:
    st.session_state.known_set = set()
if "category_filter" not in st.session_state:
    st.session_state.category_filter = "전체보기"

# 앱 타이틀
st.title("🔥 소방 도시기호 고화질 암기장")
st.caption("✨ 벡터(SVG) 방식으로 스마트폰 & 4K PC 어디서나 100% 선명하게 학습하세요!")

# 탭 구성
tab_card, tab_quiz, tab_gallery = st.tabs(["🎴 플래시카드", "📝 실전 퀴즈", "📚 기호 전체도감"])

# --- TAB 1: 플래시카드 학습 모드 ---
with tab_card:
    categories = ["전체보기", "소화기류", "소화전/배관", "헤드류", "밸브류", "경보/감지기", "제연/기타"]
    selected_cat = st.selectbox("📂 카테고리 필터:", categories, index=categories.index(st.session_state.category_filter))

    if selected_cat != st.session_state.category_filter:
        st.session_state.category_filter = selected_cat
        st.session_state.card_idx = 0
        st.session_state.is_flipped = False
        st.rerun()

    filtered_cards = VECTOR_SYMBOLS_DB if selected_cat == "전체보기" else [s for s in VECTOR_SYMBOLS_DB if s["category"] == selected_cat]

    if not filtered_cards:
        st.info("해당 카테고리에 등록된 기호가 없습니다.")
    else:
        total_c = len(filtered_cards)
        curr_idx = st.session_state.card_idx % total_c
        curr_card = filtered_cards[curr_idx]

        # 진도율 프로그레스
        known_cnt = len([s for s in filtered_cards if s["id"] in st.session_state.known_set])
        prog_val = min(1.0, known_cnt / total_c) if total_c > 0 else 0
        st.progress(prog_val)
        st.caption(f"📊 암기 진도율: {total_c}개 중 {known_cnt}개 달성 ({int(prog_val*100)}%)")

        # 플래시카드 앞/뒷면
        if not st.session_state.is_flipped:
            st.markdown(f'''
            <div class="flashcard-box">
                <div class="card-badge">{curr_card['category']}</div>
                <div class="card-num">{curr_idx + 1} / {total_c}</div>
                <div class="svg-container">{curr_card['svg']}</div>
                <div class="touch-hint">👆 아래 [🔄 카드 뒤집기]를 눌러 명칭과 설명을 확인하세요</div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="flashcard-box" style="border-color: #3b82f6; background: #ffffff;">
                <div class="card-badge" style="background-color: #10b981;">정답 명칭</div>
                <div class="card-num">{curr_idx + 1} / {total_c}</div>
                <div class="card-title">{curr_card['name']}</div>
                <div class="card-desc">💡 <b>설명:</b> {curr_card['desc']}</div>
                <div class="exam-tip">{curr_card['exam_tip']}</div>
            </div>
            ''', unsafe_allow_html=True)

        # 컨트롤 버튼
        col_flip, col_know = st.columns(2)
        with col_flip:
            if st.button("🔄 카드 뒤집기", type="primary"):
                st.session_state.is_flipped = not st.session_state.is_flipped
                st.rerun()
        with col_know:
            is_k = curr_card['id'] in st.session_state.known_set
            if st.button("👍 암기완료!" if is_k else "👍 암기했어요"):
                if is_k:
                    st.session_state.known_set.remove(curr_card['id'])
                else:
                    st.session_state.known_set.add(curr_card['id'])
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

# --- TAB 2: 실전 테스트 퀴즈 모드 ---
with tab_quiz:
    st.subheader("📝 소방기호 4지선다 실전 테스트")
    if "quiz_idx" not in st.session_state:
        st.session_state.quiz_idx = 0

    quiz_card = VECTOR_SYMBOLS_DB[st.session_state.quiz_idx % len(VECTOR_SYMBOLS_DB)]

    st.markdown(f'''
    <div style="text-align: center; background: white; padding: 20px; border-radius: 16px; border: 2px solid #cbd5e1; margin-bottom: 15px;">
        <div style="color: #64748b; font-weight: bold;">문제 {st.session_state.quiz_idx + 1}</div>
        <div style="width: 130px; height: 130px; margin: 15px auto;">{quiz_card['svg']}</div>
        <div style="font-size: 1.15rem; font-weight: bold; color: #0f172a;">위 소방 도시기호의 올바른 명칭은?</div>
    </div>
    ''', unsafe_allow_html=True)

    correct_name = quiz_card['name']
    other_names = [s['name'] for s in VECTOR_SYMBOLS_DB if s['name'] != correct_name]
    wrong_samples = random.sample(other_names, min(3, len(other_names)))
    options = [correct_name] + wrong_samples
    random.seed(quiz_card['id'])
    random.shuffle(options)

    user_choice = st.radio("정답 선택:", options, key=f"quiz_opt_{st.session_state.quiz_idx}")

    if st.button("🎯 정답 제출하기"):
        if user_choice == correct_name:
            st.success("🎉 정답입니다! 완벽해요!")
        else:
            st.error(f"❌ 아쉽네요! 정답은 [{correct_name}] 입니다.")
        st.info(f"💡 {quiz_card['desc']}")

    if st.button("➡️ 다음 문제"):
        st.session_state.quiz_idx += 1
        st.rerun()

# --- TAB 3: 전체 소방기호 한눈에 보기 도감 ---
with tab_gallery:
    st.subheader("📚 소방 도시기호 전체 도감")
    for item in VECTOR_SYMBOLS_DB:
        with st.expander(f"[{item['category']}] {item['name']}"):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.markdown(f'<div style="width:100px; height:100px;">{item["svg"]}</div>', unsafe_allow_html=True)
            with col_txt:
                st.write(f"**명칭:** {item['name']}")
                st.write(f"**설명:** {item['desc']}")
                st.caption(item['exam_tip'])
