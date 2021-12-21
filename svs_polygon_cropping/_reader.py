import os

import dask.array as da
import zarr
from napari_plugin_engine import napari_hook_implementation
from openslide import PROPERTY_NAME_COMMENT, OpenSlide, OpenSlideUnsupportedFormatError

from .log_writer import notify
from .store import OpenSlideStore


@napari_hook_implementation
def napari_get_reader(path):
    """A basic implementation of the napari_get_reader hook specification.

    Parameters
    ----------
    path : str
        Path to file

    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list):
        # Don't handle multiple paths
        notify("List of input paths not accepted")
        return failed_reader_function

    if OpenSlide.detect_format(path) is None:
        notify("Please make sure input format is .svs")
        return failed_reader_function

    try:
        slide = OpenSlide(path)
    except OpenSlideUnsupportedFormatError:
        notify("There seems to be an issue with the input file")
        return failed_reader_function

    description = slide.properties.get(PROPERTY_NAME_COMMENT)
    # Don't try to handle OME-TIFF
    # https://github.com/cgohlke/tifffile/blob/b346e3bd7de81de512a6715b01124c8f6d60a707/tifffile/tifffile.py#L5781
    if description and description[-4:] == "OME>":
        notify("This plugin does not handle OME files")
        return failed_reader_function

    # Don't try to handle files that aren't multiscale.
    if slide.level_count == 1:
        notify("Make sure the .svs file is multi-scale")
        return failed_reader_function

    slide.close()
    return reader_function


# Napari_get_reader must return another function.
# This function returns [(None,)] to disallow any another plugins from reading the input path
def failed_reader_function(_path):
    return [(None,)]


def reader_function(path):
    """Takes a path and returns a LayerData tuple where the data is a dask.array.

    Parameters
    ----------
    path : str
        Path to file

    Returns
    -------
    layer_data : list of LayerData tuples
    """

    store = OpenSlideStore(path)
    grp = zarr.open(store, mode="r")

    multiscales = grp.attrs["multiscales"][0]
    pyramid = [
        da.from_zarr(store, component=d["path"]) for d in multiscales["datasets"]
    ]

    add_kwargs = {"name": "image",
                  'metadata': {
                      'path': path, 'filename': os.path.splitext(os.path.basename(path))[0]}}

    return [(pyramid, add_kwargs)]
