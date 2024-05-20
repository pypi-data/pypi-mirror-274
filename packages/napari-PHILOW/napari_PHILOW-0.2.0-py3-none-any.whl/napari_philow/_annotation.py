import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from magicgui import magicgui
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from napari._qt.qthreading import thread_worker
from qtpy.QtWidgets import QWidget, QPushButton, QSizePolicy, QLineEdit, QCheckBox, QLabel, QVBoxLayout, QFileDialog, QFormLayout
from qtpy.QtCore import Qt
from scipy import ndimage
from skimage import io
from vispy.color import Colormap

from napari_philow._data_manager import Datamanager
from napari_philow._utils import load_images, load_saved_masks, load_raw_masks, label_ct, \
    label_and_sort, save_masks, crop_img, show_so_layer, load_mask_masks


class AnnotationMode(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self._viewer = napari_viewer
        self.opath = ""
        self.modpath = ""
        self.maskpath = ""
        self.btn1 = QPushButton('Open', self)
        self.btn1.clicked.connect(self.show_dialog_o)
        self.lbl1 = QLabel("Not selected")
        self.btn2 = QPushButton('Open', self)
        self.btn2.clicked.connect(self.show_dialog_mod)
        self.lbl2 = QLabel("Not selected")

        self.textbox = QLineEdit(self)

        self.checkBox = QCheckBox("Create new dataset?")

        self.checkBox_mask = QCheckBox("Apply mask? (If you are labeling cristae, please apply a mitochondrial mask)")
        self.checkBox_mask.stateChanged.connect(self.toggle_mask_button)

        self.lbl_mask_dir = QLabel('Mask dir:')
        self.btn_mask = QPushButton('Open', self)
        self.btn_mask.clicked.connect(self.show_dialog_mask)
        self.lbl_mask = QLabel("Not selected")
        self.lbl_mask_dir.hide()
        self.btn_mask.hide()
        self.lbl_mask.hide()

        self.checkBox_3d = QCheckBox("If you are labeling 3D data, please check this box")

        self.btn4 = QPushButton('Start tracing', self)
        self.btn4.clicked.connect(self.launch)

        self.build()

        self.filenames = None

    def build(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.addRow('Original dir:', self.btn1)
        form_layout.addRow(self.lbl1)
        form_layout.addRow('Label dir:', self.btn2)
        form_layout.addRow(self.lbl2)
        form_layout.addRow(self.checkBox_mask)
        form_layout.addRow(self.lbl_mask_dir, self.btn_mask)
        form_layout.addRow(self.lbl_mask)
        form_layout.addRow('Model type (do not use word "train"):', self.textbox)
        form_layout.setLabelAlignment(Qt.AlignLeft)  # 左寄せに設定

        layout.addLayout(form_layout)
        layout.addWidget(self.checkBox)
        layout.addWidget(self.checkBox_3d)
        layout.addWidget(self.btn4)

        self.setLayout(layout)
        self.show()

    def show_dialog_o(self):
        default_path = max(self.opath, self.modpath, os.path.expanduser('~'))
        f_name = QFileDialog.getExistingDirectory(self, 'Open Directory', default_path)
        if f_name:
            self.opath = f_name
            self.lbl1.setText(f_name)

    def show_dialog_mod(self):
        default_path = max(self.opath, self.modpath, os.path.expanduser('~'))
        f_name = QFileDialog.getExistingDirectory(self, 'Open Directory', default_path)
        if f_name:
            self.modpath = f_name
            self.lbl2.setText(f_name)

    def show_dialog_mask(self):
        default_path = max(self.opath, self.modpath, os.path.expanduser('~'))
        f_name = QFileDialog.getExistingDirectory(self, 'Open Directory', default_path)
        if f_name:
            self.maskpath = f_name
            self.lbl_mask.setText(f_name)

    def toggle_mask_button(self, state):
        if state == Qt.Checked:
            self.lbl_mask_dir.show()
            self.btn_mask.show()
            self.lbl_mask.show()
        else:
            self.lbl_mask_dir.hide()
            self.btn_mask.hide()
            self.lbl_mask.hide()

    def launch(self):
        images = load_images(self.opath)
        if self.modpath == "":
            self.modpath = os.path.join(os.path.dirname(self.opath), self.textbox.text())
            os.makedirs(self.modpath, exist_ok=True)
        else:
            pass
        if len(os.listdir(self.modpath)) == 0:
            labels = np.zeros_like(images.compute())
            self.filenames = [fn.name for fn in sorted(list(Path(self.opath).glob('./*png')))]
            for i, filename in enumerate(self.filenames):
                io.imsave(os.path.join(self.modpath, filename), labels[i])
        else:
            labels, self.filenames = load_saved_masks(self.modpath)
        try:
            labels_raw = load_raw_masks(self.modpath + '_raw')
        except:
            labels_raw = None
        if self.maskpath == "":
            mask = None
        else:
            mask = load_mask_masks(self.maskpath)
        self._viewer.window.remove_dock_widget(self)
        self.launch_anm(images, labels, labels_raw, mask)

    def launch_anm(self, original, base, raw, mask):
        global slicer
        global z_pos
        global layer
        global images_original
        global base_label
        r_path = self.modpath
        model_type = self.textbox.text()
        checkbox = self.checkBox.isChecked()
        images_original = original
        base_label = base
        try:
            del layer
        except NameError:
            pass
        self._viewer.add_image(images_original, contrast_limits=[0, 255])
        self._viewer.add_labels(base_label, name='base')
        if raw is not None:
            if self.checkBox_3d.isChecked():
                self._viewer.add_image(ndimage.gaussian_filter(raw, sigma=3), colormap='magenta', name='low_confident',
                                       blending='additive')
            else:
                self._viewer.add_image(ndimage.gaussian_filter(raw, sigma=(0, 3, 3)), colormap='magenta', name='low_confident',
                                       blending='additive')
        else:
            pass
        if mask is not None:
            self._viewer.add_image(mask, name='mask', blending='minimum')

        @thread_worker(connect={"returned": show_so_layer})
        def create_label(viewer):
            labeled_sorted, nums = label_and_sort(base_label)
            print(nums)
            labeled_c = label_ct(labeled_sorted, nums, 10)
            return labeled_c, labeled_sorted, nums, viewer

        if len(np.unique(base_label)) > 1:
            create_label(self._viewer)

        layer = self._viewer.layers[0]
        layer1 = self._viewer.layers[1]

        @magicgui(dirname={"mode": "d"}, call_button=False)
        def dirpicker(dirname=Path(r_path)):
            """Take a filename and do something with it."""
            print("The filename is:", dirname)
            return dirname

        self._viewer.window.add_dock_widget(dirpicker, area='bottom')

        @magicgui(call_button="save")
        def saver():
            # out_dir = gui.dirname
            out_dir = dirpicker.dirname.value
            print("The directory is:", out_dir)
            return save_masks(layer1.data, out_dir, self.filenames)

        self._viewer.window.add_dock_widget(saver, area='bottom')

        dmg = Datamanager()
        dmg.prepare(r_path, model_type, checkbox)
        self._viewer.window.add_dock_widget(dmg, area='left')

        def update_button(axis_event):
            # axis = axis_event.axis
            # if axis != 0:
            #    return
            slice_num, _, _ = axis_event.value
            dmg.update(slice_num)

        self._viewer.dims.events.current_step.connect(update_button)

        # draw canvas

        with plt.style.context('dark_background'):
            canvas = FigureCanvas(Figure(figsize=(3, 15)))

            xy_axes = canvas.figure.add_subplot(3, 1, 1)

            xy_axes.imshow(np.zeros((100, 100), np.uint8))
            xy_axes.scatter(50, 50, s=10, c='red', alpha=0.15)
            xy_axes.set_xlabel('x axis')
            xy_axes.set_ylabel('y axis')
            yz_axes = canvas.figure.add_subplot(3, 1, 2)
            yz_axes.imshow(np.zeros((100, 100), np.uint8))
            yz_axes.scatter(50, 50, s=10, c='red', alpha=0.15)
            yz_axes.set_xlabel('y axis')
            yz_axes.set_ylabel('z axis')
            zx_axes = canvas.figure.add_subplot(3, 1, 3)
            zx_axes.imshow(np.zeros((100, 100), np.uint8))
            zx_axes.scatter(50, 50, s=10, c='red', alpha=0.15)
            zx_axes.set_xlabel('x axis')
            zx_axes.set_ylabel('z axis')

            # canvas.figure.tight_layout()
            canvas.figure.subplots_adjust(left=0, bottom=0.1, right=1, top=0.95, wspace=0, hspace=0.4)

        self._viewer.window.add_dock_widget(canvas, area='right')

        @layer.mouse_drag_callbacks.append
        def update_canvas_canvas(layer, event):
            if 'shift' in event.modifiers:
                try:
                    m_point = np.round(self._viewer.cursor.position).astype(int)
                    print(m_point)
                    crop_big = crop_img([m_point[0], m_point[1], m_point[2]], layer)
                    xy_axes.imshow(crop_big[50], 'gray')
                    yz_axes.imshow(crop_big.transpose(1, 0, 2)[50], 'gray')
                    zx_axes.imshow(crop_big.transpose(2, 0, 1)[50], 'gray')
                    canvas.draw_idle()
                except Exception as e:
                    print(e)
