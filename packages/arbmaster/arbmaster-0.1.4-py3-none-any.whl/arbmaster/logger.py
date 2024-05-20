import sys
import logging
import colorlog

logger = colorlog.getLogger(__name__)

logger.setLevel(logging.INFO)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'INFO': 'green',
        'WARNING': 'orange',
        'ERROR': 'red',
    },
    secondary_log_colors={},
    style='%'
)

stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setFormatter(formatter)

logger.addHandler(stdout)
