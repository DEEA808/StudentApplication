class StudentException(Exception):
    def __init__(self, msg=''):
        self._message = msg

    def getMessage(self):
        return self._message

    def __str__(self):
        return self._message

class AssignmentException(Exception):
    def __init__(self, msg=''):
            self._message = msg

    def getMessage(self):
            return self._message

    def __str__(self):
            return self._message

class RepositoryException(Exception):
    def __init__(self,msg=''):
        self._message=msg

    def GetMessage(self):
        return self._message

    def __str__(self):
        return self._message

class UndorRedoException(Exception):
    def __init__(self,msg=''):
        self._message=msg

    def GetMessage(self):
        return self._message

    def __str__(self):
        return self._message