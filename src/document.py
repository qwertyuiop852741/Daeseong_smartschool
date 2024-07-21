import sqlite3
import anthropic
import json
import config
from datetime import datetime
from PIL import Image
from pytesseract import *
import os

class DocumentSummarizer:
    def __init__(self, claude_api_key=config.CLAUDE_KEY, db_name='summaries.db'):
        """
        DocumentSummarizer 클래스 초기화
        :param claude_api_key: Claude API 키
        :param json_filename: 요약 내용을 저장할 JSON 파일 이름
        """
        self.claude_client = anthropic.Client(api_key=claude_api_key)
        self.db_name = os.path.join(os.getcwd(), 'src', 'data', db_name)
        self.init_db()
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
        extracted_text = self.extract_text_from_image(image_path)
        summary = self.summarize_text(extracted_text)
        self.save_summary_to_db(summary)
        return summary

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS summaries
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        summary TEXT NOT NULL)
         ''')
        conn.commit()
        conn.close()

    def save_summary_to_db(self, summary):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO summaries (date, summary) VALUES (?, ?)',
                   (current_date, summary))
        conn.commit()
        conn.close()
        print(f"요약 내용이 데이터베이스에 저장되었습니다.")

    def delete_summary_from_db(self, date_to_delete):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM summaries WHERE date = ?', (date_to_delete,))
        if cursor.rowcount > 0:
            print(f"{date_to_delete} 날짜의 요약이 삭제되었습니다.")
        else:
            print(f"{date_to_delete} 날짜의 요약을 찾을 수 없습니다.")
        conn.commit()
        conn.close()

    def get_all_summaries(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT date, summary FROM summaries ORDER BY date DESC')
        summaries = cursor.fetchall()
        conn.close()
        return summaries
