import random
import string
from datetime import date
from src.domain.entity import Student,Assignment,Grade
from src.domain.exceptions import RepositoryException
from src.services.undo_redo_service import FunctionCall,Operation

FIRST_INDEX_FOR_GROUP=911
SECOND_INDEX_FOR_GROUP=917
FIRST_DAY_INDEX=1
SECOND_DAY_INDEX=30
PARTICULARY_DAY_INDEX=28
ONE_INDEX=1
TWO_INDEX=2
ZERO_INDEX=0
FIRST_GRADE_INDEX=0
SECOND_GRADE_INDEX=10
TEN_INDEX=10
FOUR_INDEX=4
FIRST_YEAR_INDEX=2020
SECOND_YEAR_INDEX=2022
FIRST_MOUNTH_INDEX=1
SECOND_MOUNTH_INDEX=12
FIFTEEN_INDEX=15

class StudentService:
    def __init__(self, student_repository, student_validator, undo_redo_service, grade_service):
        self._undo_redo_service = undo_redo_service
        self._student_repository = student_repository
        self._student_validator = student_validator
        self._grade_service = grade_service

    def add(self, student_id, name, group):
        student = self.add_without_record(student_id, name, group)
        undo_ = FunctionCall(self.remove_without_record, student.student_id)
        redo_ = FunctionCall(self.add_without_record, student.student_id, student.name, student.group)
        self._undo_redo_service.record(Operation(undo_, redo_))

    def add_without_record(self, student_id, name, group):
        student = Student(student_id, name, group)
        self._student_validator.validate(student)
        self._student_repository.add(student)
        return student

    def add_student_and_grades(self, student_id, name, group, list_of_grades):
        student = Student(student_id, name, group)
        self._student_validator.validate(student)
        self._student_repository.add(student)
        if list_of_grades is not None:
            for grade in list_of_grades:
                self._grade_service.add_grade_without_record(grade[ZERO_INDEX], grade[ONE_INDEX], grade[TWO_INDEX])

    def remove(self, student_id):
        student, list_of_grades = self.remove_without_record(student_id)
        undo_ = FunctionCall(self.add_student_and_grades, student.student_id, student.name, student.group,
                             list_of_grades)
        redo_ = FunctionCall(self.remove_without_record, student.student_id)
        self._undo_redo_service.record(Operation(undo_, redo_))

    def remove_without_record(self, student_id):
        check_student_id = Student(student_id, 'test name', FIRST_INDEX_FOR_GROUP)
        self._student_validator.validate(check_student_id)
        student = self._student_repository.remove_student(student_id)
        list_of_grades = self._grade_service.remove_by_student(student)
        return student, list_of_grades

    def update(self, student_id, new_name, new_group):
        old_student_name, old_group = self.update_without_record(student_id, new_name, new_group)
        undo_ = FunctionCall(self.update_without_record, student_id, old_student_name, old_group)
        redo_ = FunctionCall(self.update_without_record, student_id, new_name, new_group)
        self._undo_redo_service.record(Operation(undo_, redo_))

    def update_without_record(self, student_id, new_name, new_group):
        old_student_name, old_group = self._student_repository.update(student_id, new_name, new_group)
        return old_student_name, old_group

    def get_all(self):
        return self._student_repository.get_all_students()

    @staticmethod
    def random_student_id(length):
        letters_and_digits = string.ascii_letters + string.digits
        student_id = ''.join((random.choice(letters_and_digits) for index in range(length)))
        return student_id

    def initialise(self):
        name_list = ["Rus Andreea","Teglas Alex","Iuga Maria","Malina Chifor","Braica Alexandra",
                     "Ignat Alex","Rus Ana","Pop Vlad","Ion Dragos","Stoica Patricia"
                     "Dan Maria","Popa Ioana","Badiu Larisa","Todea David","Turc Paula"
                     "Florin Daniel","Munte Bianca","Sara Trif","Marc Popescu"]
        for index in range(TEN_INDEX):
            student_id = self.random_student_id(FOUR_INDEX)
            name = random.choice(name_list)
            group = random.randint(FIRST_INDEX_FOR_GROUP, SECOND_INDEX_FOR_GROUP)
            self.add_without_record(student_id, name, group)

class AssignmentService:
    def __init__(self, assignment_repository, assignment_validator, undo_redo_service, grade_service):
        self._undo_redo_service = undo_redo_service
        self._assignment_repository = assignment_repository
        self._assignment_validator = assignment_validator
        self._grade_service = grade_service

    def add(self, assignment_id, description, deadline):
        new_assignment = self.add_without_record(assignment_id, description, deadline)
        self._assignment_validator.validate(new_assignment)
        undo_ = FunctionCall(self.remove_without_record, assignment_id)
        redo_ = FunctionCall(self.add_without_record, new_assignment.assignment_id, new_assignment.description,
                             new_assignment.deadline)
        self._undo_redo_service.record(Operation(undo_, redo_))

    def add_without_record(self, assignment_id, description, deadline):
        assignment = Assignment(assignment_id, description, deadline)
        self._assignment_repository.add(assignment)
        return assignment

    def add_assignment_and_grades(self, assignment_id, description, deadline, list_of_grades):
        new_assignment = Assignment(assignment_id, description, deadline)
        self._assignment_repository.add(new_assignment)
        if list_of_grades is not None:
            for grade in list_of_grades:
                self._grade_service.add_grade_without_record(grade[ZERO_INDEX], grade[ONE_INDEX], grade[TWO_INDEX])

    def remove(self, assignment_id):
        assignment, list_of_grades = self.remove_without_record(assignment_id)
        undo_ = FunctionCall(self.add_assignment_and_grades, assignment.assignment_id, assignment.description,
                             assignment.deadline, list_of_grades)
        redo_ = FunctionCall(self.remove_without_record, assignment.assignment_id)
        self._undo_redo_service.record(Operation(undo_, redo_))

    def remove_without_record(self, assignment_id):
        check_assignment = Assignment(assignment_id, "description", date(FIRST_YEAR_INDEX, FIRST_DAY_INDEX, ONE_INDEX))
        self._assignment_validator.validate(check_assignment)
        assignment = self._assignment_repository.remove_assignment(assignment_id)
        list_of_grades = self._grade_service.remove_by_assignment(assignment)
        return assignment, list_of_grades

    def update(self, assignment_id, new_description, new_deadline):
        old_description, old_deadline = self.update_without_record(assignment_id, new_description, new_deadline)
        undo_ = FunctionCall(self.update_without_record, assignment_id, old_description, old_deadline)
        redo_ = FunctionCall(self.update_without_record, assignment_id, new_description, new_deadline)
        self._undo_redo_service.record(Operation(undo_, redo_))

    def update_without_record(self, assignment_id, new_description, new_deadline):
        old_description, old_deadline = self._assignment_repository.update(assignment_id, new_description, new_deadline)
        return old_description, old_deadline

    def get_assignment_by_id(self, assignment_id):
        return self._assignment_repository.get_assignment_by_id(assignment_id)

    def get_all(self):
        return self._assignment_repository.get_all_assignments()

    @staticmethod
    def random_assignment_id(letter_count, digits_count):
        letters = string.ascii_letters
        digits = string.digits
        assignment_id = ''.join(random.choice(letters) for index in range(letter_count))
        assignment_id += ''.join(random.choice(digits) for index in range(digits_count))
        return assignment_id

    def initialise(self):
        description_list = ["Algebra test", "CSA test", "FP test", "Mathematical Analysis test",
                            "Computational Logic test",
                            "Algebra hw", "CSA hw", "FP hw", "Mathematical Analysis hw", "Computational Logic hw",
                            "Chemistry hw", "Biology hw", "History hw", "Literature hw", "English hw",
                            "Chemistry test", "Biology test", "History test", "Literature test", "English test"]
        for index in range(TEN_INDEX):
            assignment_id = self.random_assignment_id(ONE_INDEX, ONE_INDEX)
            description = random.choice(description_list)
            deadline_year = random.randint(FIRST_YEAR_INDEX, SECOND_YEAR_INDEX)
            deadline_month = random.randint(FIRST_MOUNTH_INDEX, SECOND_MOUNTH_INDEX)
            if deadline_month == TWO_INDEX:
                deadline_day = random.randint(FIRST_DAY_INDEX, PARTICULARY_DAY_INDEX)
            else:
                deadline_day = random.randint(FIRST_DAY_INDEX, SECOND_DAY_INDEX)
            deadline = date(deadline_year, deadline_month, deadline_day)
            self.add_without_record(assignment_id, description, deadline)


class GradeService:
    def __init__(self, student_repository, assignment_repository, grade_repository, undo_redo_service):
        self._student_repository = student_repository
        self._assignment_repository = assignment_repository
        self._undo_redo_service = undo_redo_service
        self._grade_repository = grade_repository

    def add(self, student_id, assignment_id, grade):
        self.add_grade_without_record(student_id, assignment_id, grade)
        undo_ = FunctionCall(self._grade_repository.remove_last_grades, ONE_INDEX)
        redo_ = FunctionCall(self.add_grade_without_record, student_id, assignment_id, grade)
        self._undo_redo_service.record(Operation(undo_, redo_))

    def add_grade_without_record(self, student_id, assignment_id, grade):
        new_grade = Grade(student_id, assignment_id, grade)
        self._grade_repository.add(new_grade)
        return new_grade

    def remove(self, student_id, assignment_id):
        list_of_grades = []
        for grade in self._grade_repository.get_grades_list():
            if grade.assignment_id == student_id:
                if grade.student_id == assignment_id:
                    list_of_grades.append(grade)
                    self._grade_repository.remove(grade.student_id, grade.assignment_id)
        return list_of_grades

    def remove_by_student(self, student_id):
        list_of_grades = []
        for grade in self._grade_repository.get_grades_list():
            if grade.student_id == student_id:
                list_of_grades.append(grade)
                self._grade_repository.remove(grade.student_id, grade.assignment_id)
        return list_of_grades

    def remove_by_assignment(self, assignment_id):
        list_of_grades = []
        for grade in self._grade_repository.get_grades_list():
            if grade.assignment_id == assignment_id:
                list_of_grades.append(grade)
                self._grade_repository.remove(grade.student_id, grade.assignment_id)
        return list_of_grades


    def is_graded(self, student_id, assignment_id):
        for grade in self._grade_repository.get_all_grades():
            if grade.student_id == student_id:
                if grade.assignment_id == assignment_id:
                    return True
        return False

    def add_grade_to_group(self, assignment_id, group):
        number_of_adds = self.add_to_group_without_record(assignment_id, group)
        undo_ = FunctionCall(self._grade_repository.remove_last_grades, number_of_adds)
        redo_ = FunctionCall(self.add_grade_to_group, assignment_id, group)
        self._undo_redo_service.record(Operation(undo_, redo_))

    def add_to_group_without_record(self, assignment_id, group):
        number_of_adds = ZERO_INDEX
        if group <FIRST_INDEX_FOR_GROUP or group > SECOND_INDEX_FOR_GROUP:
            raise ValueError("Invalid student group!")
        for student in self._student_repository.get_all_students():
            if student.group == group:
                if not self.is_graded(student.student_id, assignment_id):
                    self.add_grade_without_record(student.student_id, assignment_id, ZERO_INDEX)
                    number_of_adds += ONE_INDEX
        return number_of_adds

    def grade(self, student_id, assignment_id, grade):
        self.grade_without_record(student_id, assignment_id, grade)
        undo_ = FunctionCall(self.grade_without_record, student_id, assignment_id, ZERO_INDEX)
        redo_ = FunctionCall(self.grade_without_record, student_id, assignment_id, grade)
        self._undo_redo_service.record(Operation(undo_, redo_))

    def grade_without_record(self, student_id, assignment_id, grade):
        if self._grade_repository.search_if_grade_exists(student_id, assignment_id) is False:
            raise RepositoryException("The student and the assignment are not linked!")
        self._grade_repository.grade(student_id, assignment_id, grade)

    def get_all(self):
        return self._grade_repository.get_grades_list()

    def initialise(self):
        for index in range(FIFTEEN_INDEX):
            random_student_id = self._student_repository.get_random_id()
            random_assignment_id = self._assignment_repository.get_random_id()
            random_grade = float(random.randint(FIRST_GRADE_INDEX, SECOND_GRADE_INDEX))
            random_grading = Grade(random_student_id, random_assignment_id, random_grade)
            if random_grading not in self._grade_repository.get_grades_list():
                self._grade_repository.add(random_grading)
            else:
                index -= ONE_INDEX