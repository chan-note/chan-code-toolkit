import json
import os
import cv2
import random

def generate_colors(num_classes):
    """밝고 연한 색상으로 RGB 값을 생성합니다."""
    colors = []
    random.seed(100)  # 재현성을 위한 시드 설정
    for _ in range(num_classes):
        # RGB 값이 128 이상으로 설정되도록 하여 밝고 연한 색상을 생성
        color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
        colors.append(color)
    return colors

def visualize_custom_format(json_path, image_folder, output_folder):
    # 출력 폴더 생성
    os.makedirs(output_folder, exist_ok=True)
    
    # JSON 파일 로드
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    unique_labels = {annotation["lbl_id"] for item in data for annotation in item["annotations"]}
    label_colors = {label_id: color for label_id, color in zip(unique_labels, generate_colors(len(unique_labels)))}
    
    for item in data:
        # 이미지 정보
        image_info = item["images"]
        image_id = image_info["img_id"] 
        image_name = f"{image_id}.jpg"  # image 파일 이름
        image_path = os.path.join(image_folder, image_name) # image 파일 경로
        
        # 이미지 로드
        image = cv2.imread(image_path)
        if image is None:
            print(f"이미지를 불러올 수 없습니다: {image_name}")
            continue
        
        # 각 주석(annotation)에 대해 바운딩 박스를 그림
        for annotation in item["annotations"]:
            # 주석 정보
            label_id = annotation['lbl_id'] # 클래스 번호
            label_name = annotation["lbl_nm"]    # 클래스 이름
            bbox = eval(annotation["annotations_info"])  # bbox 문자열을 리스트로 변환
            color = label_colors[label_id] 
            
            # 바운딩 박스 좌표 변환 (x, y, width, height) -> (x1, y1), (x2, y2)
            x, y, w, h = map(int, bbox)
            x1, y1, x2, y2 = x, y, x + w, y + h
            
            # 바운딩 박스 그리기
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

            # 텍스트 삽입
            text = f"{label_id}: {label_name}"
            font_scale = 1.0  # 글자 크기 증가
            thickness = 2     # 글자 굵기 증가 (볼드 효과)
            # 텍스트 크기 계산
            (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
            text_x, text_y = x1, y1 - 10  # 텍스트 위치

            # 텍스트 배경을 텍스트 너비와 높이만큼만 설정
            cv2.rectangle(image, (text_x, text_y - text_height - baseline), (text_x + text_width, text_y + baseline), color, -1)

            # 텍스트 삽입 (흰색 글씨)
            cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
        
        # 시각화 결과 저장
        output_path = os.path.join(output_folder, image_name)
        cv2.imwrite(output_path, image)
        print(f"저장 완료: {output_path}")

    print("모든 이미지 시각화 완료.")

# 파라미터 설정
json_path = '/Users/imch/Downloads/2D 객체 검지/train.json'  # JSON 파일 경로
image_folder = '/Users/imch/Downloads/2D 객체 검지/train' # 이미지 폴더 경로
output_folder = './test'  # 시각화 결과를 저장할 폴더 경로

# 시각화 실행
visualize_custom_format(json_path, image_folder, output_folder)