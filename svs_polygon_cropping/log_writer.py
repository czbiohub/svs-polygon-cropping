import logging
from datetime import datetime

from napari.utils.notifications import (
    Notification,
    notification_manager,
    show_info,
)

FORMAT = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
formatter = logging.Formatter(FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create file handler which logs even info messages
now = datetime.now()
date_time = now.strftime("%m_%d_%Y_%H_%M_%S")

log_handlers = [
    logging.FileHandler('svs_crops_{}.log'.format(date_time), 'w'),
    logging.StreamHandler(),
]

for handler in log_handlers:
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def notify(message):
    with notification_manager:
        # save all of the events that get emitted
        store: [Notification] = []  # noqa
        _append = lambda e: store.append(e)  # lambda needed on py3.6  # noqa
        notification_manager.notification_ready.connect(_append)
        show_info(message)
    logger.info(message)
