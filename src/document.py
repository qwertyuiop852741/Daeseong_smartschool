import easyocr
import anthropic
import json
import config
from datetime import datetime
from PIL import Image
from pytesseract import *
import os

class DocumentSummarizer:
    def __init__(self, claude_api_key=config.CLAUDE_KEY, json_filename='summaries.json'):
        """
        DocumentSummarizer 클래스 초기화
        :param claude_api_key: Claude API 키
        :param json_filename: 요약 내용을 저장할 JSON 파일 이름
        """
        self.claude_client = anthropic.Client(api_key=claude_api_key)
        self.json_filename = os.path.join(os.getcwd(), 'src', 'data', json_filename)
        
    def extract_text_from_image(self, image_path):
        """
        이미지에서 텍스트 추출
        :param image_path: 이미지 파일 경로
        :return: 추출된 전체 텍스트
        """
        # result = self.reader.readtext(image_path)
        # full_text = ' '.join([text[1] for text in result])
        # return full_text
        image = Image.open(image_path)
        text = image_to_string(image, lang='kor')
        return text

    def summarize_text(self, text):
        """
        Claude API를 사용하여 텍스트 요약
        :param text: 요약할 텍스트
        :return: 요약된 텍스트
        """
        prompt = f"다음은 학교 문서를 OCR 스캔한 결과인데, 읽기 좋게 내용을 다듬어주세요.:\n\n{text}"
        
        response = self.claude_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.5,
            system="당신은 문서 스캔 결과를 알아보기 쉽게 다듬는 전문가입니다.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content

    def process_image(self, image_path):
        """
        이미지 처리 전체 과정 수행: 텍스트 추출, 요약, JSON 저장
        :param image_path: 처리할 이미지 파일 경로
        :return: 추출된 텍스트와 요약 내용
        """
        extracted_text = self.extract_text_from_image(image_path)
        summary = self.summarize_text(extracted_text)
        self.save_summary_to_json(summary)
        return summary

    def save_summary_to_json(self, summary):
        """
        요약 내용을 JSON 파일에 저장
        :param summary: 저장할 요약 내용
        """
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "date": current_date,
            "summary": summary
        }

        # 기존 파일 읽기 (없으면 새 리스트 생성)
        try:
            with open(self.json_filename, 'r', encoding='utf-8') as file:
                file_data = json.load(file)
        except FileNotFoundError:
            file_data = []

        file_data.append(data)

        # 업데이트된 데이터 저장
        with open(self.json_filename, 'w', encoding='utf-8') as file:
            json.dump(file_data, file, ensure_ascii=False, indent=4)

        print(f"요약 내용이 {self.json_filename}에 저장되었습니다.")

    def delete_summary_from_json(self, date_to_delete):
        """
        특정 날짜의 요약 내용을 JSON 파일에서 삭제
        :param date_to_delete: 삭제할 요약의 날짜 (문자열 형식: "YYYY-MM-DD HH:MM:SS")
        """
        try:
            with open(self.json_filename, 'r', encoding='utf-8') as file:
                file_data = json.load(file)
        except FileNotFoundError:
            print(f"{self.json_filename} 파일을 찾을 수 없습니다.")
            return

        # 지정된 날짜의 항목을 제외한 새 리스트 생성
        file_data = [item for item in file_data if item['date'] != date_to_delete]

        # 업데이트된 데이터 저장
        with open(self.json_filename, 'w', encoding='utf-8') as file:
            json.dump(file_data, file, ensure_ascii=False, indent=4)

        print(f"{date_to_delete} 날짜의 요약이 삭제되었습니다.")

    #todo: add loading feature


    def show_documents(self):
        try:
            with open(self.json_filename, 'r', encoding='utf-8') as file:
                doc = json.load(file)
        except FileNotFoundError:
            doc = []