# Python Version: 3.x
import logging
logger = logging.getLogger(__name__)

def setLevel(lvl):
    logger.setLevel(lvl)
def addHandler(handler):
    logger.addHandler(handler)
def removeHandler(handler):
    logger.removeHandler(handler)

import colorama
from colorama import Fore, Back, Style
colorama.init()
# thanks to https://github.com/Gallopsled/pwntools/pwnlib/log.py
prefix = {
    'status'       : '[' + Fore.MAGENTA +                'x'        + Style.RESET_ALL + '] ',
    'success'      : '[' + Fore.GREEN   + Style.BRIGHT + '+'        + Style.RESET_ALL + '] ',
    'failure'      : '[' + Fore.RED     + Style.BRIGHT + '-'        + Style.RESET_ALL + '] ',
    'debug'        : '[' + Fore.RED     + Style.BRIGHT + 'DEBUG'    + Style.RESET_ALL + '] ',
    'info'         : '[' + Fore.BLUE    + Style.BRIGHT + '*'        + Style.RESET_ALL + '] ',
    'warning'      : '[' + Fore.YELLOW  + Style.BRIGHT + '!'        + Style.RESET_ALL + '] ',
    'error'        : '[' + Fore.RED     +                'ERROR'    + Style.RESET_ALL + '] ',
    'exception'    : '[' + Fore.RED     +                'ERROR'    + Style.RESET_ALL + '] ',
    'critical'     : '[' + Fore.RED     +                'CRITICAL' + Style.RESET_ALL + '] ',
}

def emit(s: str, *args) -> None:
    # logger.info(str(s), *args)
    pass
def status(s: str, *args) -> None:
    # logger.info(prefix['status'] + str(s), *args)
    pass
def success(s: str, *args) -> None:
    # logger.info(prefix['success'] + str(s), *args)
    pass
def failure(s: str, *args) -> None:
    # logger.info(prefix['failure'] + str(s), *args)
    pass
def debug(s: str, *args) -> None:
    # logger.debug(prefix['debug'] + str(s), *args)
    pass
def info(s: str, *args) -> None:
    # logger.info(prefix['info'] + str(s), *args)
    pass
def warning(s: str, *args) -> None:
    # logger.warning(prefix['warning'] + str(s), *args)
    pass
def error(s: str, *args) -> None:
    # logger.error(prefix['error'] + str(s), *args)
    pass
def exception(s: str, *args) -> None:
    # logger.error(prefix['exception'] + str(s), *args)
    pass
def critical(s: str, *args) -> None:
    # logger.critical(prefix['critical'] + str(s), *args)
    pass

# 高速化用
def faster_emit(s: str, *args) -> None:
    logger.info(str(s), *args)
def faster_status(s: str, *args) -> None:
    logger.info(prefix['status'] + str(s), *args)
def faster_success(s: str, *args) -> None:
    logger.info(prefix['success'] + str(s), *args)
def faster_failure(s: str, *args) -> None:
    logger.info(prefix['failure'] + str(s), *args)
def faster_debug(s: str, *args) -> None:
    logger.debug(prefix['debug'] + str(s), *args)
def faster_info(s: str, *args) -> None:
    logger.info(prefix['info'] + str(s), *args)
def faster_warning(s: str, *args) -> None:
    logger.warning(prefix['warning'] + str(s), *args)
def faster_error(s: str, *args) -> None:
    logger.error(prefix['error'] + str(s), *args)
def faster_exception(s: str, *args) -> None:
    logger.error(prefix['exception'] + str(s), *args)
def faster_critical(s: str, *args) -> None:
    logger.critical(prefix['critical'] + str(s), *args)

bold = lambda s: colorama.Style.BRIGHT + s + colorama.Style.RESET_ALL
green = lambda s: colorama.Fore.GREEN + s + colorama.Fore.RESET
red = lambda s: colorama.Fore.RED + s + colorama.Fore.RESET
