import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="수학 및 소방·전기 도면 자동 생성기", layout="wide")

st.title("📐 수학 그래프 및 도면 자동 출제 시스템")
st.markdown("수능 기출 스타일의 그래프와 단권화용 도면을 코드로 생성하고 다운로드하세요.")

# 2. 사이드바(왼쪽 메뉴)에서 모드 선택
st.sidebar.header("🛠️ 생성 모드 선택")
mode = st.sidebar.selectbox(
    "원하는 모드를 고르세요",
    ["이차함수 그래프", "삼차함수 및 접선", "소방·전기 블록 계통도"]
)

# 3. 모드별 화면 구성 및 로직
if mode == "이차함수 그래프":
    st.subheader("📈 이차함수 ($y = ax^2 + bx + c$) 설정")
    
    # 사이드바 입력창
    a = st.sidebar.number_input("이차항 계수 (a)", value=1.0, step=0.5)
    b = st.sidebar.number_input("일차항 계수 (b)", value=0.0, step=0.5)
    c = st.sidebar.number_input("상수항 (c)", value=-4.0, step=1.0)

    # 그래프 계산
    x = np.linspace(-5, 5, 200)
    y = a * x**2 + b * x + c

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x, y, color='blue', linewidth=2.5, label=f'$y = {a}x^2 + {b}x + {c}$')
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend(fontsize=12)
    ax.set_title("Quadratic Function Graph", fontsize=14, fontweight='bold')

    # 화면에 띄우기
    st.pyplot(fig)

    # 다운로드 버튼 기능
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    buf.seek(0)
    st.download_button(
        label="📥 이 그래프 이미지 다운로드 (PNG)",
        data=buf,
        file_name="quadratic_graph.png",
        mime="image/png"
    )

elif mode == "삼차함수 및 접선":
    st.subheader("📉 삼차함수 그래프 ($y = x^3 - 3x$)")
    
    x = np.linspace(-3, 3, 400)
    y_func = x**3 - 3*x
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x, y_func, label='$y = x^3 - 3x$', color='purple', linewidth=2.5)
    ax.plot(1, -2, 'ro', markersize=8)
    ax.text(1.1, -2.2, '접점 $(1, -2)$', fontsize=11, fontweight='bold')
    
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend(fontsize=12)
    ax.set_title("Cubic Function with Point", fontsize=14, fontweight='bold')

    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    buf.seek(0)
    st.download_button(
        label="📥 삼차함수 그래프 이미지 다운로드 (PNG)",
        data=buf,
        file_name="cubic_graph.png",
        mime="image/png"
    )

elif mode == "소방·전기 블록 계통도":
    st.subheader("⚡ 소방/전기 시스템 블록 다이어그램")
    
    import matplotlib.patches as patches
    
    fig, ax = plt.subplots(figsize=(9, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')

    # 블록 박스들 생성
    box1 = patches.Rectangle((0.5, 1.5), 2, 1, edgecolor='black', facecolor='#ffcccc', linewidth=1.5)
    box2 = patches.Rectangle((4, 1.5), 2, 1, edgecolor='black', facecolor='#ccffcc', linewidth=1.5)
    box3 = patches.Rectangle((7.5, 1.5), 2, 1, edgecolor='black', facecolor='#ccccff', linewidth=1.5)

    for b_box in [box1, box2, box3]:
        ax.add_patch(b_box)

    ax.text(1.5, 2, '수신기 (R형)', fontsize=10, ha='center', va='center', weight='bold')
    ax.text(5, 2, '중계기 (Interface)', fontsize=10, ha='center', va='center', weight='bold')
    ax.text(8.5, 2, '감지기 / 경종', fontsize=10, ha='center', va='center', weight='bold')

    ax.annotate('', xy=(4, 2), xytext=(2.5, 2), arrowprops=dict(arrowstyle="->", lw=2, color='darkred'))
    ax.annotate('', xy=(7.5, 2), xytext=(6, 2), arrowprops=dict(arrowstyle="->", lw=2, color='darkblue'))

    ax.set_title("Fire Protection System Schematic", fontsize=14, fontweight='bold')

    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    buf.seek(0)
    st.download_button(
        label="📥 소방 계통도 이미지 다운로드 (PNG)",
        data=buf,
        file_name="fire_system_diagram.png",
        mime="image/png"
    )
