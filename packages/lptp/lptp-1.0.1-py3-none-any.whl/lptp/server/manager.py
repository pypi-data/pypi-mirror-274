from typing import Callable, List, Optional
from .procedure import Procedure
import hashlib


class Manager:
    _procedures: List[Procedure]

    def __init__(self) -> None:
        self._procedures = []

    def procedure(self, coro, name: int = None, subtype: int = 0):
        procedure = Procedure(coro, name, subtype)
        self._procedures.append(procedure)
        self._reissue_names()
        return coro
    
    def sub_procedure(self, proc_func: Callable, subtype: int = 1):

        def inner(coro):
            procedure = self.get_by_func(proc_func)
            if not procedure:
                raise ValueError("Undefined procedure")
            return self.procedure(coro, procedure.name, subtype)
        return inner
    
    def _reissue_names(self):
        procedures = {
            procedure: list(filter(lambda p: p.name == procedure.name and p.subtype > 0, self._procedures))
            for procedure in self._procedures
            if procedure.subtype == 0
        }
        for i, (procedure, sub_procedures) in enumerate(sorted(procedures.items(), key=lambda p: p[0].get_func_name())):
            for proc in (procedure, *sub_procedures):
                proc.name = i

    def get_by_func(self, func: Callable) -> Optional[Procedure]:
        return next(filter(lambda proc: proc.coro == func, self._procedures), None)
    
    def get(self, name: int, subtype: int) -> Optional[Procedure]:
        return next(filter(lambda proc: proc.name == name and proc.subtype == subtype, self._procedures), None)
    
    def extend(self, manager: "Manager") -> None:
        if not isinstance(manager, Manager):
            raise TypeError("manager should be instance of Manager")
        self._procedures.extend(manager._procedures)
        self._reissue_names()

    @property
    def hash(self) -> str:
        procedures = b"".join([
            procedure.name.to_bytes() + procedure.subtype.to_bytes() + procedure.get_func_name().encode() + b"".join([
                field.name.to_bytes() + field.varname.encode() + str(field.field_type.data_type).encode() + str(field.default).encode()
                for field in procedure.get_fields()
            ])
            for procedure in self._procedures
        ])
        return hashlib.sha256(procedures).hexdigest()