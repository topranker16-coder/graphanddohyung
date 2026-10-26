import matplotlib.pyplot as plt
import numpy as np

# 1. x 값 범위 설정 (-5부터 5까지)
x = np.linspace(-5, 5, 100)
y = x**2 - 4   # 이차함수 y = x^2 - 4

# 2. 그래프 그리기 준비
plt.figure(figsize=(5, 5))
plt.plot(x, y, color='blue', linewidth=2, label='$y = x^2 - 4$')

# 3. 선과 격자 정리
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

# 4. 'my_graph.png'라는 이름으로 컴퓨터에 그림 파일로 저장하기
plt.savefig('my_graph.png', dpi=300, bbox_inches='tight')
plt.close()

print("그림 파일 저장 완료!")
