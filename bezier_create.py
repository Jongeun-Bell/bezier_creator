import cv2
import numpy as np
import random
import json
import os


# ==========================================================
# 1) Bézier 곡선 생성 함수
# ==========================================================
def bezier_curve(P0, P1, P2, P3, num_points=250):
    t = np.linspace(0, 1, num_points).reshape(num_points, 1)

    P0 = P0.reshape(1, 2)
    P1 = P1.reshape(1, 2)
    P2 = P2.reshape(1, 2)
    P3 = P3.reshape(1, 2)

    curve = (1 - t)**3 * P0 \
            + 3 * (1 - t)**2 * t * P1 \
            + 3 * (1 - t) * t**2 * P2 \
            + t**3 * P3

    return curve.astype(int)



# ==========================================================
# 2) 절취선 생성 함수
# ==========================================================
def generate_vertical_cutline(
    img_path,
    output_folder="output",      # 폴더명 추가
    x_center_ratio=(0.45, 0.55),
    x_jitter=2,
    ticket_y_ratio=(0.49, 0.89),
    dash_length=13,
    thickness=7,
    segment_ratio=1.3
):

    # ------------------------------------------------------
    # A) 출력 폴더 생성 (없으면 자동 생성)
    # ------------------------------------------------------
    os.makedirs(output_folder, exist_ok=True)

    # 실행할 때마다 파일 넘버링
    # ticket_cutline_1.png, ticket_cutline_2.png ...
    file_index = 1
    while True:
        output_img = os.path.join(output_folder, f"ticket_cutline_{file_index}.png")
        if not os.path.exists(output_img):
            break
        file_index += 1

    # JSON 파일 경로
    output_json = output_img.replace(".png", ".json")

    # ------------------------------------------------------
    # 1) 이미지 로드
    # ------------------------------------------------------
    img = cv2.imread(img_path)
    if img is None:
        print("[ERROR] 입력 이미지가 존재하지 않습니다:", img_path)
        return None

    h, w = img.shape[:2]

    # ------------------------------------------------------
    # 2) 티켓 y 범위 계산
    # ------------------------------------------------------
    ticket_y_min = int(h * ticket_y_ratio[0])
    ticket_y_max = int(h * ticket_y_ratio[1])

    # ------------------------------------------------------
    # 3) x 위치 설정
    # ------------------------------------------------------
    x_min = int(w * x_center_ratio[0])
    x_max = int(w * x_center_ratio[1])
    base_x = random.randint(x_min, x_max)

    # ------------------------------------------------------
    # 4) Bézier Control Points
    # ------------------------------------------------------
    P0 = np.array([base_x, ticket_y_min])
    P3 = np.array([base_x, ticket_y_max])

    P1 = np.array([base_x + random.randint(-x_jitter, x_jitter),
                   ticket_y_min + int((ticket_y_max - ticket_y_min) * 0.3)])

    P2 = np.array([base_x + random.randint(-x_jitter, x_jitter),
                   ticket_y_min + int((ticket_y_max - ticket_y_min) * 0.7)])

    # ------------------------------------------------------
    # 5) Bézier 곡선 좌표 생성
    # ------------------------------------------------------
    curve_points = bezier_curve(P0, P1, P2, P3)

    # ------------------------------------------------------
    # 6) 점선 그리기
    # ------------------------------------------------------
    segment_length = int(dash_length * segment_ratio)
    color = (255, 255, 255)  # 흰색

    for i in range(0, len(curve_points), dash_length):

        if (i // dash_length) % 2 == 0:
            start = tuple(curve_points[i])
            end_idx = min(i + segment_length, len(curve_points) - 1)
            end = tuple(curve_points[end_idx])

            x1, y1 = start
            x2, y2 = end
            half = thickness // 2

            cv2.rectangle(
                img,
                (x1 - half, y1),
                (x1 + half, y2),
                color,
                -1
            )

    # ------------------------------------------------------
    # 7) 이미지 저장 (자동 넘버링)
    # ------------------------------------------------------
    cv2.imwrite(output_img, img)
    print("이미지 저장 완료:", output_img)

    # ------------------------------------------------------
    # 8) JSON 데이터 저장
    # ------------------------------------------------------
    result = {
        "curve_points": curve_points.tolist(),
        "base_x": base_x,
        "ticket_y_range": [ticket_y_min, ticket_y_max]
    }

    with open(output_json, "w") as f:
        json.dump(result, f, indent=4)

    print("JSON 저장 완료:", output_json)

    return result



# ==========================================================
# 3) 실행부
# ==========================================================
if __name__ == "__main__":
    generate_vertical_cutline(
        img_path="ticket.png",
        output_folder="output"
    )
