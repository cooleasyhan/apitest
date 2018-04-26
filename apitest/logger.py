# encoding: utf-8

import logging
import sys

logger = logging.getLogger('apitest')




def setup_logger(log_level):
    level = getattr(logging, log_level.upper(), None)
    if not level:
        color_print("Invalid log level: %s" % log_level, "RED")
        sys.exit(1)

    # hide traceback when log level is INFO/WARNING/ERROR/CRITICAL
    if level >= logging.INFO:
        sys.tracebacklimit = 0

    formatter = logging.Formatter(
        '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
        datefmt='%Y-%m-%d %A %H:%M:%S',
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)


log_debug = logger.debug
log_info = logger.info
log_warning = logger.warning
log_error = logger.error
log_critical = logger.critical
