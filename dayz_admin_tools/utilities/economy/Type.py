# .//*[@folder]/file[@type='types']


class Type:

    _name: str
    _filesource: str

    def __init__(self, name: str, filesource: str):
        self._name = name
        self._filesource = filesource

    @property
    def name(self) -> str:
        return self._name

    @property
    def filesource(self) -> str:
        return self._filesource

    #@name.setter
    #def name(self, name: str):
    #    self._name = name

