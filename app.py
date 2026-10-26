import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 웹페이지 제목 만들기
st.title("수학 그래프 자동 생성기")
st.write("파이썬으로 그린 그래프를 웹에서 확인하는 테스트 페이지입니다.")

# 1. x 값 범위 설정
x = np.linspace(-5, 5, 100)
y = x**2 - 4   # 이차함수 y = x^2 - 4

# 2. 그래프 그리기 준비
fig, ax = plt.subplots(figsize=(5, 5))
ax.plot(x, y, color='blue', linewidth=2, label='$y = x^2 - 4$')

ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend()

# 3. ★ 핵심: 스트림릿 웹 화면에 그래프 띄우기!
st.pyplot(fig)
