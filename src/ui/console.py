from datetime import date
from src.domain.exceptions import StudentException,AssignmentException,RepositoryException,UndorRedoException

ZERO_INDEX=0
ONE_INDEX=1
ONE_OPTION=1
SECOND_OPTION=2
THIRD_OPTION=3
FOURTH_OPTION=4
FIFTH_OPTION=5
OPTION_SIX=6
OPTION_SEVEN=7
OPTION_EIGHT=8
OPTION_NINE=9
OPTION_TEN=10
OPTION_ELEVEN=11


class UI:
    def __init__(self, student_service, assignment_service, grade_service, statistics, undo_redo_service):
        self.student_service = student_service
        self.assignment_service = assignment_service
        self.grade_service = grade_service
        self.statistics = statistics
        self.undo_redo_service = undo_redo_service

    def add_student_ui(self):
        student_id = input("Student id: ")
        name = input("Name: ")
        group = input("Group: ")
        self.student_service.add(student_id, name, group)

    def remove_student_ui(self):
        student_id = input("Student id to remove: ")
        self.student_service.remove(student_id)
        self.grade_service.remove_by_student(student_id)

    def update_student_ui(self):
        student_id = input("Student id to update: ")
        new_name = input("New name: ")
        new_group = int(input("New group: "))
        self.student_service.update(student_id, new_name, new_group)

    def list_students_ui(self):
     students = self.student_service.get_all()
     try:
        if len(students) == ZERO_INDEX:
            raise ValueError("There are no students!")
        for student in students:
            print(str(student))
     except ValueError:
        print('There are no students')

    def add_assignment_ui(self):
        assignment_id = input("Assignment id: ")
        description = input("Description: ")
        deadline_year = int(input("Year: "))
        deadline_month = int(input("Month: "))
        deadline_day = int(input("Day: "))
        deadline = str(date(deadline_year, deadline_month, deadline_day))
        self.assignment_service.add(assignment_id, description, deadline)

    def remove_assignment_ui(self):
        assignment_id = input("Assignment id to remove: ")
        self.assignment_service.remove(assignment_id)
        self.grade_service.remove_by_assignment(assignment_id)

    def update_assignment_ui(self):
        assignment_id = input("Assignment id to update: ")
        new_description = input("New description: ")
        deadline_year = int(input("New year: "))
        deadline_month = int(input("New month: "))
        deadline_day = int(input("New day: "))
        new_deadline = date(deadline_year, deadline_month, deadline_day)
        self.assignment_service.update(assignment_id, new_description, new_deadline)

    def list_assignment_ui(self):
     assignments = self.assignment_service.get_all()
     try:
        if len(assignments) ==ZERO_INDEX:
            raise ValueError("There are no assignments!")
        for assignment in assignments:
            print(str(assignment))
     except ValueError:
         print('There are not asssignments')

    def assign_to_student_s_ui(self):
        print("LIST OF STUDENTS ID_S: ")
        students = self.student_service.get_all()
        students_id = []
        for index in range(len(students)):
            students_id.append(students[index].student_id)
        for id_ in students_id:
            print(str(id_))
        print("LIST OF ASSIGNMENTS IDS: ")
        assignments = self.assignment_service.get_all()
        assignments_id = []
        for index in range(len(assignments)):
            assignments_id.append(assignments[index].assignment_id)
        for id_ in assignments_id:
            print(str(id_))
        assignment_id = input("What assignment do you want to give? Enter the id: ")
        student_id = input("Enter the id of the student: ")
        if student_id in students_id:
            if assignment_id in assignments_id:
                self.grade_service.add(student_id, assignment_id, ZERO_INDEX)
                print("Successfully assigned!")
            else:
                raise RepositoryException("No such assignment id in the list!")
        else:
            raise RepositoryException("No such student id in the list!")

    def list_assigned_ui(self):
        grades = self.grade_service.get_all()
        if len(grades) == ZERO_INDEX:
            raise RepositoryException("The list of given assignments is empty!")
        for grade in grades:
            print(str(grade))

    def remove_assigned_ui(self):
        students = self.student_service.get_all()
        students_id = []
        for index in range(len(students)):
            students_id.append(students[index].student_id)
        assignments = self.assignment_service.get_all()
        assignments_id = []
        for index in range(len(assignments)):
            assignments_id.append(assignments[index].assignment_id)
        student_id = input("Enter the id of the student: ")
        assignment_id = input("What assignment do you want to remove? Enter the id: ")
        if student_id in students_id:
            if assignment_id in assignments_id:
                self.grade_service.remove(student_id, assignment_id)
            else:
                raise RepositoryException("No such assignment id in the list!")
        else:
            raise RepositoryException("No such student id in the list!")

    @staticmethod
    def unique(list_):
        list_set = set(list_)
        unique_list = (list(list_set))
        return unique_list

    def grade_assignment_ui(self):
        grades = self.grade_service.get_all()
        students = []
        print("The students that have assignments are: ")
        for index in range(len(grades)):
            students.append(grades[index].assignment_id)
        unique_students = self.unique(students)
        if len(unique_students) == ZERO_INDEX:
            raise RepositoryException("No student with assignments.")
        for index in range(len(unique_students)):
            print(unique_students[index])
        student_id = input("Enter the student you want to grade: ")
        if student_id not in unique_students:
            raise RepositoryException("Invalid student id")
        else:
            assignments = []
            grade_type = []
            print("This student has the following assignments: ")
            for index in range((len(grades))):
                if grades[index].assignment_id == student_id:
                    if grades[index].grade_value == ZERO_INDEX:
                        assignments.append(grades[index].student_id)
                        grade_type.append({'assignment': grades[index].student_id, 'status': "ungraded"})
                    else:
                        assignments.append(grades[index].student_id)
                        grade_type.append({'assignment': grades[index].student_id, 'status': "graded"})
            for index in range(len(assignments)):
                print(assignments[index] + ", " + grade_type[index]['status'])
            student_id = input("Enter the id of the assignment you want to grade: ")
            if student_id in assignments:
                for index_type in range(len(grade_type)):
                    if grade_type[index_type]['assignment'] == student_id:
                        if grade_type[index_type]['status'] == "graded":
                            raise RepositoryException("This assignment has already been graded.")
                grade = input("Enter the grade: ")
                if grade == '':
                    raise ValueError("Grade input is empty.")
                self.grade_service.grade(student_id,student_id, grade)
            else:
                raise RepositoryException("Invalid id, there's no student id with the provided assignment!")
            for index in range(len(grade_type)):
                for index1 in range(len(grades)):
                    if grades[index1].student_id == grade_type[index]['assignment']:
                        if grades[index1].grade_value== ZERO_INDEX:
                            grade_type[index]['status'] = "ungraded"
                        else:
                            grade_type[index]['status'] = "graded"

    def statistics_1_ui(self):
        print("--All students who received a given assignment, ordered by average grade for that assignment--")
        unique_assignments = self.statistics.get_unique_assignments()
        for index in range(len(unique_assignments)):
            print("ASSIGNMENT: {}".format(unique_assignments[index]))
            print("STUDENT ID ---------- GRADE")
            unique_students = self.statistics.statistics_1(unique_assignments[index])
            for index1 in range(len(unique_students)):
                if unique_students[index1][ONE_INDEX] != ZERO_INDEX:
                    print(unique_students[index1][ZERO_INDEX] + "     ----------   " + str(unique_students[index1][1]))
                elif unique_students[index1][ONE_INDEX] == ZERO_INDEX:
                    print(unique_students[index1][ZERO_INDEX] + "     ---------- ungraded")

    def statistics_2_ui(self):
        print("--All students who are late in handing in at least one assignment--")
        unique_late_students_all = self.statistics.statistics_2()
        if len(unique_late_students_all) != ZERO_INDEX:
            for index in range(len(unique_late_students_all)):
                print(unique_late_students_all[index])
        else:
            print("No students that are late for all the given assignments.")

    def statistics_3_ui(self):
        print("--Students with the best school situation, "
              "sorted in descending order of the average grade received for all assignments--")
        best_students=self.statistics.statistics_3()
        for index in range(len(best_students)):
                print("Student ID: {}, average grade: {}".format(best_students[index][0], best_students[index][1]))
    def show_menu_ui(self):
        print("OPTIONS: ")
        print("0. Exit.")
        print("1. Add a/an student/assignment.")
        print("2. Remove a/an student/assignment.")
        print("3. Update a/an student/assignment.")
        print("4. List all students/assignments.")
        print("5. Assign an assignment to a student.")
        print("6. List all the given assignments and grades.")
        print("7. Remove an assigned assignment.")
        print("8. Grade an assignment.")
        print("9. STATISTICS")
        print("10.UNDO")
        print("11.REDO")

    def submenu_1_ui(self):
        print("OPTIONS: ")
        print("1. Add a student.")
        print("2. Add an assignment.")

    def submenu_2_ui(self):
        print("OPTIONS: ")
        print("1. Remove a student.")
        print("2. Remove an assignment.")

    def submenu_3_ui(self):
        print("OPTIONS: ")
        print("1. Update a student.")
        print("2. Update an assignment.")

    def submenu_4_ui(self):
        print("OPTIONS: ")
        print("1. List all students.")
        print("2. List all assignments.")

    def submenu_9_ui(self):
        print("OPTIONS: ")
        print("1. List all students who received a given assignment, ordered by average grade for that assignment.")
        print("2. List all students who are late in handing in at least one assignment."
              "\n   These are all the students who have an ungraded assignment for which the deadline has passed.")
        print("3. List students with the best school situation, "
              "sorted in descending order of the average grade received for all assignments.")

    def start_ui(self):
        self.student_service.initialise()
        self.assignment_service.initialise()
        self.grade_service.initialise()
        done = False
        self.show_menu_ui()
        while not done:
            try:
                option = int(input("Enter option: "))
                if option == ZERO_INDEX:
                    done = True
                    print("The end")
                elif option ==ONE_OPTION:
                    self.submenu_1_ui()
                    option_1 = int(input("Enter option: "))
                    if option_1 == ONE_OPTION:
                        self.add_student_ui()
                    elif option_1 == SECOND_OPTION:
                        self.add_assignment_ui()
                    else:
                        print("Bad input!")
                elif option == SECOND_OPTION:
                    self.submenu_2_ui()
                    option_2 = int(input("Enter option: "))
                    if option_2 == ONE_OPTION:
                        self.remove_student_ui()
                    elif option_2 == SECOND_OPTION:
                        self.remove_assignment_ui()
                    else:
                        print("Bad input!")
                elif option == THIRD_OPTION:
                    self.submenu_3_ui()
                    option_3 = int(input("Enter option: "))
                    if option_3 == ONE_OPTION:
                        self.update_student_ui()
                    elif option_3 == SECOND_OPTION:
                        self.update_assignment_ui()
                    else:
                        print("Bad input!")
                elif option == FOURTH_OPTION:
                    self.submenu_4_ui()
                    option_4 = int(input("Enter option: "))
                    if option_4 == ONE_OPTION:
                        self.list_students_ui()
                    elif option_4 == SECOND_OPTION:
                        self.list_assignment_ui()
                elif option == FIFTH_OPTION:
                    self.assign_to_student_s_ui()
                elif option == OPTION_SIX:
                    self.list_assigned_ui()
                elif option == OPTION_SEVEN:
                    self.remove_assigned_ui()
                elif option == OPTION_EIGHT:
                    self.grade_assignment_ui()
                elif option == OPTION_NINE:
                    self.submenu_9_ui()
                    option_9 = int(input("Enter option: "))
                    if option_9 == ONE_OPTION:
                        self.statistics_1_ui()
                    elif option_9 == SECOND_OPTION:
                        self.statistics_2_ui()
                    elif option_9 == THIRD_OPTION:
                        self.statistics_3_ui()
                    else:
                        print("Bad input!")
                elif option == OPTION_TEN:
                    self.undo_redo_service.undo()
                elif option == OPTION_ELEVEN:
                    self.undo_redo_service.redo()
                else:
                    print("Bad input!")
            except RepositoryException as re:
                print(re)
            except StudentException as se:
                print(se)
            except AssignmentException as ae:
                print(ae)
            except ValueError as ve:
                print(ve)
            except UndorRedoException as ure:
                print(ure)

