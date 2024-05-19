from typing import *
import abc

from oj.constants import *


__all__ = [
    'ValidationError',
    'AbstractValidator',
    'RangeValidator',
    'TimeComplexityValidator',
    'IntCoverageValidator',
]


T = TypeVar('T')


class ValidationError(Exception):
    pass


class AbstraceValidator(Generic[T], abc.ABC):
    def __init__(self, raise_exception = False) -> None:
        super().__init__()
        self._raise_exception = raise_exception

    @abc.abstractmethod
    def __validator__(self, obj: T) -> bool:
        ...

    def validate(self, *objs: Tuple[T], method: Callable[[Iterable[T]], bool]=all) -> bool:
        is_validated = method(map(self.__validator__, objs))
        if is_validated or not self._raise_exception:
            return is_validated
        raise ValidationError(f'{objs} did not passed the validation.')

    def validate_all(self, iterable: Iterable[T]) -> bool:
        return self.validate(*iterable, method=all)

    def validate_any(self, iterable: Iterable[T]) -> bool:
        return self.validate(*iterable, method=any)


class RangeValidator(Generic[T], AbstraceValidator[T]):
    def __init__(self, lo: T = None, hi: T = None, raise_exception = False) -> None:
        """특정 범위에 있는지를 검사한다.

        lo 이상 hi 이하의 범위에 있지 않다면 예외를 발생시킨다.
        """
        super().__init__(raise_exception=raise_exception)
        self.lo = lo
        self.hi = hi

    def __validator__(self, obj: T) -> bool:
        if (self.lo is not None) and (self.lo > obj):
            return False
        if (self.hi is not None) and (self.hi < obj):
            return False
        return True


class TimeComplexityValidator(RangeValidator[float]):
    def __init__(self, seconds: float, T_per_second: float = 5e8, raise_exception = False) -> None:
        super().__init__(hi=T_per_second * seconds, raise_exception=raise_exception)


class IntCoverageValidator(RangeValidator[float]):
    def __init__(self,
                 allow_int32=False,
                 allow_uint32=False,
                 allow_int64=False,
                 allow_uint64=False,
                 allow_natural=False,
                 raise_exception=False) -> None:
        if not any([allow_int32, allow_uint32, allow_int64, allow_uint64]):
            raise ValueError("적어도 하나 이상의 자료형은 허용해야 합니다.")
        lo = []
        hi = []
        if allow_int32:
            lo.append(INT32_MIN_VALUE)
            hi.append(INT32_MAX_VALUE)
        if allow_uint32:
            lo.append(UINT32_MIN_VALUE)
            hi.append(UINT32_MAX_VALUE)
        if allow_int64:
            lo.append(INT64_MIN_VALUE)
            hi.append(INT64_MAX_VALUE)
        if allow_uint64:
            lo.append(UINT64_MIN_VALUE)
            hi.append(UINT64_MAX_VALUE)
        if allow_natural:
            lo.append(1)
        super().__init__(lo=min(lo, default=None),
                         hi=max(hi, default=None),
                         raise_exception=raise_exception)
