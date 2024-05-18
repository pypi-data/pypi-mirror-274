#
# File:    ./src/vutils/testing/utils.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-14 17:12:48 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Miscellaneous utilities."""

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from unittest import TestCase

    from vutils.testing import (
        ArgsType,
        BasesType,
        ExcSpecType,
        FuncType,
        KwArgsType,
        MembersType,
        TypeType,
    )


def make_type(
    name: str,
    bases: "BasesType" = None,
    members: "MembersType" = None,
    **kwargs: object,
) -> type:
    """
    Make a new type.

    :param name: The type name
    :param bases: The type's bases
    :param members: The definition of type's members and methods
    :param kwargs: Additional key-value arguments passed to :class:`type`
    :return: the new type

    This function becomes handy when creating types used as test data. For
    instance, instead of ::

        class ErrorA(Exception):
            pass

        class ErrorB(Exception):
            pass

        class MyTestCase(TestCase):

            def setUp(self):
                self.error_a = ErrorA
                self.error_b = ErrorB

    it is possible to write::

        class MyTestCase(TestCase):

            def setUp(self):
                self.error_a = make_type("ErrorA", Exception)
                self.error_b = make_type("ErrorB", Exception)

    This helps to keep test data in the proper scope and to reduce the size of
    the code base.
    """
    if bases is None:
        bases = ()
    if not isinstance(bases, tuple):
        bases = (bases,)
    if members is None:
        members = {}
    return type(name, bases, members, **kwargs)


class LazyInstanceMethod:
    """Lazy instance method."""

    #: The lazy instance proxy
    __owner: "LazyInstanceProxy"
    #: The method name
    __name: str

    __slots__ = ("__owner", "__name")

    def __init__(self, owner: "LazyInstanceProxy", name: str) -> None:
        """
        Initialize the method wrapper.

        :param owner: The owner of the lazy instance method
        :param name: The name of the method
        """
        self.__owner = owner
        self.__name = name

    def __call__(self, *args: object, **kwargs: object) -> object:
        """
        Delegate the call to the proper method of the instance.

        :param args: Positional arguments passed to the method
        :param kwargs: Key-value arguments passed to the method
        :return: the value returned by the method
        """
        inst: object = self.__owner.get_instance()
        return cast("FuncType", getattr(inst, self.__name))(*args, **kwargs)


class LazyInstanceProxy:
    """Lazy instance proxy."""

    #: The lazy instance
    __owner: "LazyInstance"
    #: Positional arguments passed to the instance constructor
    __args: "ArgsType"
    #: Key-value arguments passed to the instance constructor
    __kwargs: "KwArgsType"

    __slots__ = ("__owner", "__args", "__kwargs")

    def __init__(
        self,
        owner: "LazyInstance",
        args: "ArgsType",
        kwargs: "KwArgsType",
    ) -> None:
        """
        Initialize the proxy.

        :param owner: The owner of the proxy
        :param args: Positional arguments to be passed to the constructor
            during the initialization of the instance
        :param kwargs: Key-value arguments to be passed to the constructor
            during the initialization of the instance
        """
        self.__owner = owner
        self.__args = args
        self.__kwargs = kwargs

    def get_instance(self) -> object:
        """
        Get the instance via proxy.

        :return: the initialized or cached instance
        """
        return self.__owner.get_instance(self, self.__args, self.__kwargs)

    def __getattr__(self, name: str) -> "LazyInstanceMethod | object":
        """
        Get the value of the :arg:`name` member of the instance.

        :param name: The name of the member
        :return: the value of the member

        If the value of :arg:`name` is callable, wrap it inside
        :class:`.LazyInstanceMethod`.
        """
        if self.__owner.has_method(name):
            return LazyInstanceMethod(self, name)
        inst: object = self.get_instance()
        return cast(object, getattr(inst, name))


class LazyInstance:
    r"""
    Support lazy initialization.

    Object is constructed/initialized at time when its member function is
    called. Example::

        foo_factory = LazyInstance(Foo, initialize_once=False)
        foo = foo_factory.create(1, bar=2)
        test(foo.quux)

    when ``test`` calls ``foo.quux``, ``Foo(1, bar=2)`` is invoked first
    to make the instance of ``Foo`` and to cache the instance inside
    ``foo_factory``. Then, from this instance, ``quux`` is invoked. Since
    ``foo_factory`` was created with :attr:`~.LazyInstance.__initialize_once`
    property set to :obj:`False`, ``foo`` is initialized every time when
    ``foo.quux`` is invoked.

    The story behind :class:`.LazyInstance`: consider the following snippet of
    code::

        class Foo:
            def __init__(self):
                self.stream = sys.stderr

            def greet(self):
                self.stream.write("Hello!\n")


        def test(func, mystream):
            # Replace sys.stderr for mystream:
            with SysStderrPatcher(mystream).patch():
                func()

    in this scenario::

        mystream = io.StringIO()
        foo = Foo()
        test(foo.greet, mystream)

    ``Hello!\n`` will be send to :obj:`sys.stderr` since the patching has been
    done too late. This is where :class:`.LazyInstance` comes to help us::

        mystream = io.StringIO()
        foo_factory = LazyInstance(Foo)
        foo = foo_factory.create()
        test(foo.greet, mystream)

    now, ``Hello!\n`` is written to ``mystream`` as expected.
    """

    #: The lazy instance proxy to the instance mapping
    __cache: "dict[LazyInstanceProxy, object]"
    #: The class of the instance
    __klass: "TypeType"
    #: When :obj:`False`, :meth:`~.LazyInstance.get_instance` creates a new
    #: instance every time when called
    __initialize_once: bool

    __slots__ = ("__cache", "__klass", "__initialize_once")

    def __init__(
        self, klass: "TypeType", initialize_once: bool = False
    ) -> None:
        """
        Initialize the lazy instance.

        :param klass: The class from which instance is created
        :param initialize_once: The flag saying that instance should be created
            and initialized only once
        """
        self.__cache = {}
        self.__klass = klass
        self.__initialize_once = initialize_once

    def get_instance(
        self,
        proxy: "LazyInstanceProxy",
        args: "ArgsType",
        kwargs: "KwArgsType",
    ) -> object:
        """
        Get the instance.

        :param proxy: The lazy instance proxy
        :param args: Positional arguments passed to the constructor during the
            initialization of the instance
        :param kwargs: Key-value arguments passed to the constructor during the
            initialization of the instance
        :return: the initialized or cached instance

        If the instance is not created or initialized or if it is to be needed
        reinitialized, do it. :arg:`args` and :arg:`kwargs` are passed to the
        constructor.
        """
        if proxy not in self.__cache or not self.__initialize_once:
            self.__cache[proxy] = self.__klass(*args, **kwargs)
        return self.__cache[proxy]

    def has_method(self, name: str) -> bool:
        """
        Test whether the class has method :arg:`name`.

        :param name: The name of the method
        :return: :obj:`True` if the class has the method called :arg:`name`
        """
        return callable(cast(object, getattr(self.__klass, name, None)))

    def create(self, *args: object, **kwargs: object) -> "LazyInstanceProxy":
        """
        Create the proxy of the lazy instance.

        :param args: Positional arguments passed to the constructor during the
            initialization of the instance
        :param kwargs: Key-value arguments passed to the constructor during the
            initialization of the instance
        :return: the proxy of the lazy instance
        """
        return LazyInstanceProxy(self, args, kwargs)


class AssertRaises:
    """
    Wrapper that asserts that callable raises.

    Consider there are two functions ``func1`` and ``func2`` that are very
    similar to each other except ``func2`` raises an exception. Since their
    similarity, the test case defines a function ``run_and_verify(func)`` which
    runs them and test their results and side-effects. However, since ``func2``
    raises an exception, ``run_and_verify(func2)`` fails. To deal with such a
    situation, :class:`.AssertRaises` can be used::

        class MyTestCase(CommonTestCase):

            def test_funcs(self):
                wfunc2 = AssertRaises(self, func2, FooError)

                # run_and_verify is defined in CommonTestCase
                self.run_and_verify(func1)
                # Does not fail, exception is caught and stored for later use
                self.run_and_verify(wfunc2)
                # Analyze caught exception
                self.assertEqual(wfunc2.get_exception().detail, "foo")
    """

    #: The test case
    __testcase: "TestCase"
    #: The callable object to be tested
    __func: "FuncType"
    #: Expected exceptions
    __raises: "ExcSpecType"
    #: The caught exception
    __exception: "Exception | None"

    __slots__ = ("__testcase", "__func", "__raises", "__exception")

    def __init__(
        self, testcase: "TestCase", func: "FuncType", raises: "ExcSpecType"
    ) -> None:
        """
        Initialize the wrapper.

        :param testcase: The test case
        :param func: The callable object to be tested
        :param raises: Expected exceptions
        """
        self.__testcase = testcase
        self.__func = func
        if not isinstance(raises, tuple):
            raises = (raises,)
        self.__raises = raises
        self.__exception = None

    def get_exception(self) -> "Exception | None":
        """
        Get the caught exception.

        :return: the caught exception object

        When called, the caught exception storage is cleared (the next call
        will return :obj:`None`).
        """
        exc: "Exception | None" = self.__exception
        self.__exception = None
        return exc

    def __call__(self, *args: object, **kwargs: object) -> None:
        """
        Invoke the callable object.

        :param args: Positional arguments
        :param kwargs: Key-value arguments

        Invoke the callable object with :arg:`args` and :arg:`kwargs`, catch
        and store the exception. Fail if the exception is not raised by the
        callable object or if it is not in the list of expected exceptions.
        """
        with self.__testcase.assertRaises(self.__raises) as catcher:
            self.__func(*args, **kwargs)
        self.__exception = catcher.exception
