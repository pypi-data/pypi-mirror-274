from gc import collect
from re import match
from time import sleep, time

import pytest
from py_mini_racer import LibAlreadyInitializedError, MiniRacer, init_mini_racer
from py_mini_racer._context import context_count


def test_init():
    init_mini_racer(ignore_duplicate_init=True)

    with pytest.raises(LibAlreadyInitializedError):
        init_mini_racer()

    init_mini_racer(ignore_duplicate_init=True)


# Unfortunately while init_mini_racer allows changing V8 flags, it's hard to test
# automatically because only the first use of V8 can set flags. We'd need to
# restart Python between tests.
# Here's a manual test:
# def test_init_flags():
#     from py_mini_racer import DEFAULT_V8_FLAGS, MiniRacer, init_mini_racer
#     init_mini_racer(flags=(*DEFAULT_V8_FLAGS, '--no-use-strict'))
#     mr = MiniRacer()
#     # this would normally fail in strict JS mode because foo is not declared:
#     mr.eval('foo = 4')


def test_version():
    mr = MiniRacer()
    assert match(r"^\d+\.\d+\.\d+\.\d+$", mr.v8_version) is not None


def test_sandbox():
    mr = MiniRacer()
    assert mr._ctx.v8_is_using_sandbox()  # noqa: SLF001


def test_del():
    collect()
    count_before = context_count()
    mr = MiniRacer()
    del mr

    start = time()
    while time() - start < 2 and context_count() != count_before:
        collect()
        sleep(0.1)

    assert context_count() == count_before
