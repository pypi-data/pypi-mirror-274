#
# File:    ./src/vutils/testing/mock.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-13 17:04:14 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Mocking utilities."""

import unittest.mock
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable
    from unittest.mock import Mock

    from vutils.testing import (
        KwArgsType,
        MockableType,
        PatchType,
        ReturnsType,
        SetupFuncType,
        make_patch,
    )
else:
    make_patch = unittest.mock.patch


def make_mock(*args: object, **kwargs: object) -> "Mock":
    """
    Make the :class:`unittest.mock.Mock` object.

    :param args: Positional arguments to be passed to the
        :class:`unittest.mock.Mock` constructor
    :param kwargs: Key-value arguments to be passed to the
        :class:`unittest.mock.Mock` constructor
    :return: the :class:`unittest.mock.Mock` object
    """
    return unittest.mock.Mock(*args, **kwargs)


def make_callable(returns: "ReturnsType" = None) -> "Mock":
    """
    Make the :class:`unittest.mock.Mock` object that serves as a callable.

    :param returns: If callable, :arg:`returns` is treated as the
        :arg:`side_effect:unittest.mock.Mock` parameter to
        :class:`unittest.mock.Mock`. Otherwise, it is treated as
        the :arg:`return_value:unittest.mock.Mock` parameter
    :return: the :class:`unittest.mock.Mock` object representing the callable
    """
    if callable(returns):
        return unittest.mock.Mock(side_effect=returns)
    return unittest.mock.Mock(return_value=returns)


class PatchSpec:
    """Holds the patch specification."""

    #: The target to be patched
    __target: object
    #: The setup function for the patch
    __setupfunc: "SetupFuncType"
    #: Key-value arguments passed to :func:`unittest.mock.patch`
    __kwargs: "KwArgsType"

    __slots__ = ("__target", "__setupfunc", "__kwargs")

    def __init__(
        self, target: object, setupfunc: "SetupFuncType", **kwargs: object
    ) -> None:
        """
        Initialize the patch specification.

        :param target: The target to be patched
        :param setupfunc: The function used to setup the patch
        :param kwargs: Additional key-value arguments passed to
            :func:`unittest.mock.patch`
        """
        self.__target = target
        self.__setupfunc = setupfunc
        self.__kwargs = kwargs

    def __call__(self) -> "PatchType":
        """
        Create the patcher from the specification.

        :return: the patcher

        The patcher is created in four steps:

        #. :class:`unittest.mock.Mock` object is created
        #. if *new* is in :arg:`kwargs:.PatchSpec.__init__`, the mock object
           becomes *new*
        #. if :arg:`setupfunc:.PatchSpec.__init__` is not :obj:`None`, the mock
           object is passed to it; the :arg:`setupfunc:.PatchSpec.__init__` can
           then adjust the object
        #. the patcher is created by calling :func:`unittest.mock.patch` with
           :arg:`target:.PatchSpec.__init__`, the mock object, and additional
           arguments given by :arg:`kwargs:.PatchSpec.__init__`, respectively
        """
        kwargs: "KwArgsType" = self.__kwargs.copy()
        mock: "MockableType" = kwargs.pop("new", make_mock())
        if self.__setupfunc is not None:
            self.__setupfunc(mock)
        return make_patch(self.__target, mock, **kwargs)


class PatchingContextManager:
    """Context manager that handles the patching."""

    #: The list of patchers
    __patchers: "list[PatchType]"

    __slots__ = ("__patchers",)

    def __init__(self, patchers: "Iterable[PatchType]") -> None:
        """
        Initialize the context manager.

        :param patchers: The list of patchers
        """
        self.__patchers = list(patchers)

    def __enter__(self) -> "PatchingContextManager":
        """
        Apply patches.

        :return: the instance that receives this method call (a.k.a *self*)
        """
        for patcher in self.__patchers:
            patcher.start()
        return self

    def __exit__(self, *args: object) -> None:
        """
        Revert applied patches in reverse order.

        :param args: Unused positional arguments
        """
        for patcher in reversed(self.__patchers):
            patcher.stop()


class PatcherFactory:
    r"""
    Factory for creating patchers.

    This factory allows to create and apply the set of patches simultaneously,
    omitting the nested ``with`` statements for every patch. In the following
    example, it is demonstrated how this class can be used to test the sending
    colored text to the standard output. First, define the factory that patch
    the :mod:`colorama` and :mod:`sys` modules::

        import colorama
        import io
        import sys


        class MyPatcher(PatcherFactory):

            def setup_sys(self, mock):
                self.stream = io.StringIO()
                mock.stdout = self.stream

            @staticmethod
            def setup_colorama(mock):
                mock.Fore.RESET = "</c>"
                mock.Fore.RED = "<c:red>"

            def setup(self):
                self.add_spec("__main__.colorama", self.setup_colorama)
                self.add_spec("__main__.sys", self.setup_sys)

    Next, use the factory in the test::

        def echo_red(text):
            sys.stdout.write(
                f"{colorama.Fore.RED}{text}{colorama.Fore.RESET}\n"
            )


        def test_echo_red():
            patcher = MyPatcher()
            message = "Alert!"

            with patcher.patch():
                echo_red(message)

            assert patcher.stream.getvalue() == f"<c:red>{message}</c>\n"

    The patches are applied in order as their specifications were added by
    :meth:`~.PatcherFactory.add_spec`.
    """

    #: The list of patch specifications
    __specs: "list[PatchSpec]"

    __slots__ = ("__specs",)

    def __init__(self) -> None:
        """Initialize the factory."""
        self.__specs = []
        self.setup()

    def add_spec(
        self,
        target: object,
        setupfunc: "SetupFuncType" = None,
        **kwargs: object,
    ) -> "PatcherFactory":
        """
        Add the patch specification to the factory.

        :param target: The target to be patched
        :param setupfunc: The function used to setup the patch, see
            :class:`.PatchSpec`
        :param kwargs: Additional key-value arguments to
            :func:`unittest.mock.patch`
        :return: the instance that receives this method call (a.k.a *self*)
        """
        self.__specs.append(PatchSpec(target, setupfunc, **kwargs))
        return self

    def setup(self) -> None:
        """Set up the factory."""

    def patch(self) -> PatchingContextManager:
        """
        Create the context manager that perform the patching.

        :return: the context manager used for patching
        """
        return PatchingContextManager([spec() for spec in self.__specs])
