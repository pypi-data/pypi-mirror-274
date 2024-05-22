import logging
import os
import re
import sys
from logging import Formatter as BaseFormatter
from logging.handlers import TimedRotatingFileHandler
from os import PathLike
from pathlib import Path
from typing import TextIO, Callable, Optional, Literal

from colorlog import ColoredFormatter as CF

from my_tools.color import Color
from my_tools.decorators import singleton

default_level_colors = {
    "TRACE": "cyan",
    "DEBUG": "blue",
    "SUCCESS": "light_green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

default_secondary_log_colors = {
    "levelname": "level",
    "message": "level",
    "asctime": 'green',
    "name": 'purple',
    "module": 'cyan',
    "funcName": 'cyan',
    "lineno": 'cyan',
}


class ColoredFormatter(CF):

    def __init__(
            self,
            fmt: Optional[str] = None,
            datefmt: Optional[str] = None,
            log_colors: Optional[dict] = None,
            reset: bool = True,
            secondary_log_colors: Optional[dict] = None,
            level_colors: Optional[dict] = None,
            style='{',
    ) -> None:
        level_colors = level_colors or default_level_colors
        secondary_log_colors = secondary_log_colors or default_secondary_log_colors
        secondary_log_colors = {
            k: ({lv: v for lv in logging._nameToLevel} if v != 'level' else level_colors)  # noqa
            for k, v in secondary_log_colors.items()
        }

        for k in secondary_log_colors.keys():
            if style == '{':
                fmt = re.sub(rf'({{{k}.*?}})', rf'{{{k}_log_color}}\1{{reset}}', fmt)
            elif style == '%':
                fmt = re.sub(rf'(%\({k}.*?\)s)', rf'%({k}_log_color)s\1%(reset)s', fmt)
            elif style == '$':
                fmt = re.sub(rf'(\${{{k}.*?}})', rf'${{{k}_log_color}}\1${{reset}}', fmt)
            else:
                raise ValueError('style only support \'{\' or \'%\' or \'$\'')
        super().__init__(
            fmt=fmt,
            datefmt=datefmt,
            style=style,
            log_colors=log_colors,
            reset=reset,
            secondary_log_colors=secondary_log_colors,
        )

    def format(self, record):
        if record.exc_info:

            if not record.exc_text:
                record.exc_text = Color.thin_red(self.formatException(record.exc_info))
            elif isinstance(record.exc_text, str) and not record.exc_text.startswith('\033['):
                record.exc_text = Color.thin_red(record.exc_text)
        return super().format(record)


class Formatter(BaseFormatter):

    def format(self, record):
        return re.sub(r'\033\[.+?m', '', super().format(record))


ColoredFormatter.default_msec_format = '%s.%03d'
Formatter.default_msec_format = '%s.%03d'
BaseFormatter.default_msec_format = '%s.%03d'

TRACE = 5
SUCCESS = 25
logging.addLevelName(TRACE, "TRACE")
logging.addLevelName(SUCCESS, "SUCCESS")
default_fmt = '{asctime} | {levelname:<8} | {name} | {module}:{funcName}:{lineno} - {message}'
default_console_format = ColoredFormatter(default_fmt)
default_file_format = Formatter(default_fmt, style='{')
default_format = BaseFormatter(default_fmt, style='{')


@singleton('name')
class ManagerLogger(logging.Logger):

    def catch_exception(self, func: Callable):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.exception(f'{func.__name__}执行错误：[{e.__class__.__name__}]{e}', stacklevel=2)

        return inner

    def _add_console_handler(self, stream=None, level=None, formatter: str | Formatter = None,
                             filters: Callable | list[Callable] = None):
        if stream is None:
            stream = sys.stdout
        handler = logging.StreamHandler(stream)
        if not formatter:
            formatter = default_console_format
        if isinstance(formatter, str):
            formatter = Formatter(formatter)
        handler.setFormatter(formatter)
        handler.setLevel(level)
        if filters is not None:
            if isinstance(filters, Callable):
                filters = [filters]
            for f in filters:
                handler.addFilter(f)
        self.addHandler(handler)

    def _add_file_handler(self, path: str | PathLike, level=None, formatter: str | Formatter = None,
                          filters: Callable | list[Callable] = None):
        handler = TimedRotatingFileHandler(
            path,
            when="midnight",
            backupCount=10,
            encoding="utf-8",
            delay=True,
        )
        handler.setLevel(level)
        if not formatter:
            formatter = default_file_format
        if isinstance(formatter, str):
            formatter = Formatter(formatter)
        handler.setFormatter(formatter)
        if filters is not None:
            if isinstance(filters, Callable):
                filters = [filters]
            for f in filters:
                handler.addFilter(f)
        self.addHandler(handler)

    def remove(self, handler=None):
        if handler:
            return self.removeHandler(handler)
        while self.handlers:
            self.handlers.pop()

    def add(self, sink: TextIO | str | PathLike, *, level: int | str = "DEBUG", formatter=None, filters=None):
        if sink == sys.stdout or sink == sys.stderr:
            return self._add_console_handler(sink, level=level, filters=filters, formatter=formatter)
        return self._add_file_handler(sink, level=level, filters=filters, formatter=formatter)

    def success(self, msg, *args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        return self._log(
            SUCCESS, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel + 1
        )

    def trace(self, msg, *args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        return self._log(
            TRACE, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel + 1
        )


getLogger_raw = logging.getLogger


def _get_loger(name):
    __logger = getLogger_raw(name)
    __logger_new = ManagerLogger(__logger.name, __logger.level)
    __logger_new.handlers = __logger.handlers
    __logger_new.filters = __logger.filters
    return __logger_new


logging.getLogger = _get_loger


class LogManager:

    def __init__(
            self, __name, *,
            console_level: int | str = "DEBUG",
            file_path: str = None,
            file_level: int | str | None = "DEBUG",
            error_level: int | str | None = "ERROR",
            fmt: str = default_fmt,
            colorize: bool = True,
    ) -> None:
        logging.root.setLevel(logging.NOTSET)
        self._file_path = self._init_log_file_path(file_path)
        if not self._file_path.exists():
            os.mkdir(self._file_path)
        self.console_level = console_level
        self.file_level = file_level
        self.error_level = error_level
        self._logger: ManagerLogger = _get_loger(__name)
        self.fmt = fmt
        self.colorize = colorize

    @staticmethod
    def _init_log_file_path(file_path: str | PathLike = None) -> Path:
        if file_path:
            return Path(file_path)
        if "PYTHONPATH" in os.environ and os.path.exists(os.environ['PYTHONPATH']):
            return Path(os.environ['PYTHONPATH']) / 'logs'
        return Path('/pythonlogs')

    @staticmethod
    def _guess_fmt_style(fmt: str) -> Literal['{', '%', '$']:
        for i in fmt:
            if i == '{':
                return '{'
            if i == '%':
                return '%'
            if i == '$':
                return '$'
        return '{'

    def get_logger(self, reset=False) -> ManagerLogger:
        if reset:
            self._logger.remove()
        if not self._logger.handlers:
            style = self._guess_fmt_style(self.fmt)
            file_format = Formatter(self.fmt, style=style)
            if not self.colorize:
                console_format = BaseFormatter(fmt=self.fmt, style=style)
            else:
                console_format = ColoredFormatter(fmt=self.fmt, style=style)
            self._logger.add(sys.stdout, level=self.console_level, formatter=console_format)
            if self.file_level:
                self._logger.add(self._file_path / 'out.log', level=self.file_level, formatter=file_format)
            if self.error_level:
                self._logger.add(self._file_path / 'error.log', level=self.error_level, formatter=file_format)
        return self._logger


if __name__ == '__main__':
    logger = LogManager(__name__, console_level=TRACE, file_path='./../logs').get_logger()

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
    logger.success('success!')
    logger.trace('trace message')
    logger.info(f'My Name is {Color.red("John")}, Yes!')


    @logger.catch_exception
    def func(a, b):
        return a / b


    r = func(1, 0)
    print('Hello World!')
