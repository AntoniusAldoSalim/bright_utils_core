'''
Author: Ezra

Parameterized classes

I hope you dont mind, but I wrote these at work and stole them because theyre useful

# Description

These are extended generics which allow for direct access to the type arguments
during runtime. This could be used to access the constructor or methods.

The class creation method is defined in a subclass using the

__create_type__

method. 

# Partial Evaluation

If a parameterized type has not recieved all of it's type parameters, only static methods 
may be accessed. Techincally you can attempt access other methods, but success is not
guaranteed

Partial evaluation of a parameterized type will return a new type NT such that

__class_getitem__ now takes less parameters

__

- Generic type behaviour
- 




'''

from types import NoneType
from typing import Any, get_origin, Generic, Type, Self, ClassVar, TypeVar, TypeVarTuple


__all__ = ('ParameterizedClass',
           'ExposeType',
           'ExposeBiType',
           'ExposeTriType',
           'Expose4Type',
           'Expose5Type',
           'ExposeMultiType'
           )

T1 = TypeVar('T1', bound=Any)
T2 = TypeVar('T2', bound=Any)
T3 = TypeVar('T3', bound=Any)
T4 = TypeVar('T4', bound=Any)
T5 = TypeVar('T5', bound=Any)

TT = TypeVarTuple('TT')


def _get_unique_type_name(t: Any, existing_names: set[str] = set()):
    if get_origin(t):
        name = str(t)
    else:
        name = t.__name__

    name = '.'.join(name.split('.')[-2:])
    if name in existing_names:
        raise Exception('Error: calculated type name was not unique')
    return name


class ParameterizedClass(Generic[T1]):
    '''
    This is a base generic. DO NOT try creating types from this class. Only Subclass.

    cache is required so that ParameterizedClass[SomeType] = Res[SomeType]. This is crucial for many applications, including
    FastAPI.
    '''
    _cache : ClassVar[dict[Type[Any], Type[Self]]] = {}

    @classmethod
    def __create_type__(cls, t: Any) -> Type[Self]:
        '''
        Must be overridden
        '''
        return super().__class_getitem__(t)  # type:ignore # So that ParameterizedClass acts like Generic

    @classmethod
    def __create_type_name__(cls, t: Any) -> str:
        '''
        Optionally overridden
        '''
        name = _get_unique_type_name(t)
        return f'{cls.__name__}[{name}]'

    def __init_subclass__(cls) -> None:
        # Each subclass must have an independent cache, otherwise funny stuff happens
        cls._cache = {}
        return super().__init_subclass__()

    @classmethod
    def __class_getitem__(cls, wrapped: Any, *args: Any) -> Any:
        
        if isinstance(wrapped, tuple):
            wrapped = wrapped[0]
        if wrapped == Any or isinstance(wrapped, TypeVar):
            # We throw away the typevar information here.
            # Therefore we need to be careful that the typevar is always respected.
            return cls
        if wrapped is None:
            wrapped = NoneType
        if wrapped not in cls._cache:
            new_type = cls.__create_type__(wrapped)
            new_type.__name__ = cls.__create_type_name__(wrapped)
            cls._cache[wrapped] = new_type
        return cls._cache[wrapped]


class ExposeType(ParameterizedClass[T1]):
    type: ClassVar[Type[T1]] = Any

    @classmethod
    def __create_type__(cls, t: Any) -> Type[Self]:
        class __T(cls):
            type = t
        return __T


class MultiparameterizedClass(Generic[*TT]):
    '''
    This is a base generic. DO NOT try creating types from this class. Only Subclass.

    '''
    _cache : ClassVar[dict[tuple[Type[Any], ...], Type[Self]]] = {}

    @classmethod
    def __create_type__(cls, t: Any) -> Type[Self]:
        return super().__class_getitem__(*t)  # type: ignore

    @classmethod
    def __create_type_name__(cls, t: Any) -> str:
        typearg_name = ', '.join(_get_unique_type_name(t_) for t_ in t)
        return f'{cls.__name__}[{typearg_name}]'

    def __init_subclass__(cls) -> None:
        # Each subclass must have an independent cache, otherwise funny stuff happens
        cls._cache = {}
        return super().__init_subclass__()

    @classmethod
    def __class_getitem__(cls, t: Any = Any, *args: Any) -> Any:
        for t_ in t:
            if t_ == Any:
                return cls

        type_vars = {}
        for t_ in t:
            if isinstance(t_, TypeVar):
                type_vars[t_] = t_

        new_degree = len(type_vars)
        if new_degree == len(t):
            return super().__class_getitem__.__func__(cls, t)  # type: ignore
        elif new_degree > 0:
            new_cls = ParameterizedClass if new_degree == 1 else MultiparameterizedClass

            def assemble_types(new_types: Any):
                if not isinstance(new_types, tuple):
                    new_types = (new_types,)
                type_var_assignment = {k: t for k, t in zip(type_vars, new_types)}
                assembled_types = [type_var_assignment.get(t_, t_) for t_ in t]
                return (*assembled_types,)

            class __PartialParameterizedType(new_cls[*type_vars.keys()]):  # type: ignore
                @classmethod
                def __create_type__(_cls, t: Any) -> Type[Self]:
                    return cls.__create_type__.__func__(_cls, assemble_types(t))

                @classmethod
                def __create_type_name__(_cls, t: Any) -> str:
                    return cls.__create_type_name__.__func__(_cls, assemble_types(t))

            return __PartialParameterizedType

        t_list = list(t)
        for i in range(len(t_list)):
            if t_list[i] is None:
                t_list[i] = NoneType
        # return to tuple
        t = (*t_list,)

        if t not in cls._cache:
            new_type = cls.__create_type__(t)
            new_type.__name__ = cls.__create_type_name__(t)
            cls._cache[t] = new_type
        return cls._cache[t]


class ExposeBiType(MultiparameterizedClass[T1, T2]):
    type: tuple[Type[T1], Type[T2]] = Any, Any

    @classmethod
    def __create_type__(cls, t) -> Type[Self]:
        class __T(cls):
            type = t
        return __T


class ExposeTriType(MultiparameterizedClass[T1, T2, T3]):
    type: tuple[Type[T1], Type[T2], Type[T3]] = Any, Any, Any

    @classmethod
    def __create_type__(cls, t) -> Type[Self]:
        class __T(cls):
            type = t
        return __T


class Expose4Type(MultiparameterizedClass[T1, T2, T3, T4]):
    type: tuple[Type[T1], Type[T2], Type[T3], Type[T4]] = Any, Any, Any, Any

    @classmethod
    def __create_type__(cls, t) -> Type[Self]:
        class __T(cls):
            type = t
        return __T


class Expose5Type(MultiparameterizedClass[T1, T2, T3, T4, T5]):
    type: tuple[Type[T1], Type[T2], Type[T3], Type[T4], Type[T5]] = Any, Any, Any, Any, Any

    @classmethod
    def __create_type__(cls, t) -> Type[Self]:
        class __T(cls):
            type = t
        return __T


class ExposeMultiType(MultiparameterizedClass[*TT]):
    type: tuple[Type[Any], ...] = None

    @classmethod
    def __create_type__(cls, t) -> Type[Self]:
        class __T(cls):
            type = t
        return __T
