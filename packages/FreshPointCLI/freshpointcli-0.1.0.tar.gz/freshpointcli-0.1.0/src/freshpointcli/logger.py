import logging

from logging.handlers import RotatingFileHandler


logger = logging.getLogger('freshpointcli')


def configure_logging(
    log_file: str,
    level: int = logging.DEBUG,
    fmt: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    max_bytes: int = 10**7,
    backup_count: int = 5
) -> None:
    """
    Configure the logging module to only log to a specified file.

    Args:
        log_path (str): Path to the log file.
        max_bytes (int, optional): Maximum size of the log file in bytes.
        When the file exceeds this size, it will be rotated.
        Defaults to 10**7.
        backup_count (int, optional): Number of backup log files to keep.
        Defaults to 5.
    """
    f_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count
        )
    f_formatter = logging.Formatter(fmt)
    f_handler.setFormatter(f_formatter)
    logging.basicConfig(level=level, handlers=[f_handler])
