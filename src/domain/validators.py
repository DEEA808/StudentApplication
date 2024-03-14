from src.domain.exceptions import StudentException,AssignmentException

NUMBER_OF_STUDENT_ID_CHARACTERS=4
NONE=0
FIRST_GROUP_INDEX=911
SECOND_GROUP_INDEX=917
NUMBER_OF_ASSIGNMENT_ID_CHARACTERS=2
DATE_LEN=10

class StudentValidator:
    @staticmethod
    def validate(student):
        if len(str(student.student_id))!=NUMBER_OF_STUDENT_ID_CHARACTERS:
            raise StudentException("Invalid id")
        if len(str(student.name))==NONE:
            raise StudentException("You should add a name")
        if int(student.group)<FIRST_GROUP_INDEX and int(student.group)>SECOND_GROUP_INDEX:
            raise StudentException("This group does not exist")

class AssignmentValidator:
    @staticmethod
    def  validate(assignment):
        if len(str(assignment.assignment_id))!=NUMBER_OF_ASSIGNMENT_ID_CHARACTERS:
            raise AssignmentException("Invalid id")
        if len(str(assignment.description))==NONE:
            raise AssignmentException("You sould add a description")
        if len(str(assignment.deadline))!=DATE_LEN:
            raise AssignmentException("Invalid deadline")

