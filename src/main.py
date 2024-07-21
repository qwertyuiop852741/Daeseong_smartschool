from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
import sys

from sympy import false

from document import DocumentSummarizer
from point import StudentPoint
import config
from point_dialog import PointDialog

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

        self.std_point = StudentPoint()

        # self.student_points_arr = [] # 학생 포인트 관리 클래스 초기화
        # for i in range(0, config.CLASSES):
        #     self.student_points_arr.append(StudentPoint(i + 1))

    def initUI(self):
        self.setWindowTitle('Daeseong High School')
        self.setGeometry(100, 100, 600, 400)

        # 메인 레이아웃
        main_layout = QHBoxLayout()

        # 왼쪽 레이아웃 (리스트)
        self.list_widget = QListWidget()
        self.list_widget.addItems(["포인트", "공지사항", "시간표"])
        self.list_widget.currentRowChanged.connect(self.display_content)
        main_layout.addWidget(self.list_widget, 1)

        # 오른쪽 레이아웃 (변경되는 내용)
        self.content_stack = QStackedWidget()

        # 포인트 페이지-------------------------------
        point_page = QWidget()
        point_layout = QVBoxLayout(point_page)

        modify_button = QPushButton('포인트 추가/차감')
        modify_button.clicked.connect(self.modify_points)
        point_layout.addWidget(modify_button)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setEditTriggers(QAbstractItemView.EditTriggers.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(['이름', '포인트'])
        point_layout.addWidget(self.table)
        self.content_stack.addWidget(point_page)

        self.class_combo = QComboBox()
        for i in range(1, config.CLASSES + 1):
            self.class_combo.addItem(f'{i}반')

        self.class_combo.currentIndexChanged.connect(self.generate_table)
        point_layout.addWidget(self.class_combo)

        # 공지사항 페이지 --------------------------------------
        #todo
        # --------------------------------------------------


        main_layout.addWidget(self.content_stack, 2)

        self.setLayout(main_layout)

    def generate_table(self):
            self.update_class()
            data = self.std_point.get_class_students_points(self.current_class)
            # data = self.student_points_arr[current_class].return_point()
            self.table.setRowCount(len(data))

            for row, (key, value) in enumerate(data.items()):
                self.table.setItem(row, 0, QTableWidgetItem(str(key)))
                self.table.setItem(row, 1, QTableWidgetItem(str(value)))

            self.table.show() 
            
    def display_content(self, index):
        self.content_stack.setCurrentIndex(index)

    def modify_points(self):
        self.update_class()
        # current_class = self.student_points_arr[int(self.class_combo.currentIndex())]
        dialog = PointDialog(self)
        if dialog.exec() == QDialog.Accepted:
            inputs = dialog.get_inputs()
            std_name = inputs[0]
            points_to_modify = inputs[1]
            current_id = self.std_point.get_student_id(std_name, self.current_class)

            if current_id != None:
                self.std_point.update_points(current_id, points_to_modify)
            else:
                self.std_point.add_student(std_name, self.current_class)
                current_id = self.std_point.get_student_id(std_name, self.current_class)
                self.std_point.update_points(current_id, points_to_modify)

            # if self.std_point.student_exists(current_id):
            #     self.std_point.update_points(current_id, points_to_modify)
            # elif self.std_point.student_exists(current_id) == False:
            #     self.std_point.add_student(std_name, self.current_class)
            #     self.std_point.update_points(current_id, points_to_modify)
        self.generate_table()

    def update_class(self):
        self.current_class = self.class_combo.currentIndex()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.generate_table()
    sys.exit(app.exec())

