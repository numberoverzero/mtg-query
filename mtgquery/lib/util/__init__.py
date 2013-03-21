##mtgquery.lib.util
import logging

__log = logging.getLogger(__name__)


def DEBUG(string):
    __log.debug(string)


def INFO(string):
    __log.info(string)


def WARN(string):
    __log.warn(string)


def ERROR(string):
    __log.error(string)


def CRITICAL(string):
    __log.critical(string)
