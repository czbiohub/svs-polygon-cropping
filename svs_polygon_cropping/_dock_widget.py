from napari_plugin_engine import napari_hook_implementation

from .gui import CropWidget

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return (CropWidget, dict(area="right", allowed_areas=["right", "left"]))