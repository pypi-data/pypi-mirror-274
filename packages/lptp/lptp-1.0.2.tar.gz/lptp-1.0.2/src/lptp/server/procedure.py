from typing import Any, Callable, Coroutine, List, Optional
import inspect

from lptp.exceptions.data import DataException
from lptp.types.pds.pds import ProcedureDataStructure
from lptp.types.pds.types import FieldType


class Procedure:
    coro: Callable[..., Coroutine]
    name: Optional[int]
    subtype: int

    def __init__(self, coro: Callable[..., Coroutine], name: Optional[int], subtype: int) -> None:
        if name:
            if not isinstance(name, int):
                raise TypeError("name should be instance of int")
            if name < 1 or name > 255:
                raise ValueError("name should be within 1-0xFF")
        if not isinstance(subtype, int):
            raise TypeError("name should be instance of int")
        if subtype < 0 or subtype > 255:
            raise ValueError("subtype should be within 0xFF")
        
        self.coro = coro
        self.name = name
        self.subtype = subtype
        self.get_fields() # Check for errors

        if not self.get_return():
            raise TypeError(f"{self.get_return_datatype().__name__} is invalid FieldType")

    async def call(self, pds: ProcedureDataStructure) -> Any:
        if not self.validate_fields(pds):
            raise DataException("Invalid fields")
        res = await self.coro(*pds.get_params())
        if not isinstance(res, self.get_return_datatype()):
            raise TypeError(f"Procedure returned invalid response ({type(res).__name__})")
        return res

    def validate_fields(self, pds: ProcedureDataStructure) -> bool:
        fields = self.get_fields()
        valid_pds_fields = []
        for field in fields:
            pds_field = next(filter(lambda f: f.name == field.name, pds.fields), None)
            if not pds_field:
                if field.have_default: continue
                return False
            if not field.field_type.validate_field(pds_field):
                return False
            valid_pds_fields.append(pds_field)
        if len(valid_pds_fields) != len(pds.fields):
            return False
        return True

    def get_func_name(self) -> str:
        return self.coro.__name__

    def get_return_datatype(self) -> type:
        return inspect.getfullargspec(self.coro).annotations.get('return', None)

    def get_return(self) -> Optional[FieldType]:
        return FieldType.by_datatype(self.get_return_datatype())

    def get_fields(self) -> List["ProcedureParam"]:
        spec = inspect.getfullargspec(self.coro)
        defaults = dict(zip(spec.args[-len(spec.defaults):], spec.defaults)) if spec.defaults else {}
        params = {
            name: {
                "type": spec.annotations.get(name, Any)
            }
            for name in self.coro.__annotations__
            if name != "return"
        }
        for k,v in defaults.items():
            params[k]['default'] = v
        return [
            ProcedureParam(i, name, info['type'], 'default' in info, info.get('default', None))
            for i, (name, info) in enumerate(params.items())
        ]
    
    def __repr__(self) -> str:
        name = self.name
        subtype = self.subtype
        coro = self.coro
        return f"<{type(self).__name__} {name=} {subtype=} {coro=}>"


class ProcedureParam:
    name: int
    varname: str
    field_type: FieldType
    have_default: bool
    default: Any

    def __init__(self, name: int, varname: str, type_: type, have_default: bool = False, default: Any = None) -> None:
        if not isinstance(name, int):
            raise TypeError("name should be instance of int")
        if not isinstance(varname, str):
            raise TypeError("varname should be instance of str")
        if not isinstance(have_default, bool):
            raise TypeError("have_default should be instance of bool")
        
        field_type = FieldType.by_datatype(type_)
        if not field_type:
            raise TypeError(f"{type_.__name__} is invalid FieldType")
        
        self.name = name
        self.varname = varname
        self.field_type = field_type
        self.have_default = have_default
        self.default = default

    def __repr__(self) -> str:
        name = self.name
        varname = self.varname
        field_type = self.field_type
        have_default = self.have_default
        default = self.default
        return f"<{type(self).__name__} {name=} {varname=} {field_type=} {have_default=} {default=}>"