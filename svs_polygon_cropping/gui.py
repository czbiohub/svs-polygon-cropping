from qtpy.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import QThreadPool
from ._key_bindings import crop_tissue

class CropWidget(QWidget):
    def __init__(self, napari_viewer):
        """
        Add gui elements to the viewer
        """
        self.viewer = napari_viewer
        super().__init__()

        layout = QVBoxLayout()

        # Turn off ipython console if it is on
        view = napari_viewer.window.qt_viewer
        # Check if console is present before it is requested
        if view._console is not None:
            # Check console has been created when it is supposed to be shown
            view.toggle_console_visibility(None)

        tissue_name_input = QLineEdit()
        tissue_name_input.setPlaceholderText("Tissue name")
        layout.addWidget(tissue_name_input)
        self.tissue_name_input = tissue_name_input

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        crop_tissue_btn = QPushButton("Crop a tissue")
        crop_tissue_btn.clicked.connect(self._crop_tissue_on_click)
        crop_tissue_btn.setToolTip("Crop out only 1 tissue over which polygon is drawn")
        layout.addWidget(crop_tissue_btn)
        self.crop_tissue_btn = crop_tissue_btn


        self.setLayout(layout)

    def _crop_tissue_on_click(self):
        crop_tissue(self.viewer, self.tissue_name_input.text(), self.threadpool)