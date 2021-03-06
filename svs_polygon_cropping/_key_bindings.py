# and other key bindings that already exist from https://github.com/czbiohub/napari-he-annotations/blob/master/napari_he_annotations/_key_bindings.py that will help annotate
import os

import pyvips
import logging
from datetime import datetime

from napari.utils.notifications import (
    Notification,
    notification_manager,
    show_info,
)
from .workerThread import (
    Worker
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create file handler which logs even info messages
now = datetime.now()
date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
fh = logging.FileHandler('svs_crops_{}.log'.format(date_time), 'w')
logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO)
formatter = logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)
TILE_SIZE = 512


def notify(message):
    with notification_manager:
        # save all of the events that get emitted
        store: List[Notification] = []  # noqa
        _append = lambda e: store.append(e)  # lambda needed on py3.6  # noqa
        notification_manager.notification_ready.connect(_append)
        show_info(message)
    logger.info(message)


def crop_tissue(viewer, tissue_name, threadpool):
    layers = viewer.layers
    image_layer = layers["he"]
    dirname = os.path.dirname(image_layer.metadata['path'])

    if "Shapes" not in layers or layers["Shapes"].nshapes < 1:
        notify("Please draw a polygon around a tissue.")
    elif layers["Shapes"].nshapes > 1:
        notify("Only 1 shape is allowed, delete the others")
    elif tissue_name == '':
        notify("Please enter a tissue name to proceed")
    else:
        x = tuple(int(point[1]) for point in layers["Shapes"].data[0])
        y = tuple(int(point[0]) for point in layers["Shapes"].data[0])
        points = tuple([a, b] for a, b in zip(x, y))
        left = min(x)
        top = min(y)
        image = pyvips.Image.new_from_file(image_layer.metadata["path"], access="sequential")
        crop = image.crop(left, top, max(x) - left, max(y) - top)
        svg = f"""
                <svg viewBox="0 0 {crop.width} {crop.height}">
                    <polygon style="fill: white; stroke: none" points="
            """
        svg += " ".join([f"{x - left}, {y - top} " for x, y in points])
        svg += """
                    "/>
                </svg>
            """
        mask = pyvips.Image.svgload_buffer(bytes(svg, "ascii"))[3]
        temp = crop[:3]
        cropped = temp.bandjoin(mask)
        cropped2 = cropped.flatten(background=[244.0, 244.0, 243.0])  # the white color from most slides background

        os.makedirs(os.path.join(dirname, "he_crops"), exist_ok=True)
        notify("Starting cropping tissue: " + tissue_name)

        worker = Worker(
            save_file, cropped2, dirname, image_layer, tissue_name
        )  # Any other args, kwargs are passed to the run function

        worker.signals.result.connect(returned)
        worker.signals.finished.connect(finished)

        # Execute
        threadpool.start(worker)


def finished():
    logger.info("finished")


def returned(tissue_name):
    logger.info("returned " + tissue_name)


def save_file(cropped, dir_name, image_layer, tissue_name):

    # If .tif is the preferred output format
    # cropped.write_to_file(os.path.join(dir_name, "he_crops", image_layer.metadata['filename']
    #                                    + "_" + tissue_name + '.tiff'), pyramid=True, tile=True, compression=i)
    cropped.dzsave(os.path.join(dir_name, "he_crops", image_layer.metadata['filename']
                                + "_" + tissue_name))
    return tissue_name

