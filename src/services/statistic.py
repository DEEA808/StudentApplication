from datetime import date

ONE_INDEX=1
ZERO_INDEX=0
NUMBER_DECIMALS=2

def unique(list_):
    list_set = set(list_)
    unique_list = (list(list_set))
    return unique_list


class Statistics:
    def __init__(self, grade_service, assignment_service, student_service):
        self.grade_service = grade_service
        self.assignment_service = assignment_service
        self.student_service = student_service

    @staticmethod
    def take_second(elem):
        return int(elem[ONE_INDEX])

    def get_unique_assignments(self):
        grades = self.grade_service.get_all()
        assignments = []
        for index in range(len(grades)):
            assignments.append(grades[index].assignment_id)
        unique_assignments = unique(assignments)
        return unique_assignments

    """
    STATISTICS 1
    """
    def statistics_1(self, assignment_id):
        grades = self.grade_service.get_all()
        students = []
        for index2 in range(len(grades)):
            if grades[index2].assignment_id == assignment_id:
                students.append((grades[index2].student_id, int(grades[index2].grade_value)))
        unique_students = unique(students)
        unique_students.sort(reverse=True, key=self.take_second)
        return unique_students

    """
    STATISTICS 2
    """
    def statistics_2(self):
        grades = self.grade_service.get_all()
        late_students_all = []
        for index in range(len(grades)):
            if grades[index].grade_value == ZERO_INDEX:
                assignment = self.assignment_service.get_assignment_by_id(grades[index].assignment_id)
                if assignment.deadline < date.today():
                    late_students_all.append(grades[index].student_id)
        unique_late_students_all = unique(late_students_all)
        return unique_late_students_all

    """
    STATISTICS 3
    """
    def statistics_3(self):
        grades = self.grade_service.get_all()
        students_all = []
        for index in range(len(grades)):
            students_all.append(grades[index].assignment_id)
        assignments_all = self.assignment_service.get_all()
        best_students = []
        for index in range(len(students_all)):
            number_of_grades = ZERO_INDEX
            sum_grades = ZERO_INDEX
            for index1 in range(len(assignments_all)):
                for index2 in range(len(grades)):
                    if assignments_all[index1].assignment_id == grades[index2].student_id:
                          if students_all[index] == grades[index2].assignment_id:
                                number_of_grades += ONE_INDEX
                                sum_grades += int(grades[index2].grade_value)
            if number_of_grades != ZERO_INDEX:
                if sum_grades != ZERO_INDEX:
                    average_grade = round(sum_grades / number_of_grades, NUMBER_DECIMALS)
                    best_students.append((students_all[index], average_grade))
                elif sum_grades == ZERO_INDEX:
                    average_grade = round(ZERO_INDEX)
                    best_students.append((students_all[index], average_grade))

        best_students = unique(best_students)
        best_students.sort(reverse=True, key=self.take_second)
        return best_students