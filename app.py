import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import io

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="고급 수학 및 도면 자동 생성기", layout="wide")

st.title("📐 종합 수학 함수 및 기하 도면 자동 출제 시스템")
st.markdown("수능·모의고사 출제 및 단권화 노트를 위한 모든 함수 및 도형 시각화 프로그램")

# 2. 사이드바(왼쪽 메뉴) 설정
st.sidebar.header("🛠️ 파일명 및 종류 설정")
save_filename = st.sidebar.text_input("저장할 파일 이름", value="q01_graph.png")

st.sidebar.markdown("---")
st.sidebar.header("📊 함수 및 도형 종류 선택")
category = st.sidebar.selectbox(
    "어떤 그래프를 그리시겠습니까?",
    ["N차 다항함수", "지수 및 로그함수", "삼각함수", "분수 및 무리함수", "원 (Circle)"]
)

# [핵심 수정] PDF 내보내기 시 페이지를 침범하지 않는 아담한 시험지용 크기 (가로 3.2, 세로 2.4인치)
fig, ax = plt.subplots(figsize=(3.2, 2.4))

# 3. 카테고리별 분기 및 로직 처리
if category == "N차 다항함수":
    st.subheader("📈 N차 다항함수 그래프 (1차 ~ 4차)")
    deg = st.sidebar.selectbox("함수 차수 선택", [1, 2, 3, 4], index=1)
    
    if deg == 1:
        a = st.sidebar.number_input("기울기 (a)", value=1.0)
        b = st.sidebar.number_input("절편 (b)", value=0.0)
        x = np.linspace(-5, 5, 200)
        y = a * x + b
        label_text = f'$y = {a}x + {b}$'
    elif deg == 2:
        a = st.sidebar.number_input("이차항 (a)", value=1.0)
        b = st.sidebar.number_input("일차항 (b)", value=0.0)
        c = st.sidebar.number_input("상수항 (c)", value=-4.0)
        x = np.linspace(-5, 5, 200)
        y = a * x**2 + b * x + c
        label_text = f'$y = {a}x^2 + {b}x + {c}$'
    elif deg == 3:
        a = st.sidebar.number_input("삼차항 (a)", value=1.0)
        b = st.sidebar.number_input("일차항 (b)", value=-3.0)
        c = st.sidebar.number_input("상수항 (c)", value=0.0)
        x = np.linspace(-3, 3, 200)
        y = a * x**3 + b * x + c
        label_text = f'$y = {a}x^3 + {b}x + {c}$'
    else:
        a = st.sidebar.number_input("사차항 (a)", value=1.0)
        b = st.sidebar.number_input("이차항 (b)", value=-4.0)
        c = st.sidebar.number_input("상수항 (c)", value=3.0)
        x = np.linspace(-3, 3, 200)
        y = a * x**4 + b * x**2 + c
        label_text = f'$y = {a}x^4 + {b}x^2 + {c}$'

    ax.plot(x, y, color='blue', linewidth=1.8, label=label_text)
    ax.set_title(f"Degree {deg} Polynomial", fontsize=10, fontweight='bold')

elif category == "지수 및 로그함수":
    st.subheader("📈 지수 및 로그함수 그래프")
    func_type = st.sidebar.radio("유형 선택", ["지수함수 ($a^x$)", "로그함수 ($\log_a x$)"])
    
    if "지수" in func_type:
        base = st.sidebar.slider("밑 (a)", 1.1, 5.0, 2.0, 0.1)
        x = np.linspace(-3, 3, 200)
        y = base**x
        ax.plot(x, y, color='green', linewidth=1.8, label=f'$y = {base}^x$')
        ax.set_title("Exponential Function", fontsize=10, fontweight='bold')
    else:
        x = np.linspace(0.01, 5, 200)
        y = np.log(x)
        ax.plot(x, y, color='darkorange', linewidth=1.8, label='$y = \\ln(x)$')
        ax.set_title("Logarithmic Function", fontsize=10, fontweight='bold')

elif category == "삼각함수":
    st.subheader("📉 삼각함수 그래프 (Sin, Cos, Tan)")
    trig_func = st.sidebar.selectbox("함수 선택", ["Sine ($\sin x$)", "Cosine ($\cos x$)", "Tangent ($\tan x$)"])
    
    x = np.linspace(-2*np.pi, 2*np.pi, 400)
    if "Sine" in trig_func:
        y = np.sin(x)
        label_text = '$y = \\sin(x)$'
    elif "Cosine" in trig_func:
        y = np.cos(x)
        label_text = '$y = \\cos(x)$'
    else:
        x = np.linspace(-1.4*np.pi, 1.4*np.pi, 400)
        y = np.tan(x)
        y[np.abs(y) > 10] = np.nan
        label_text = '$y = \\tan(x)$'

    ax.plot(x, y, color='purple', linewidth=1.8, label=label_text)
    ax.set_xlim(-2*np.pi, 2*np.pi)
    ax.set_ylim(-3, 3)
    ax.set_title("Trigonometric Function", fontsize=10, fontweight='bold')

elif category == "분수 및 무리함수":
    st.subheader("📉 분수(유리) 및 무리함수 그래프")
    func_type = st.sidebar.selectbox("유형 선택", ["분수함수 ($a/x$)", "무리함수 ($\sqrt{x}$ )"])
    
    if "분수" in func_type:
        a = st.sidebar.number_input
