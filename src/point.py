import json
import os
import tabulate

class StudentPoint:
    def __init__(self):
        with open(f'{os.getcwd()}\\src\\point.json') as pj:
            self.point_dict : dict = json.load(pj)

    def __write_modified_data(self): #수정된 데이터 저장
        with open(f'{os.getcwd()}\\src\\point.json', 'w') as pj:
            json.dump(self.point_dict, pj, indent = 2, ensure_ascii = False)

    def __add_point(self, std_name, pnt_to_add): # 포인트 추가
        #self.point_dict[std_name] += pnt_to_add
        #self.__write_modified_data()
        if self.point_dict.get(std_name) == None:
            self.point_dict[std_name] = pnt_to_add
        else:
            self.point_dict[std_name] += pnt_to_add

        self.__write_modified_data()

    def __remove_point(self, std_name, pnt_to_add): #포인트 차감
        self.point_dict[std_name] += pnt_to_add
        self.__write_modified_data()

    def dialog(self): #질문한 후 지정 명령 실행
        student_name = input('이름: ')
        point_to_pm = int(input('추가 또는 차감할 포인트: '))
        what_to_do = input('추가 또는 차감: ')
        if what_to_do == '추가':
            self.__add_point(student_name, point_to_pm)
        elif what_to_do == '차감':
            self.__remove_point(student_name, point_to_pm)

    def print_point(self, sorting): #표 출력
        head = ['이름', '포인트']
    
        if sorting == 'name':
                sorted_list = sorted(self.point_dict.items())
        elif sorting == 'point':
                sorted_list = sorted(self.point_dict.items(), key=lambda x: x[1], reverse=True)

        print(tabulate.tabulate(sorted_list, headers=head))

#for debug
pnt = StudentPoint()
pnt.dialog()
pnt.print_point('point')




