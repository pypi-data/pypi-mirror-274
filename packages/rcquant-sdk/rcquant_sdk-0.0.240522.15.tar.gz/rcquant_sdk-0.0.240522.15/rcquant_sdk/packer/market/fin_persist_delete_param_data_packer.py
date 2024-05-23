from ...interface import IPacker


class FinPersistDeleteParamDataPacker(IPacker):
    def __init__(self, obj) -> None:
        super().__init__(obj)

    def obj_to_tuple(self):
        return [str(self._obj.InstrumentID), str(self._obj.Period), int(self._obj.StartDate), int(self._obj.EndDate)]

    def tuple_to_obj(self, t):
        if len(t) >= 5:
            self._obj.InstrumentID = t[0]
            self._obj.Period = t[1]
            self._obj.StartDate = t[2]
            self._obj.EndDate = t[3]

            return True
        return False
