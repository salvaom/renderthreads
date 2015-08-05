

"""
renderthreads_logging
==========================================

Module to handle all things related to logging in
the renderthreads package.

------------------------------------------

Members:

#. UniversalPrintObject
    Implements the print_message interface
    used in UniversalStreamHandler.

#. UniversalStreamHandler
    Stream handler subclass that is initialized with
    a UniversalPrintObject that delivers the correct
    print behaviour under the same interface.

...
"""


#  Import
#  ------------------------------------------------------------------
#  python
import sys
import logging
import functools
#  PySide
from PySide import QtGui
from PySide import QtCore


#  Import variable
do_reload = True

#  renderthreads

#  lib

#  renderthreads_globals
import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)


#  Globals
#  ------------------------------------------------------------------
INITIAL_LOGGING_LEVEL = renderthreads_globals.INITIAL_LOGGING_LEVEL


#  Decorators
#  ------------------------------------------------------------------

def execute_with_logger(logger_class):
    """
    Closure logger with argument.
    """

    def execute_with_logger_func_decorator(func):
        """
        Use enclosed logger_class and
        return func object to use.
        """

        def wrapped_func(*args, **kwargs):

            # current_logger_class
            current_logger_class = logging.getLoggerClass()

            # set default logger
            logging.setLoggerClass(logger_class)

            # execute func
            result = func(*args, **kwargs)

            # reset logger
            logging.setLoggerClass(current_logger_class)

            # return
            return result

        return wrapped_func

    return execute_with_logger_func_decorator


#  RenderThreadsLogger
#  ------------------------------------------------------------------
class RenderThreadsLogger(logging.getLoggerClass()):
    """
    Custom logging class RenderThreadsLogger to
    be able to test against type.
    """


#  Functions
#  ------------------------------------------------------------------
def get_formatter(verbose_level=logging.WARNING):
    """
    Return correctly formatted handler for display.
    For ease of use, verbose_level corresponds to
    known logging constants.
    """

    # debug
    if (verbose_level == logging.DEBUG):
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # info
    elif (verbose_level == logging.INFO):
        return logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # warning
    elif (verbose_level == logging.WARNING):
        return logging.Formatter('%(name)s - %(message)s')

    # error
    elif (verbose_level >= logging.ERROR):
        return logging.Formatter('%(message)s')


def get_handler(display=sys.stdout):
    """
    Return correctly formatted handler for display.
    """

    # formatter
    formatter = get_formatter()
    handler = logging.StreamHandler()
    # add formatter
    handler.setFormatter(formatter)

    # return
    return handler


@execute_with_logger(RenderThreadsLogger)
def get_logger(name,
                display=sys.stdout,
                logging_level=INITIAL_LOGGING_LEVEL):
    """
    Return correctly formatted logger from single source.
    """

    # handler
    handler = get_handler(display)

    # logger
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)
    logger.handlers = []
    logger.addHandler(handler)

    # return
    return logger


def set_logging_level(logging_level):
    """
    Set logging level for all instances of
    RenderThreads loggers. (That is all loggers in
    global dict of type RenderThreadsLogger)
    """

    # iterate
    for logger_name, logger in logging.Logger.manager.loggerDict.iteritems():

        # check type (a direct type check fails here, for whatever reason)
        # Instead check against __name__ of type which succeeds
        if (type(logger).__name__ == RenderThreadsLogger.__name__):

            # set level
            logger.setLevel(logging_level)

            # print
            print('Set logger {0} to {1}'.format(logger_name, logging_level))
