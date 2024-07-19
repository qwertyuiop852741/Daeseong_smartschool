from document import DocumentSummarizer
from point import StudentPoint
import config
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
def main():
    point_array: StudentPoint = []
    for i in range(0, 10):
        point_array.append(StudentPoint(i + 1))

    chosen_menu = menu()

    if chosen_menu == 1:
        point_array[point_choose_class()].dialog()
    
    elif chosen_menu == 2:   
        while True:
            sorting = input('정렬 방식 입력 (name 또는 point)')
            if sorting == 'name' or 'point':
                break
            else:
                print('name 또는 point 중 하나를 입력하세요.')
        point_array[point_choose_class()].print_point()

    elif chosen_menu == 3:
        document_path = input('문서 이미지 경로 입력:')
        doc_sum = DocumentSummarizer()
        doc_sum.process_image(document_path)



def menu():
    print('1. 포인트 추가/차감')
    print('2. 포인트 순위 보기')
    print('3. 문서 저장')
    print('4. 저장된 문서 보기')
    choice = int(input('기능 선택: '))
    return choice

def point_choose_class():
    return int(input('반 선택:')) - 1

if __name__ == '__main__':
    main()
