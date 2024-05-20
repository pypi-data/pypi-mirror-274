import logging
import os
from os.path import isfile, join

from gadapt.utils.TimeStampFormatter import TimestampFormatter


def init_logging(is_logging: bool):
    """
    Initializes logging for genetic algorithm
    """

    def get_last_num(s: str) -> int:
        try:
            if not s.startswith("gadapt_log.log"):
                return -1
            if s == "gadapt_log.log":
                return 0
            s_last_number = s.rsplit(".", 1)[-1]
            n_last_number = int(s_last_number)
            s.rsplit(".", 1)[-1]
            return n_last_number
        except Exception:
            return -1

    path = os.path.join(os.getcwd(), "log")
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        onlyfiles = [f for f in os.listdir(path) if isfile(join(path, f))]
        onlyfiles.sort(reverse=True, key=get_last_num)
        for f in onlyfiles:
            if f == "gadapt_log.log":
                try:
                    os.rename(
                        os.path.join(path, f), os.path.join(path, "gadapt_log.log.1")
                    )
                except Exception:
                    print("Unable to rename log file: " + os.path.join(path, f))
                    break
            elif f.startswith("gadapt_log.log."):
                n_last_number = get_last_num(f)
                if n_last_number == -1:
                    continue
                n_last_number += 1
                try:
                    os.rename(
                        os.path.join(path, f),
                        os.path.join(path, "gadapt_log.log." + str(n_last_number)),
                    )
                except Exception:
                    break
    logpath = os.path.join(path, "gadapt_log.log")
    logger = logging.getLogger("gadapt_logger")
    handler = logging.FileHandler(logpath)
    handler.setFormatter(
        TimestampFormatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    for h in logger.handlers:
        logger.removeHandler(h)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    if not is_logging:
        logger.disabled = True
    else:
        logger.disabled = False


def gadapt_log_info(msg: str):
    logger = logging.getLogger("gadapt_logger")
    logger.info(msg)
