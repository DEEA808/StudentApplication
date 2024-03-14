class Student:
    def __init__(self,student_id,name,group):
        self.__student_id=student_id
        self.__name=name
        self.__group=group

    @property
    def student_id(self):
        return self.__student_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name=value

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, value):
        self.__group=value

    def __str__(self):
        return "ID: {} , Name: {}, from group {}".format(self.student_id, self.name, self.group)

    # def __eq__(self, other):
    #     return self.student_id == other.student_id

class Assignment:
    def __init__(self,assignment_id,description,deadline):
        self.__assignment_id=assignment_id
        self.__description=description
        self.__deadline=deadline

    @property
    def assignment_id(self):
        return self.__assignment_id

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description=value

    @property
    def deadline(self):
        return self.__deadline

    @deadline.setter
    def deadline(self, value):
        self.__deadline=value

    def __str__(self):
        return "ID: {} , Description: {}, Deadline {}".format(self.__assignment_id, self.description, self.deadline)

    # def __eq__(self, other):
    #     return self.assignment_id == other.assignment_id

class Grade:
    def __init__(self,assignment_id,student_id,grade_value):
        self.__assignment_id=assignment_id
        self.__student_id=student_id
        self.__grade_value=grade_value

    @property
    def assignment_id(self):
        return self.__assignment_id

    @property
    def student_id(self):
        return self.__student_id

    @property
    def grade_value(self):
        return self.__grade_value

    @grade_value.setter
    def grade_value(self, value):
        self.__grade_value=value

    def __str__(self):
        if self.grade_value == 0:
            return "Assigned to student {} the assignment {}".format(self.assignment_id, self.student_id)
        else:
            return "The grade for student {} for the assignment {} is {}".format(self.assignment_id, self.student_id,
                                                                                 float(self.grade_value))

    def __eq__(self, other):
        return self.student_id == other.student_id and self.assignment_id == other.assignment_id