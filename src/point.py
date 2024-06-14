import json
import os
import tabulate

class StudentPoint:
    def __init__(self):
        with open("point.json") as pj:
            self.point_dict = json.load(pj)

    def write_modified_data(self): #수정된 데이터 저장
        with open('point.json') as pj:
            pj.write(json.dump(self.point_dict,indent = 2, ensure_ascii = False))

    def __add_point(std_name, pnt_to_add, self): # 포인트 추가
        self.point_dict[std_name] += pnt_to_add
        self.write_modified_data()

    def __remove_point(std_name, pnt_to_add, self): #포인트 차감
        self.point_dict[std_name] += pnt_to_add
        self.write_modified_data()

    def dialog(self): #질문한 후 지정 명령 실행
        student_name = input('이름: ')
        point_to_pm = input('추가 또는 차감할 포인트: ')
        what_to_do = input('추가 또는 차감: ')
        if what_to_do == '추가':
            self.__add_point(student_name, point_to_pm)
        elif what_to_do == '차감':
            self.__remove_point(student_name, point_to_pm)

    def print_point(sorting, self): #표 출력
        try:
            if sorting == 'name':
                sorted_list = sorted(self.point_dict.items())
            elif sorting == 'point':
                sorted_list = sorted(self.point_dict.items(), key=lambda x: x[1])
        finally:
            print('print_point 함수 오류')

        print(tabulate(sorted_list))

#for debug
pnt = StudentPoint()
pnt.dialog()




