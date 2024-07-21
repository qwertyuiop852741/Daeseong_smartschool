import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

class PointDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("포인트 수정")

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.point_input = QLineEdit(self)

        form_layout.addRow("이름:", self.name_input)
        form_layout.addRow("추가/차감할 포인트:", self.point_input)


        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_inputs(self):
        return (self.name_input.text(), int(self.point_input.text()))