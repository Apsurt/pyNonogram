# -*- coding: utf-8 -*-


class PathException(Exception):
    """
    Exception that's thrown when the path is invalid
    """
    pass


class NonogramException(Exception):
    """
    Base exception for all nonogram exceptions
    """
    pass


class LoadingException(NonogramException):
    """
    Exception that's thrown when errors occur while loading a nonogram.
    """
    pass


class NotLoaded(NonogramException):
    """
    Exception that's thrown when a nonogram is not loaded.
    """
    pass

class NotSolved(NonogramException):
    """
    Exception that's thrown when a nonogram is not solved.
    """
    pass

class UnknownFormat(Exception):
    """
    Exception thrown when trying to export to a unknown format.
    Supported formats: .non
    """
    pass