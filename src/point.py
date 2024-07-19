import json
import os
import tabulate
import config


class StudentPoint:
    def __init__(self, classroom):
        self.classroom = classroom
        self.point_dict = {}
        self.file_path = os.path.join(os.getcwd(), 'src', 'data', 'point', f'point{self.classroom}.json')
        self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, 'r') as pj:
                self.point_dict = json.load(pj)
        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {self.file_path}")
            self.point_dict = {}

    def write_modified_data(self):
        with open(self.file_path, 'w') as pj:
            json.dump(self.point_dict, pj, indent=2)

    def modify_point(self, std_name: str, point_to_modify: int):
        if self.point_dict.get(std_name) == None:
            self.point_dict[std_name] = point_to_modify
        else:
            self.point_dict[std_name] += point_to_modify

        self.write_modified_data()
    # def add_point(self, std_name, pnt_to_add):
    #     self.point_dict[std_name] = self.point_dict.get(std_name, 0) + pnt_to_add
    #     self.write_modified_data()

    # def remove_point(self, std_name, pnt_to_remove):
    #     self.point_dict[std_name] = self.point_dict.get(std_name, 0) - pnt_to_remove
    #     self.write_modified_data()

    # def dialog(self):
    #     student_name = input('이름: ').strip()
    #     if not student_name:
    #         print("올바른 이름을 입력해주세요.")
    #         return

    #     try:
    #         point_to_pm = int(input('추가 또는 차감할 포인트: '))
    #     except ValueError:
    #         print("올바른 숫자를 입력해주세요.")
    #         return

    #     what_to_do = input('추가 또는 차감: ').strip().lower()
    #     if what_to_do == '추가':
    #         self.add_point(student_name, point_to_pm)
    #     elif what_to_do == '차감':
    #         self.remove_point(student_name, point_to_pm)
    #     else:
    #         print("'추가' 또는 '차감'만 입력 가능합니다.")

    def print_point(self, sorting):
        head = ['이름', '포인트']
        if sorting == 'name':
            sorted_list = sorted(self.point_dict.items())
        elif sorting == 'point':
            sorted_list = sorted(self.point_dict.items(), key=lambda x: x[1], reverse=True)
        else:
            print("정렬 방식은 'name' 또는 'point'만 가능합니다.")
            return
        print(tabulate.tabulate(sorted_list, headers=head))
    
    def return_point(self, sorting='name'):
        head = ['이름', '포인트']
        if sorting == 'name':
            sorted_list = sorted(self.point_dict.items())
        elif sorting == 'point':
            sorted_list = sorted(self.point_dict.items(), key=lambda x: x[1], reverse=True)
        else:
            print("정렬 방식은 'name' 또는 'point'만 가능합니다.")

        return self.point_dict
    
    def return_student_num(self):
        return len(self.point_dict)
    

