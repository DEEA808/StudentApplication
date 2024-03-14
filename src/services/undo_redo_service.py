from src.domain.exceptions import UndorRedoException

ONE_INDEX=1
ZERO_INDEX=0

class UndoRedoService:
    def __init__(self):
        self._history=[]
        self._position=-ONE_INDEX

    def record(self,operation):
        self._history=self._history[ZERO_INDEX:self._position+ONE_INDEX]
        self._history.append(operation)
        self._position=self._position+ONE_INDEX


    def undo(self):
        if self._position==-ONE_INDEX:
            raise UndorRedoException('Cant undo')

        self._history[self._position].undo()
        self._position=self._position-ONE_INDEX
        return True

    def redo(self):
        if self._position+ONE_INDEX==len(self._history):
            raise UndorRedoException('Cant redo')
        self._position=self._position+ONE_INDEX
        self._history[self._position].redo()
        return True


class Operation:
    def __init__(self,function_undo,function_redo):
        self._function_undo=function_undo
        self._function_redo=function_redo

    def undo(self):
        self._function_undo()

    def redo(self):
        self._function_redo()

class FunctionCall:
    def __init__(self,function_name,*function_params):
        self._function_name=function_name
        self._function_params=function_params

    def call(self):
        return self._function_name(*self._function_params)

    def __call__(self):
        return self.call()

