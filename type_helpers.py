from typing import dataclass_transform, get_args, get_origin, overload, ParamSpec, TypeVar, Callable, Concatenate, Any, Literal, Type, Optional, Union
from types import UnionType
import mongoengine.fields as fields

__all__ = 'hint_inherit_paramspec', 'hint_remove_params', 'hint_add_params', 'hint_return_type', 'literal_get', 'mongoengine_field_specifiers', 'hint_mongo_constructor', 'get_type_tuple_from_union', 'hint_function_type'

####
# TYPE HINTER DECORATORS
####


def literal_get(t: Type[Any], index: int) -> Type[Any] | None:
    if get_origin(t) == Literal:
        return get_args(t)[index]
    return None


P1 = ParamSpec('P1')
P2 = ParamSpec('P2')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
R = TypeVar('R')


def donothing(f: Any):
    return f

# Yes. this is literally on a case-by-case basis.
# But it works!


@overload
def hint_inherit_paramspec(fn: Callable[P1, Any]) -> Callable[[Callable[..., R]], Callable[P1, R]]:
    ...


@overload
def hint_inherit_paramspec(fn: Callable[P1, Any], keep: Literal[1]) -> Callable[[Callable[Concatenate[T1, P2], R]], Callable[Concatenate[T1, P1], R]]:
    ...


@overload
def hint_inherit_paramspec(fn: Callable[P1, Any], keep: Literal[2]) -> Callable[[Callable[Concatenate[T1, T2, P2], R]], Callable[Concatenate[T1, T2, P1], R]]:
    ...


@overload
def hint_inherit_paramspec(fn: Callable[P1, Any], keep: Literal[4]) -> Callable[[Callable[Concatenate[T1, T2, T3, P2], R]], Callable[Concatenate[T1, T2, T3, P1], R]]:
    ...


@overload
def hint_inherit_paramspec(fn: Callable[P1, Any], add_types: Type[T1]) -> Callable[[Callable[..., R]], Callable[Concatenate[T1, P1], R]]:
    ...


@overload
def hint_inherit_paramspec(fn: Callable[P1, Any], add_types: tuple[Type[T1]]) -> Callable[[Callable[..., R]], Callable[Concatenate[T1, P1], R]]:
    ...


@overload
def hint_inherit_paramspec(fn: Callable[P1, Any], add_types: tuple[Type[T1], Type[T2]]) -> Callable[[Callable[..., R]], Callable[Concatenate[T1, T2, P1], R]]:
    ...


@overload
def hint_inherit_paramspec(fn: Callable[P1, Any], add_types: tuple[Type[T1], Type[T2], Type[T3]]) -> Callable[[Callable[..., R]], Callable[Concatenate[T1, T2, T3, P1], R]]:
    ...


@overload
def hint_inherit_paramspec(fn: Callable[P1, Any], add_types: tuple[Type[T1], Type[T2], Type[T3], Type[T4]]) -> Callable[[Callable[..., R]], Callable[Concatenate[T1, T2, T3, T4, P1], R]]:
    ...


def hint_inherit_paramspec(*args: Any, **kwargs: Any) -> Any:
    '''
    Copies the input parameter specification of the input function to the decorated function

    keep: int: How many parameters to keep from the decorated function, before the new paramspec begins
    add_types: Tuple[Type]: adds extra types at the beginning ofthe function.

    keep & add_types are mutually exclusive

    0 < keep <= 4
    0 < len(add_types) <= 4
    '''
    return donothing


@overload
def hint_remove_params(n: Literal[4]) -> Callable[[Callable[Concatenate[Any, Any, Any, Any, P1], R]], Callable[P1, R]]:
    ...


@overload
def hint_remove_params(n: Literal[3]) -> Callable[[Callable[Concatenate[Any, Any, Any, P1], R]], Callable[P1, R]]:
    ...


@overload
def hint_remove_params(n: Literal[2]) -> Callable[[Callable[Concatenate[Any, Any, P1], R]], Callable[P1, R]]:
    ...


@overload
def hint_remove_params(n: Literal[1]) -> Callable[[Callable[Concatenate[Any, P1], R]], Callable[P1, R]]:
    ...


@overload
def hint_remove_params(n: Literal[4], keep: Literal[1]) -> Callable[[Callable[Concatenate[T1, Any, Any, Any, Any, P1], R]], Callable[Concatenate[T1, P1], R]]:
    ...


@overload
def hint_remove_params(n: Literal[3], keep: Literal[1]) -> Callable[[Callable[Concatenate[T1, Any, Any, Any, P1], R]], Callable[Concatenate[T1, P1], R]]:
    ...


@overload
def hint_remove_params(n: Literal[2], keep: Literal[1]) -> Callable[[Callable[Concatenate[T1, Any, Any, P1], R]], Callable[Concatenate[T1, P1], R]]:
    ...


@overload
def hint_remove_params(n: Literal[1], keep: Literal[1]) -> Callable[[Callable[Concatenate[T1, Any, P1], R]], Callable[Concatenate[T1, P1], R]]:
    ...


@overload
def hint_remove_params(n: Literal[4], keep: Literal[2]) -> Callable[[Callable[Concatenate[T1, T2, Any, Any, Any, Any, P1], R]], Callable[Concatenate[T1, T2, P1], R]]:
    ...


@overload
def hint_remove_params(n: Literal[3], keep: Literal[2]) -> Callable[[Callable[Concatenate[T1, T2, Any, Any, Any, P1], R]], Callable[Concatenate[T1, T2, P1], R]]:
    ...


@overload
def hint_remove_params(n: Literal[2], keep: Literal[2]) -> Callable[[Callable[Concatenate[T1, T2, Any, Any, P1], R]], Callable[Concatenate[T1, T2, P1], R]]:
    ...


@overload
def hint_remove_params(n: Literal[1], keep: Literal[2]) -> Callable[[Callable[Concatenate[T1, T2, Any, P1], R]], Callable[Concatenate[T1, T2, P1], R]]:
    ...


@overload
def hint_remove_params(n: Literal[4], keep: Literal[3]) -> Callable[[Callable[Concatenate[T1, T2, T3, Any, Any, Any, Any, P1], R]], Callable[Concatenate[T1, T2, T3, P1], R]]:
    ...


@overload
def hint_remove_params(n: Literal[3], keep: Literal[3]) -> Callable[[Callable[Concatenate[T1, T2, T3, Any, Any, Any, P1], R]], Callable[Concatenate[T1, T2, T3, P1], R]]:
    ...


@overload
def hint_remove_params(n: Literal[2], keep: Literal[3]) -> Callable[[Callable[Concatenate[T1, T2, T3, Any, Any, P1], R]], Callable[Concatenate[T1, T2, T3, P1], R]]:
    ...


@overload
def hint_remove_params(n: Literal[1], keep: Literal[3]) -> Callable[[Callable[Concatenate[T1, T2, T3, Any, P1], R]], Callable[Concatenate[T1, T2, T3, P1], R]]:
    ...


def hint_remove_params(*args: Any, **kwargs: Any) -> Any:
    '''
    Removes `n` parameters from the beginning of the paramspec.
    You can skip parameters before removing using the `keep` argument.
    '''
    return donothing


@overload
def hint_add_params(add_types: Type[T1], offset: Literal[0] | None) -> Callable[[Callable[P1, R]], Callable[Concatenate[T1, P1], R]]:
    ...


@overload
def hint_add_params(add_types: Type[T1], offset: Literal[1]) -> Callable[[Callable[Concatenate[T2, P1], R]], Callable[Concatenate[T2, T1, P1], R]]:
    ...


@overload
def hint_add_params(add_types: Type[T1], offset: Literal[2]) -> Callable[[Callable[Concatenate[T2, T3, P1], R]], Callable[Concatenate[T2, T3, T1, P1], R]]:
    ...


@overload
def hint_add_params(add_types: Type[T1], offset: Literal[3]) -> Callable[[Callable[Concatenate[T2, T3, T4, P1], R]], Callable[Concatenate[T2, T3, T4, T1, P1], R]]:
    ...


@overload
def hint_add_params(add_types: tuple[Type[T1]]) -> Callable[[Callable[P1, R]], Callable[Concatenate[T1, P1], R]]:
    ...


@overload
def hint_add_params(add_types: tuple[Type[T1], Type[T2]]) -> Callable[[Callable[P1, R]], Callable[Concatenate[T1, T2, P1], R]]:
    ...


@overload
def hint_add_params(add_types: tuple[Type[T1], Type[T2], Type[T3]]) -> Callable[[Callable[P1, R]], Callable[Concatenate[T1, T2, T3, P1], R]]:
    ...


@overload
def hint_add_params(add_types: tuple[Type[T1], Type[T2], Type[T3], Type[T4]]) -> Callable[[Callable[P1, R]], Callable[Concatenate[T1, T2, T3, T4, P1], R]]:
    ...


def hint_add_params(add_types: Any, offset: Optional[Literal[0, 1, 2, 3]] = None) -> Any:
    '''
    Adds new types to the paramspec, beginning at `offset` (default 0)
    '''
    return donothing


def hint_return_type(ret_type: Type[R]) -> Callable[[Callable[P1, Any]], Callable[P1, R]]:
    '''
    Sets the return type of this function to ret_type. Note that this does not
    affect the runtime type annotation.
    '''
    return donothing


def hint_function_type(fn: Callable[P1, R]) -> Callable[[Callable[..., Any]], Callable[P1, R]]:
    return donothing


mongoengine_field_specifiers = (
    fields.StringField,
    fields.URLField,
    fields.EmailField,
    fields.IntField,
    fields.LongField,
    fields.FloatField,
    fields.DecimalField,
    fields.BooleanField,
    fields.DateTimeField,
    fields.DateField,
    fields.ComplexDateTimeField,
    fields.EmbeddedDocumentField,
    fields.ObjectIdField,
    fields.GenericEmbeddedDocumentField,
    fields.DynamicField,
    fields.ListField,
    fields.SortedListField,
    fields.EmbeddedDocumentListField,
    fields.DictField,
    fields.MapField,
    fields.ReferenceField,
    fields.CachedReferenceField,
    fields.LazyReferenceField,
    fields.GenericLazyReferenceField,
    fields.GenericReferenceField,
    fields.BinaryField,
    fields.FileField,
    fields.ImageField,
    fields.GeoPointField,
    fields.PointField,
    fields.LineStringField,
    fields.PolygonField,
    fields.SequenceField,
    fields.UUIDField,
    fields.EnumField,
    fields.MultiPointField,
    fields.MultiLineStringField,
    fields.MultiPolygonField,
    fields.GeoJsonBaseField,
    fields.Decimal128Field
)


@dataclass_transform(field_specifiers=mongoengine_field_specifiers, kw_only_default=True)
def hint_mongo_constructor(fn: Any):
    return fn


TU = TypeVar('TU')


def get_type_tuple_from_union(a: TU) -> tuple[type[TU], ...]:
    if get_origin(a) in (UnionType, Union):
        return get_args(a)
    else:
        return (a,)  # type: ignore # This is a lie, but it's a useful lie
