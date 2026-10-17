import streamlit as st
import json
import random

# 스마트폰 화면 최적화 (Mobile Responsive Viewport & Custom CSS)
st.set_page_config(
    page_title="🔥 소방기호 암기 스마트 플래시카드",
    page_icon="🎴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 모바일 전용 UI CSS 주입
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    /* 스마트폰 스크린 메인 컨테이너 고정 및 가독성 최적화 */
    .main .block-container {
        max-width: 450px !important;
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    
    /* 플래시카드 터치 패널 스타일 */
    .flashcard-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #e2e8f0;
        border-radius: 20px;
        padding: 25px 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        text-align: center;
        min-height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 15px;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .flashcard-box:active {
        transform: scale(0.98);
    }
    
    .card-badge {
        position: absolute;
        top: 12px;
        left: 15px;
        background-color: #3b82f6;
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

    .card-title {
        color: #0f172a;
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .card-desc {
        color: #334155;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-top: 8px;
        text-align: left;
        background-color: #f1f5f9;
        padding: 12px 15px;
        border-radius: 12px;
        width: 100%;
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
    }

    .touch-hint {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 12px;
    }

    /* 버튼 모바일 커스텀 */
    div.stButton > button {
        width: 100% !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 12px 0px !important;
        font-size: 0.95rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 종합 소방기호 데이터베이스 (Symbol SVG Renders & Full Specs)
SYMBOLS_DATA = [
    # 소화기류
    {
        "id": 1,
        "name": "ABC 소화기",
        "category": "소화기류",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><circle cx="50" cy="50" r="38" stroke="#1e293b" stroke-width="4" fill="#ffffff"/><text x="50" y="60" font-size="32" font-weight="900" text-anchor="middle" fill="#1e293b">소</text></svg>""",
        "desc": "가장 흔히 사용되는 A(일반화재), B(유류화재), C(전기화재) 겸용 수동식 소화기입니다.",
        "exam_tip": "📌 원 안에 '소'자가 기재된 대표 도시기호입니다."
    },
    {
        "id": 2,
        "name": "자동확산 소화기",
        "category": "소화기류",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><circle cx="50" cy="50" r="38" stroke="#1e293b" stroke-width="4" fill="#ffffff"/><text x="50" y="60" font-size="32" font-weight="900" text-anchor="middle" fill="#1e293b">자</text></svg>""",
        "desc": "주방이나 보일러실 천장에 설치되어 화재 발생 시 열을 감지하여 자동으로 약제를 분사하는 소화기입니다.",
        "exam_tip": "📌 원 안에 '자'자가 적혀 있습니다."
    },
    {
        "id": 3,
        "name": "자동식 소화기",
        "category": "소화기류",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><polygon points="50,12 88,50 50,88 12,50" fill="#1e293b"/><text x="50" y="60" font-size="28" font-weight="900" text-anchor="middle" fill="#ffffff">소</text></svg>""",
        "desc": "아파트 주방 등에 의무 설치되는 상업용/주거용 주방자동소화장치 관련 기호입니다.",
        "exam_tip": "📌 검은색 마름모 바탕에 흰색 '소' 글자가 특징입니다."
    },
    {
        "id": 4,
        "name": "이산화탄소 소화기 (CO2)",
        "category": "소화기류",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><circle cx="50" cy="50" r="38" stroke="#1e293b" stroke-width="4" fill="#ffffff"/><text x="50" y="60" font-size="34" font-weight="900" text-anchor="middle" fill="#1e293b">C</text></svg>""",
        "desc": "이산화탄소 가스를 방출하여 질식 및 냉각 효과로 화재를 진화하며, 잔여물이 남지 않는 소화기입니다.",
        "exam_tip": "📌 원 안에 영문 'C'가 표시됩니다."
    },
    {
        "id": 5,
        "name": "할로겐화합물 소화기",
        "category": "소화기류",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><polygon points="50,12 88,82 12,82" stroke="#1e293b" stroke-width="4" fill="#ffffff"/><text x="50" y="68" font-size="28" font-weight="900" text-anchor="middle" fill="#1e293b">소</text></svg>""",
        "desc": "할론 가스를 주성분으로 하는 깨끗한 소화약제 소화기입니다.",
        "exam_tip": "📌 정삼각형 안에 '소' 글자가 기재되어 있습니다."
    },

    # 소화전 & 배관
    {
        "id": 6,
        "name": "옥내소화전함",
        "category": "소화전/배관",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><rect x="18" y="18" width="64" height="64" stroke="#1e293b" stroke-width="4" fill="#ffffff"/><polygon points="18,18 82,18 18,82" fill="#1e293b"/></svg>""",
        "desc": "건물 내부에 설치되어 관계자나 거주자가 초기 진화에 사용하는 소화전 설비입니다.",
        "exam_tip": "📌 사각 상자의 대각선 좌상단 절반이 검은색으로 칠해져 있습니다."
    },
    {
        "id": 7,
        "name": "옥외소화전",
        "category": "소화전/배관",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><line x1="10" y1="50" x2="90" y2="50" stroke="#1e293b" stroke-width="4"/><path d="M 38 50 A 12 24 0 0 1 62 50" fill="none" stroke="#1e293b" stroke-width="4"/><text x="50" y="42" font-size="22" font-weight="900" text-anchor="middle" fill="#1e293b">H</text></svg>""",
        "desc": "건물 외부에 설치되어 소방대원 또는 의용소방대가 외부 진화에 사용하는 소화전 기호입니다.",
        "exam_tip": "📌 배관 라인 중앙에 'H' 문자가 기재되어 있습니다."
    },

    # 헤드류
    {
        "id": 8,
        "name": "스프링클러헤드 (폐쇄형 상향식)",
        "category": "헤드류",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><circle cx="50" cy="50" r="32" stroke="#1e293b" stroke-width="4" fill="#ffffff"/><circle cx="50" cy="50" r="12" fill="#1e293b"/><line x1="50" y1="8" x2="50" y2="18" stroke="#1e293b" stroke-width="4"/></svg>""",
        "desc": "감열부가 폐쇄되어 있고, 헤드가 위쪽을 향하게 설치되어 배관 상부에 배치되는 스프링클러 헤드입니다.",
        "exam_tip": "📌 원 안에 검은 점(원)이 채워져 있습니다."
    },
    {
        "id": 9,
        "name": "스프링클러헤드 (폐쇄형 하향식)",
        "category": "헤드류",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><circle cx="50" cy="50" r="32" stroke="#1e293b" stroke-width="4" fill="#ffffff"/><line x1="50" y1="18" x2="50" y2="82" stroke="#1e293b" stroke-width="3"/><line x1="18" y1="50" x2="82" y2="50" stroke="#1e293b" stroke-width="3"/><path d="M 33 65 A 17 17 0 0 0 67 65 Z" fill="#1e293b"/></svg>""",
        "desc": "헤드가 아래쪽을 향하게 설치되어 천장 아래로 살수하는 가장 일반적인 스프링클러 헤드입니다.",
        "exam_tip": "📌 십자선 아래쪽에 반원이 반전 칠해져 있습니다."
    },

    # 밸브류
    {
        "id": 10,
        "name": "체크밸브",
        "category": "밸브류",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><line x1="10" y1="50" x2="90" y2="50" stroke="#1e293b" stroke-width="4"/><polygon points="32,28 32,72 68,50" fill="#ffffff" stroke="#1e293b" stroke-width="4"/><line x1="68" y1="28" x2="68" y2="72" stroke="#1e293b" stroke-width="4"/></svg>""",
        "desc": "유체가 한쪽 방향으로만 흐르고 역류하지 못하도록 차단하는 밸브입니다.",
        "exam_tip": "📌 화살표 형태의 삼각 기호 끝에 수직 막대가 접해 있습니다."
    },
    {
        "id": 11,
        "name": "프리액션밸브 (준비작동식)",
        "category": "밸브류",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><circle cx="50" cy="50" r="34" stroke="#1e293b" stroke-width="4" fill="#ffffff"/><text x="50" y="61" font-size="32" font-weight="900" text-anchor="middle" fill="#1e293b">P</text></svg>""",
        "desc": "동파 우려가 있는 장소에 설치되며, 감지기 작동 시 클래퍼가 열려 2차측에 물이 공급되는 밸브입니다.",
        "exam_tip": "📌 원 안에 영문 'P'가 표시됩니다."
    },

    # 경보설비기기류
    {
        "id": 12,
        "name": "연기감지기",
        "category": "경보설비기기류",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><rect x="22" y="22" width="56" height="56" stroke="#1e293b" stroke-width="4" fill="#ffffff"/><text x="50" y="61" font-size="34" font-weight="900" text-anchor="middle" fill="#1e293b">S</text></svg>""",
        "desc": "화재 발생 초기 연기 입자를 감지하여 경보를 발하는 감지기입니다 (광전식/이온화식).",
        "exam_tip": "📌 사각형 안에 Smoke를 의미하는 'S' 문자가 들어있습니다."
    },
    {
        "id": 13,
        "name": "비상경보벨 (화재경보벨)",
        "category": "경보설비기기류",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><circle cx="50" cy="50" r="34" stroke="#1e293b" stroke-width="4" fill="#ffffff"/><text x="50" y="61" font-size="32" font-weight="900" text-anchor="middle" fill="#1e293b">B</text></svg>""",
        "desc": "화재 신호를 받아 음향으로 화재 발생을 알리는 음향장치(경종)입니다.",
        "exam_tip": "📌 원 안에 Bell의 'B' 문자가 표기됩니다."
    },
    {
        "id": 14,
        "name": "피난구유도등",
        "category": "경보설비기기류",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><circle cx="50" cy="50" r="34" stroke="#1e293b" stroke-width="4" fill="#ffffff"/><path d="M 50 16 A 34 34 0 0 1 84 50 L 50 50 Z" fill="#1e293b"/><path d="M 16 50 A 34 34 0 0 1 50 84 L 50 50 Z" fill="#1e293b"/></svg>""",
        "desc": "피난구(출입구) 상부에 설치하여 비상시 탈출구를 안내하는 유도등 기호입니다.",
        "exam_tip": "📌 원이 4분할되어 대각선 2분할이 검은색으로 칠해져 있습니다."
    },

    # 기타 & 제연
    {
        "id": 15,
        "name": "비상콘센트",
        "category": "기타/제연설비",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><circle cx="50" cy="50" r="34" stroke="#1e293b" stroke-width="4" fill="#ffffff"/><circle cx="38" cy="50" r="6" fill="#1e293b"/><circle cx="62" cy="50" r="6" fill="#1e293b"/><line x1="16" y1="50" x2="84" y2="50" stroke="#1e293b" stroke-width="3"/></svg>""",
        "desc": "화재 시 소방대원이 조명이나 동력 기구용 전원을 확보하기 위해 사용하는 소화활동유도용 콘센트입니다.",
        "exam_tip": "📌 원 안에 콘센트 구멍 2개와 가로 배선 라인이 표현되어 있습니다."
    },
    {
        "id": 16,
        "name": "접지 기호",
        "category": "기타/제연설비",
        "svg": """<svg width="130" height="130" viewBox="0 0 100 100"><line x1="50" y1="18" x2="50" y2="52" stroke="#1e293b" stroke-width="4"/><line x1="22" y1="52" x2="78" y2="52" stroke="#1e293b" stroke-width="4"/><line x1="32" y1="65" x2="68" y2="65" stroke="#1e293b" stroke-width="3"/><line x1="42" y1="78" x2="58" y2="78" stroke="#1e293b" stroke-width="2.5"/></svg>""",
        "desc": "전기 누전 방지 및 소방장비 보호를 위한 접지(Earth / Ground) 기호입니다.",
        "exam_tip": "📌 수직선 아래 점차 좁아지는 3개의 수평선 형태입니다."
    }
]

# 세션 상태 초기화
if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0
if "is_flipped" not in st.session_state:
    st.session_state.is_flipped = False
if "known_cards" not in st.session_state:
    st.session_state.known_cards = set()
if "category_filter" not in st.session_state:
    st.session_state.category_filter = "전체보기"

# 앱 타이틀
st.title("🔥 소방기호 스마트 암기장")
st.caption("📱 스마트폰 터치 한 번으로 앞면(그림) & 뒷면(명칭/설명)을 뒤집어가며 암기하세요!")

# 탭 메뉴
tab1, tab2, tab3 = st.tabs(["🎴 플래시카드", "📝 퀴즈 풀기", "📚 기호 전체보기"])

# --- TAB 1: 플래시카드 학습 모드 ---
with tab1:
    categories = ["전체보기", "소화기류", "소화전/배관", "헤드류", "밸브류", "경보설비기기류", "기타/제연설비"]
    selected_cat = st.selectbox("📂 카테고리 선택:", categories, index=categories.index(st.session_state.category_filter))
    
    if selected_cat != st.session_state.category_filter:
        st.session_state.category_filter = selected_cat
        st.session_state.card_idx = 0
        st.session_state.is_flipped = False
        st.rerun()

    filtered_symbols = SYMBOLS_DATA if selected_cat == "전체보기" else [s for s in SYMBOLS_DATA if s["category"] == selected_cat]

    if not filtered_symbols:
        st.info("해당 카테고리에 기호가 없습니다.")
    else:
        if st.session_state.card_idx >= len(filtered_symbols):
            st.session_state.card_idx = 0

        curr_card = filtered_symbols[st.session_state.card_idx]
        total_count = len(filtered_symbols)
        curr_num = st.session_state.card_idx + 1

        known_count = len([s for s in filtered_symbols if s["id"] in st.session_state.known_cards])
        progress_val = known_count / total_count if total_count > 0 else 0
        st.progress(progress_val)
        st.caption(f"📊 암기 현황: {total_count}개 중 {known_count}개 암기 완료 ({int(progress_val*100)}%)")

        if not st.session_state.is_flipped:
            card_html = f"""
            <div class="flashcard-box">
                <div class="card-badge">{curr_card['category']}</div>
                <div class="card-num">{curr_num} / {total_count}</div>
                <div style="margin: 20px 0;">{curr_card['svg']}</div>
                <div class="touch-hint">👆 아래 [🔄 카드 뒤집기]를 눌러 명칭을 확인하세요</div>
            </div>
            """
        else:
            card_html = f"""
            <div class="flashcard-box" style="border-color: #3b82f6; background: #ffffff;">
                <div class="card-badge" style="background-color: #10b981;">정답 명칭</div>
                <div class="card-num">{curr_num} / {total_count}</div>
                <div class="card-title">{curr_card['name']}</div>
                <div class="card-desc">💡 <b>설명:</b> {curr_card['desc']}</div>
                <div class="exam-tip">{curr_card['exam_tip']}</div>
            </div>
            """
            
        st.markdown(card_html, unsafe_allow_html=True)

        col_flip, col_know = st.columns([1])
        with col_flip:
            if st.button("🔄 카드 뒤집기", type="primary"):
                st.session_state.is_flipped = not st.session_state.is_flipped
                st.rerun()
                
        with col_know:
            is_known = curr_card['id'] in st.session_state.known_cards
            btn_label = "👍 암기완료!" if is_known else "👍 암기했어요"
            if st.button(btn_label):
                if is_known:
                    st.session_state.known_cards.remove(curr_card['id'])
                else:
                    st.session_state.known_cards.add(curr_card['id'])
                st.rerun()

        st.write("")
        col_prev, col_rand, col_next = st.columns([1])
        with col_prev:
            if st.button("👈 이전"):
                st.session_state.card_idx = (st.session_state.card_idx - 1) % total_count
                st.session_state.is_flipped = False
                st.rerun()
        with col_rand:
            if st.button("🎲 섞기"):
                st.session_state.card_idx = random.randint(0, total_count - 1)
                st.session_state.is_flipped = False
                st.rerun()
        with col_next:
            if st.button("👉 다음"):
                st.session_state.card_idx = (st.session_state.card_idx + 1) % total_count
                st.session_state.is_flipped = False
                st.rerun()

# --- TAB 2: 스마트폰 O/X 및 4지선다 퀴즈 ---
with tab2:
    st.subheader("📝 소방기호 4지선다 모의퀴즈")
    st.caption("스마트폰으로 실력을 테스트해보세요!")

    if "quiz_idx" not in st.session_state:
        st.session_state.quiz_idx = 0

    quiz_card = SYMBOLS_DATA[st.session_state.quiz_idx % len(SYMBOLS_DATA)]
    
    st.markdown(f"""
    <div style="text-align: center; background: white; padding: 20px; border-radius: 16px; border: 2px solid #e2e8f0; margin-bottom: 15px;">
        <div style="color: #64748b; font-weight: bold;">문제 {st.session_state.quiz_idx + 1}</div>
        <div style="margin: 15px 0;">{quiz_card['svg']}</div>
        <div style="font-size: 1.1rem; font-weight: bold; color: #1e293b;">위 소방 도시기호의 올바른 명칭은?</div>
    </div>
    """, unsafe_allow_html=True)

    correct_name = quiz_card['name']
    other_names = [s['name'] for s in SYMBOLS_DATA if s['name'] != correct_name]
    wrong_samples = random.sample(other_names, min(3, len(other_names)))
    options = [correct_name] + wrong_samples
    random.seed(quiz_card['id'])
    random.shuffle(options)

    user_choice = st.radio("정답을 선택하세요:", options, key=f"quiz_opt_{st.session_state.quiz_idx}")

    if st.button("🎯 정답 확인하기"):
        if user_choice == correct_name:
            st.success("🎉 정답입니다! 완벽해요!")
        else:
            st.error(f"❌ 아쉽네요! 정답은 [{correct_name}] 입니다.")
        st.info(f"💡 {quiz_card['desc']}")
        
    if st.button("➡️ 다음 문제 풀기"):
        st.session_state.quiz_idx += 1
        st.rerun()

# --- TAB 3: 전체 소방기호 한눈에 보기 (도감 모드) ---
with tab3:
    st.subheader("📚 소방 도시기호 한눈에 도감")
    for item in SYMBOLS_DATA:
        with st.expander(f"[{item['category']}] {item['name']}"):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.markdown(item['svg'], unsafe_allow_html=True)
            with col_txt:
                st.write(f"**명칭:** {item['name']}")
                st.write(f"**설명:** {item['desc']}")
                st.caption(item['exam_tip'])