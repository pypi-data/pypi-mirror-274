from result import Err, Ok


from typing import Iterable, Tuple, TypeVar

# This will need untangling.
from lastmile_eval.rag.debugger.common import core as core


# TODO (@jll) move this out to core_utils

T = TypeVar("T")


def res_reduce_list_separate(
    lst: Iterable[core.Res[T]],
) -> Tuple[list[T], list[Exception]]:
    oks: list[T] = []
    errs: list[Exception] = []
    for item in lst:
        match item:
            case Ok(x):
                oks.append(x)
            case Err(e):
                errs.append(e)

    return oks, errs


def res_reduce_list_all_ok(lst: Iterable[core.Res[T]]) -> core.Res[list[T]]:
    oks, errs = res_reduce_list_separate(lst)
    if errs:
        return Err(ValueError("\n".join(map(str, errs))))
    else:
        return Ok(oks)
