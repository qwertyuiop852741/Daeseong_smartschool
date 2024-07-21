import os
import config
import sqlite3


class StudentPoint:
    def __init__(self):
        self.point_dict = {}
        # self.file_path = os.path.join(os.getcwd(), 'src', 'data', 'point', f'point{self.classroom}.json')
        # self.load_data()
        self.conn = sqlite3.connect(os.path.join(os.getcwd(), 'src', 'data', 'point', 'point.db'))
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS students
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    class INTEGER NOT NULL,
                    points INTEGER DEFAULT 0)''')
        self.conn.commit()
    # 학생 추가
    def add_student(self, name, class_num):
        c = self.conn.cursor()
        c.execute("INSERT INTO students (name, class) VALUES (?, ?)", (name, class_num))
        self.conn.commit()

    # 포인트 업데이트
    def update_points(self, student_id, points):
        c = self.conn.cursor()
        c.execute("UPDATE students SET points = points + ? WHERE id = ?", (points, student_id))
        self.conn.commit()

    # 학생 정보 조회
    def get_student_info(self, student_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        return c.fetchone()
    
    # 반별 학생 목록 조회
    def get_class_students(self, class_num):
        c = self.conn.cursor()
        c.execute("SELECT * FROM students WHERE class = ?", (class_num,))
        return c.fetchall()

    # 학생 존재 여부 확인
    def student_exists(self, student_id):
        c = self.conn.cursor()
        c.execute("SELECT EXISTS(SELECT 1 FROM students WHERE id = ?)", (student_id,))
        return bool(c.fetchone()[0])

    # 학생 ID 조회
    def get_student_id(self, name, class_num):
        c = self.conn.cursor()
        c.execute("SELECT id FROM students WHERE name = ? AND class = ?", (name, class_num))
        result = c.fetchone()
        return result[0] if result else None
                

    def get_class_students_points(self, class_num):
        c = self.conn.cursor()
        c.execute("SELECT name, points FROM students WHERE class = ?", (class_num,))
        return {row[0]: row[1] for row in c.fetchall()}



